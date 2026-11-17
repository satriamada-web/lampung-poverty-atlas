#!/usr/bin/env python3
"""Download Lampung village/kelurahan boundaries from BIG ArcGIS REST.

Uses the layer's object IDs to avoid silently truncating results at the
service's maximum record count. No third-party Python packages are required.
"""

from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE_URL = (
    "https://geoservices.big.go.id/rbi/rest/services/"
    "BATASWILAYAH/BATAS_DESAKEL_AR/MapServer/0/query"
)
WHERE = "WADMPR LIKE '%Lampung%'"
BATCH_SIZE = 250
PAUSE_SECONDS = 0.5
OUTPUT = Path("data/boundaries/raw/lampung_villages.geojson")
METADATA = Path("data/boundaries/raw/lampung_villages.metadata.json")


def request_json(params: dict) -> dict:
    url = BASE_URL + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "RUPIA-Lampung-Atlas/1.0"},
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        payload = json.loads(response.read().decode("utf-8"))

    if "error" in payload:
        raise RuntimeError(f"BIG API error: {payload['error']}")
    return payload


def get_object_ids() -> tuple[str, list[int]]:
    result = request_json({
        "where": WHERE,
        "returnIdsOnly": "true",
        "returnGeometry": "false",
        "f": "json",
    })
    object_id_field = result.get("objectIdFieldName")
    object_ids = result.get("objectIds") or []

    if not object_id_field:
        raise RuntimeError(
            "BIG response did not provide objectIdFieldName. "
            f"Response keys: {list(result.keys())}"
        )
    if not object_ids:
        raise RuntimeError(
            "No matching features found. Check the province filter and BIG layer."
        )

    return object_id_field, sorted(set(int(value) for value in object_ids))


def download_features(object_id_field: str, object_ids: list[int]) -> list[dict]:
    features_by_id: dict[int, dict] = {}

    for start in range(0, len(object_ids), BATCH_SIZE):
        batch = object_ids[start:start + BATCH_SIZE]
        result = request_json({
            "objectIds": ",".join(map(str, batch)),
            "outFields": "*",
            "returnGeometry": "true",
            "outSR": "4326",
            "f": "geojson",
        })

        features = result.get("features") or []
        if result.get("exceededTransferLimit"):
            raise RuntimeError(
                "BIG reports exceededTransferLimit for an ID batch. "
                "Reduce BATCH_SIZE and retry."
            )

        for feature in features:
            properties = feature.get("properties") or {}
            feature_id = properties.get(object_id_field)
            if feature_id is None:
                # Some ArcGIS GeoJSON responses expose the object ID in properties
                # with a differently cased key. Do not silently drop such features.
                candidates = [
                    value for key, value in properties.items()
                    if key.lower() == object_id_field.lower()
                ]
                if not candidates:
                    raise RuntimeError(
                        f"Feature is missing object ID field {object_id_field!r}"
                    )
                feature_id = candidates[0]
            features_by_id[int(feature_id)] = feature

        print(
            f"Downloaded {min(start + len(batch), len(object_ids))}/"
            f"{len(object_ids)} requested IDs; "
            f"{len(features_by_id)} unique features received."
        )
        time.sleep(PAUSE_SECONDS)

    missing = sorted(set(object_ids) - set(features_by_id))
    if missing:
        raise RuntimeError(
            f"Incomplete download: {len(missing)} object IDs were not returned. "
            f"First missing IDs: {missing[:10]}"
        )

    return [features_by_id[object_id] for object_id in object_ids]


def main() -> None:
    object_id_field, object_ids = get_object_ids()
    print(f"BIG reports {len(object_ids)} matching object IDs.")

    features = download_features(object_id_field, object_ids)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    collection = {
        "type": "FeatureCollection",
        "name": "Lampung village and kelurahan administrative boundaries",
        "features": features,
    }
    OUTPUT.write_text(
        json.dumps(collection, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    metadata = {
        "title": "Lampung village and kelurahan administrative boundaries",
        "provider": "Badan Informasi Geospasial (BIG)",
        "service": BASE_URL.rsplit("/query", 1)[0],
        "filter": WHERE,
        "object_id_field": object_id_field,
        "expected_feature_count": len(object_ids),
        "downloaded_feature_count": len(features),
        "coordinate_reference": "EPSG:4326",
        "format": "GeoJSON",
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_note": (
            "Raw response features are retained. Verify BIG metadata, "
            "boundary status, administrative codes, and reuse terms before "
            "research publication."
        ),
    }
    METADATA.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    size_mb = OUTPUT.stat().st_size / (1024 * 1024)
    print(f"SUCCESS: {len(features)} features saved to {OUTPUT}")
    print(f"GeoJSON size: {size_mb:.2f} MiB")
    print(f"Metadata saved to {METADATA}")

    # GitHub has a 100 MB hard limit for an individual Git file.
    if size_mb >= 90:
        print(
            "WARNING: GeoJSON is large. Do not commit it directly to Git; "
            "use a release or external object storage."
        )


if __name__ == "__main__":
    main()
