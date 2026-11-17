# RuangKita — Implementation, Operations & Budget Plan

**Product name:** RuangKita  
**Initial service area:** Kota Bandar Lampung, Lampung, Indonesia  
**Primary users:** Public/community members  
**Reporting policy:** Account required to submit or interact; public browsing does not require an account  
**Status:** Planning document. This is not a claim that the product is deployed or operational.

## 1. Product objective

RuangKita is an open-source, public-first civic reporting platform. Residents can submit reports about public infrastructure, environment, public services, transport, and local economic conditions. Reports can include descriptions, photographs, and a map location. Other visitors can view public reports and follow their status.

RuangKita also provides geographic and statistical context for kelurahan and kecamatan. It must distinguish:
- unreviewed citizen submissions;
- moderator-reviewed reports;
- independently corroborated observations;
- official datasets;
- documented follow-up by an agency or responsible party.

A citizen report is not automatically an official complaint, a verified fact, or proof that an agency has received it.

## 2. Product principles

1. Public access to published reports without requiring an account.
2. Accounts required for report submission, comments, support/confirmation, and report following.
3. Minimal personal-data collection.
4. Location precision appropriate to the issue; do not expose a reporter's home or private location.
5. Photos must be checked for privacy and stripped of sensitive EXIF metadata before publication.
6. Moderation before public publication.
7. Transparent status history and correction/appeal process.
8. Open-source code, documented data schemas, and documented contribution process.
9. Mobile-first, low-bandwidth experience.
10. No claims of government integration or official resolution without evidence.

## 3. User roles

| Role | Permissions |
|---|---|
| Visitor | Browse map, public reports, aggregate statistics, and methodology |
| Member | Create reports; upload media; comment/support/follow where enabled; edit own draft |
| Moderator | Review, publish, reject, redact, merge duplicates, manage abuse reports |
| Administrator | Manage roles, categories, configuration, backups, and audit records |

Role assignment must be enforced server-side, not merely hidden in the UI.

## 4. MVP scope

### Public experience
- Home page with explanation, coverage area, and latest reports.
- Interactive Bandar Lampung map.
- List and detail pages for published reports.
- Filters for category, date, status, kecamatan, and kelurahan.
- Public report status history.
- Basic aggregate statistics and methodology notes.

### Member experience
- Email-based account registration and sign-in.
- Password reset and account deletion request.
- Create report with title, category, description, location pin/GPS, and photo.
- Draft/save and submission confirmation.
- View own reports and status updates.
- Follow a report and receive email/in-app notifications (later MVP increment).

### Moderator experience
- Queue of pending submissions.
- View report, location, images, and privacy warnings.
- Publish, request information, reject with reason, mark duplicate, redact, or archive.
- Record every moderation action with actor and timestamp.
- Separate internal notes from public notes.

### MVP non-goals
- Automatic forwarding to government systems.
- Automated poverty classification for individuals or households.
- AI-based truth determination.
- Public display of reporter identity or home address.
- Nationwide coverage.
- Native Android-specific functionality that cannot be delivered through a responsive web app.

## 5. Reporting categories

Initial categories:
- Infrastructure: roads, bridges, sidewalks, drainage, street lighting.
- Environment: waste, flooding, pollution, green/public spaces.
- Water and sanitation.
- Transport and road safety.
- Education facilities and access.
- Health facilities and access.
- Public facilities and social spaces.
- Local economy/public market facilities.
- Other.

Keep categories focused on observable public conditions. Do not ask users to submit private financial or medical details.

## 6. Report lifecycle

Suggested states:
1. submitted — received; not yet reviewed.
2. under_review — moderator is checking it.
3. needs_information — more details are required.
4. published — passed moderation and appears publicly.
5. forwarded — evidence exists that it was sent to a responsible party.
6. in_progress — evidence exists of work underway.
7. resolved — evidence supports that the reported issue was addressed.
8. rejected — not published; reason recorded.
9. duplicate — linked to a primary report.
10. archived — no longer active, with reason.

Every transition records timestamp, actor, previous state, new status, and a public/internal note. Never imply forwarded, in progress, or resolved without supporting evidence. Users can flag a report or request correction.

## 7. End-to-end system flow

### A. Submission
1. Member signs in.
2. Member chooses category and writes a factual description.
3. Member pins the issue location or grants one-time location permission.
4. Member attaches a photo if available.
5. Client checks required fields and file size/type.
6. Server re-validates the request, stores the report as submitted, and stores media in private/quarantine storage.
7. System returns a report reference number.

### B. Moderation
1. Moderator opens the pending queue.
2. Checks relevance, duplicate reports, location, abusive content, personal data, and image privacy.
3. Requests changes, rejects, merges as duplicate, or publishes.
4. Before public image delivery, strip EXIF metadata and redact/blur sensitive faces, license plates, and private details when necessary.
5. On publication, expose only approved public fields.

### C. Public display and automatic updates
1. Published report is available through the public API.
2. Map/list updates through realtime subscription or short refresh interval.
3. Aggregate counters update through database views or scheduled aggregation.
4. Reporter/followers receive notification on status changes.
5. A scheduled job checks stale reports and reminds moderators; it does not automatically mark them resolved.

### D. Official data updates
1. Store source name, dataset title, publisher, geographic level, reference year, retrieval date, licence, and methodology.
2. Download to raw/immutable storage.
3. Validate format, expected coverage, codes, geometry, and missing values.
4. Transform into processed tables.
5. Publish new dataset version only after review.
6. Keep prior versions for reproducibility.

## 8. Recommended architecture

### Phase-one stack
| Layer | Recommended tool | Purpose |
|---|---|---|
| Source control | GitHub public repository | Code, issues, documentation, releases |
| Web UI | React + TypeScript + Vite | Responsive web application |
| UI styling | Tailwind CSS or CSS modules | Accessible consistent design |
| Map | Leaflet | Interactive map |
| Android package | Capacitor | Build Android APK/AAB from web app |
| Backend/Auth | Supabase | Authentication, APIs, realtime |
| Database | PostgreSQL + PostGIS | Reports, roles, coordinates, boundaries |
| Media | Supabase Storage initially | Report photos with access controls |
| Frontend hosting | Cloudflare Pages | Static web hosting and deploy on Git push |
| Data pipeline | Python, Pandas, GeoPandas | Import and validate official datasets |
| CI/CD | GitHub Actions | Lint, tests, dataset checks, build |
| Error monitoring | Sentry or equivalent, later | Error visibility; review privacy settings |
| Email | Supabase Auth email initially; dedicated SMTP later | Verification and notifications |

Supabase is a managed service and is not fully self-hosted by default. The application code and underlying PostgreSQL/PostGIS ecosystem are open-source; if infrastructure independence becomes necessary, plan a separate self-hosting migration and operations budget.

### Architecture rule
The public client must never contain service-role keys, database passwords, storage admin keys, or other secrets. Use public/anon client credentials only with strict Row Level Security (RLS). Privileged actions run in server-side functions.

### Map tile policy
OpenStreetMap data is open, but the community tile servers are not an unlimited free production map API. For early low-traffic tests, use a tile source only if its current usage policy is followed, show required attribution, respect caching, and do not bulk-download tiles. For a public launch, choose a tile provider with an appropriate plan or host tiles yourself.

## 9. Data model — initial tables

- profiles: user ID, public display name, account status, created date. Keep email and private fields outside public profile views.
- reports: ID, creator ID, title, description, category, status, point geometry, administrative-area ID, timestamps, public visibility.
- report_media: report ID, private storage key, media type, moderation state, redaction state, caption.
- report_status_history: report ID, old/new status, actor, timestamp, note visibility.
- report_comments: report ID, author ID, body, moderation state, created date.
- report_supports: report ID, member ID, support/confirmation type, timestamp.
- administrative_areas: code, name, type, parent code, geometry, source/version.
- moderation_actions: target, moderator, action, reason, timestamp.
- official_datasets: title, source, year, geographic level, licence, retrieval date, processing version.
- notifications: user, event, delivery state, timestamp.

Use PostGIS geography/geometry types and spatial indexes for geographic queries. Install PostGIS into the recommended dedicated extensions schema in Supabase, not public.

## 10. Security and privacy controls

Required before public beta:
- RLS on all user-facing tables.
- Anonymous users can read only published public views.
- Members can create reports and access their own private drafts.
- Members cannot set their own role or moderation status.
- Moderators/admins use server-verified roles.
- File uploads use private/quarantine storage, size/type limits, and signed access.
- Strip EXIF before publishing images.
- Avoid exposing reporter email, phone, full name, or precise private location.
- Rate limits, abuse reporting, spam controls, email verification, and audit logs.
- Database backups and tested restore procedure.
- Incident contact and data deletion/correction process.
- Privacy policy, terms of use, community guidelines, and retention schedule.

Do not collect NIK, home address, financial account data, or health details unless a separate, justified, legally reviewed requirement exists. Review Indonesia's Personal Data Protection Law (UU 27/2022) and applicable electronic-system operator requirements before public launch. Confirm PSE registration applicability with the current Komdigi/OSS process and qualified legal guidance; do not assume an open-source or non-profit label automatically creates an exemption.

## 11. Open-source governance

Recommended initial licence:
- Application code: MIT or Apache-2.0. Choose one and add a LICENSE file before external contributions.
- Data: each source dataset keeps its own licence/terms; do not automatically apply the code licence to government or third-party data.
- Contributions: CONTRIBUTING.md, issue templates, pull request template, code of conduct, security reporting instructions.
- Secrets: keep in GitHub Actions secrets or hosting environment variables; never commit .env.
- Public repository does not mean user reports or uploaded photos are open data. User-generated content needs separate terms and explicit publication consent.

## 12. Hosting and cost plan

All figures below are planning estimates, not quotes. Provider prices, taxes, exchange rates, usage, and eligibility can change. Use a budget ceiling and usage alerts.

### A. Prototype / private development
| Item | Expected cost |
|---|---:|
| GitHub public repo and Actions | Rp0 at current public-repository policy |
| Cloudflare Pages static hosting | Rp0 within free limits |
| Supabase Free | Rp0 within quotas |
| Leaflet | Rp0 licence cost |
| Capacitor | Rp0 licence cost |
| Python/Pandas/GeoPandas | Rp0 licence cost |
| Domain | Optional; defer purchase |
| Google Play | Not needed for APK testing via direct distribution |

Estimated monthly recurring cost: Rp0, excluding optional domain, connectivity, and any paid map/email service. Supabase Free can pause projects after a week of inactivity and has small storage/bandwidth quotas, so it is for development/testing, not a dependable public service.

### B. Small public beta
| Item | Planning allowance |
|---|---:|
| Supabase Pro | US$25/month; approximately Rp400,000–450,000/month using a rough Rp16,000–18,000/USD planning rate |
| Domain | approximately Rp30,000–250,000/year depending on TLD/registrar and renewal |
| Frontend hosting | Rp0 within free static hosting limits |
| Map tiles | Rp0 only if using a permitted free provider within policy; otherwise provider-specific |
| Email | Rp0 at low volume if included quota is sufficient; otherwise variable |
| Monitoring | Rp0 at low volume/free tier |
| Play Console | US$25 one-time registration fee, plus conversion/tax/card fees |
| Contingency | reserve Rp50,000–150,000/month for unexpected usage/services |

A practical initial operating budget is roughly Rp450,000–650,000/month once the backend is on Pro, plus domain and one-time store publishing costs. This is a planning envelope, not a guarantee. It can be lower during closed testing and higher if photos, map requests, bandwidth, or email volume grow.

### C. Growth stage
When reports and photo views grow:
- Review storage and egress monthly.
- Compress images and create thumbnails.
- Add a paid tile provider if needed.
- Add dedicated email delivery and error monitoring.
- Consider a separate object-storage provider.
- Consider larger database compute only after measuring actual load.
- Budget for backups, security review, support, moderation time, and legal compliance.

Do not pay for VPS, Kubernetes, AI APIs, SMS OTP, or complex infrastructure during MVP unless a measured need appears.

## 13. Photo storage policy and cost control

- Resize/compress images before upload while retaining enough evidence detail.
- Set an upload limit (for example 5–8 MB per original; tune after testing).
- Generate thumbnails for map/list views.
- Keep original images private; publish sanitized copies.
- Set retention policy for rejected or duplicate uploads.
- Do not use public buckets for unreviewed uploads.
- Track storage and egress; photos viewed repeatedly may cost more than the initial upload.
- Consider object storage with a suitable egress model after real usage is measured.

## 14. Android distribution

First release a responsive web app/PWA and test it on Android. Then package with Capacitor.

Distribution sequence:
1. Internal APK builds for the project team.
2. Closed beta with invited residents and community testers.
3. Public APK release via GitHub Releases with checksum and release notes.
4. Google Play release after identity, testing, privacy, store listing, and policy requirements are satisfied.

Google Play developer registration is currently US$25 one-time. Personal accounts may have specific testing and device verification requirements. Do not promise a Play Store launch date before those checks are complete.

## 15. Delivery roadmap

Indicative timeline for one beginner developer working part-time with guided implementation. Actual duration depends on learning pace, testing, and available contributors.

| Stage | Deliverables | Exit criteria |
|---|---|---|
| 0. Product foundation | Name, scope, repo docs, licence, policies draft | Scope and governance approved |
| 1. Geographic foundation | Bandar Lampung kecamatan/kelurahan boundaries | Coverage, codes, source, and geometry validated |
| 2. Backend foundation | Supabase project, schema, RLS, auth | Security tests pass |
| 3. Public web | Home, map, list/detail pages | Visitors can browse public data |
| 4. Reporting | Account, report form, location, photo upload | Test report safely stored |
| 5. Moderation | Queue, publish/reject/duplicate, audit history | Unreviewed reports never appear as verified |
| 6. Live updates | Realtime list/map, status notification, aggregates | Status and report changes propagate |
| 7. Beta | User testing, bug fixes, privacy/security review | No critical defects; backup/restore tested |
| 8. Android | Capacitor build, APK, release workflow | Install and core flows work on Android |
| 9. Public launch | Documentation, support channel, outreach | Moderation and operations can sustain launch |

## 16. Success metrics

Do not measure success only by downloads. Measure:
- Number of monthly active local contributors.
- Percentage of submissions reviewed within target time.
- Median moderation time.
- Percentage of reports with usable location and evidence.
- Duplicate/spam rate.
- Percentage of published reports receiving meaningful updates.
- Time from report to documented follow-up (where evidence exists).
- Geographic coverage and participation bias by kelurahan.
- App crash/error rate and uptime.
- Cost per published report and monthly storage/egress.

Set targets after a small pilot baseline is measured. Do not compare kelurahan by raw report count without noting differences in population, connectivity, and participation.

## 17. Operating model

Before public launch, assign at least:
- One product/technical owner.
- One backup administrator.
- Two or more trained moderators if public submissions are open.
- A published moderation policy and expected review window.
- A support contact and escalation process.
- A weekly review of abuse, unresolved queue, backups, and costs.
- A monthly public transparency summary.

If only one person is available, keep the beta invite-only and cap submissions until moderation capacity exists.

## 18. Launch checklist

- [ ] Product name and domain availability checked.
- [ ] Code licence and dataset licences documented.
- [ ] Privacy policy, terms, and community guidelines reviewed.
- [ ] PSE/PDP applicability assessed.
- [ ] Bandar Lampung boundary dataset validated.
- [ ] Database RLS tests passed.
- [ ] Upload restrictions and EXIF stripping tested.
- [ ] Moderator queue and audit history tested.
- [ ] Backup and restore tested.
- [ ] Error monitoring and cost alerts configured.
- [ ] Public status labels and limitations explained.
- [ ] Accessibility and low-bandwidth tests completed.
- [ ] Android beta tested on multiple devices.
- [ ] Moderation team and contact process ready.

## 19. Immediate next steps

1. Finish the current BIG boundary download workflow, but do not use the Lampung-wide output as the final Bandar Lampung dataset without filtering and validating the city boundary.
2. Find an authoritative, current kecamatan/kelurahan boundary source for Bandar Lampung and record provenance.
3. Add the project licence, contribution guide, code of conduct, and security policy.
4. Design the database schema and RLS before building public forms.
5. Build the public map/list experience before opening user submissions.
6. Launch a small invite-only pilot, learn from real reports, then expand.

## References for planning

- Supabase pricing: https://supabase.com/pricing
- Supabase billing: https://supabase.com/docs/guides/platform/billing-on-supabase
- Supabase PostGIS: https://supabase.com/docs/guides/database/extensions/postgis
- Cloudflare Pages limits: https://developers.cloudflare.com/pages/platform/limits/
- GitHub pricing: https://github.com/pricing
- OpenStreetMap tile policy: https://operations.osmfoundation.org/policies/tiles/
- Google Play Console registration: https://support.google.com/googleplay/android-developer/answer/6112435
- Indonesia UU 27/2022 PDP: https://peraturan.bpk.go.id/Details/229798/uu-no-27-
- Komdigi PSE guidance: https://pse.komdigi.go.id/panduan/kriteria-pendaftaran-pse-lingkup-privat
