# Product Blueprint — Platform Pelaporan Warga Bandar Lampung

> Nama produk belum ditetapkan. "RuangKita" hanya nama kerja untuk diskusi, bukan identitas final.
> Cakupan awal: Kota Bandar Lampung, Provinsi Lampung, Indonesia.

## 1. Visi produk

Membangun platform publik berbasis open source yang memungkinkan masyarakat melaporkan kondisi nyata di lingkungan mereka, melihat persoalan pada peta, memantau perkembangan laporan, dan mengakses ringkasan data wilayah.

Produk ini berorientasi pada masyarakat umum. Analisis sosial-ekonomi dan statistik wilayah menjadi fitur pendukung, bukan pengganti laporan warga atau data resmi.

## 2. Prinsip produk

- Public-first: siapa pun dapat melihat halaman publik tanpa akun.
- Account-required reporting: akun diperlukan untuk membuat laporan, memberi komentar, dukungan, atau memperbarui laporan.
- Evidence-aware: laporan warga, laporan terverifikasi, data resmi, dan tindak lanjut instansi ditampilkan sebagai jenis informasi yang berbeda.
- Privacy by design: minimalkan data pribadi; jangan tampilkan alamat rumah atau identitas pelapor.
- Open source: kode, dokumentasi, skema data, dan proses kontribusi tersedia di repositori publik.
- Accessible: antarmuka mobile-first, ringan, hemat data, dan dapat digunakan melalui web maupun APK Android.
- No false promises: jangan menyatakan laporan sudah diteruskan atau ditangani instansi tanpa bukti.

## 3. Pengguna dan peran

| Peran | Hak akses utama |
|---|---|
| Pengunjung | Melihat peta, laporan publik, statistik, dan riwayat status |
| Anggota | Hak pengunjung; membuat laporan; mengunggah foto; memberi komentar/dukungan; mengikuti laporan |
| Moderator | Meninjau laporan, menyamarkan informasi sensitif, menandai duplikat, menyembunyikan konten yang melanggar |
| Administrator | Mengelola kategori, peran, konfigurasi, dan audit moderasi |

Pendaftaran diperlukan untuk tindakan yang menulis data. Penjelajahan data publik tidak memerlukan akun.

## 4. Cakupan geografis MVP

- Kota Bandar Lampung.
- Batas kecamatan dan kelurahan sebagai kerangka peta.
- Setiap laporan memiliki titik koordinat dan relasi wilayah bila dapat ditentukan.
- Data batas wilayah harus mencatat sumber, tanggal pengambilan, versi, sistem koordinat, dan keterbatasan.
- Nama/kode wilayah digunakan untuk menghubungkan dataset; pencocokan nama saja harus ditandai untuk pemeriksaan.

## 5. Kategori laporan awal

1. Infrastruktur: jalan, jembatan, trotoar, drainase, penerangan jalan.
2. Lingkungan: sampah, banjir, pencemaran, ruang hijau.
3. Air dan sanitasi: air bersih, saluran, sanitasi.
4. Transportasi: kemacetan, halte, akses angkutan, keselamatan jalan.
5. Fasilitas pendidikan: kondisi fasilitas dan akses.
6. Fasilitas kesehatan: kondisi fasilitas dan akses layanan.
7. Ekonomi lokal: kondisi pasar, akses usaha, fasilitas ekonomi publik.
8. Fasilitas umum dan sosial: taman, ruang publik, fasilitas komunitas.
9. Lainnya: laporan yang belum sesuai kategori.

Kategori ekonomi tidak boleh meminta atau mempublikasikan data keuangan pribadi warga.

## 6. Formulir laporan

Field minimum:
- Judul singkat.
- Kategori dan subkategori.
- Deskripsi kondisi yang diamati.
- Lokasi GPS atau pin pada peta.
- Kelurahan/kecamatan hasil pencocokan lokasi (dapat dikoreksi moderator).
- Foto opsional atau wajib untuk kategori tertentu setelah kebijakan ditetapkan.
- Waktu kejadian menurut pelapor (opsional) dan waktu laporan dibuat oleh server.
- Persetujuan terhadap panduan komunitas dan kebijakan privasi.

Sistem harus:
- Menghapus metadata EXIF sensitif dari foto sebelum publikasi, terutama koordinat dan informasi perangkat.
- Memeriksa tipe file, ukuran, dan konten berbahaya.
- Menyediakan pelaporan penyalahgunaan dan mekanisme penghapusan/penyamaran.
- Tidak menampilkan email, nomor telepon, nama lengkap, atau lokasi pribadi pelapor pada halaman publik.
- Menyimpan lokasi laporan secara proporsional; lokasi sensitif dapat digeneralisasi atau disembunyikan.

## 7. Siklus dan status laporan

Status yang disarankan:
- submitted: baru dikirim, menunggu pemeriksaan.
- under_review: sedang diperiksa moderator.
- published: lolos pemeriksaan dan terlihat publik.
- needs_information: membutuhkan informasi tambahan.
- forwarded: diteruskan ke pihak terkait; hanya jika ada bukti pengiriman.
- in_progress: ada bukti tindak lanjut sedang berlangsung.
- resolved: ada bukti masalah telah ditangani.
- rejected: tidak dipublikasikan, dengan alasan yang dicatat.
- duplicate: duplikat dari laporan lain, dengan tautan ke laporan utama.
- archived: diarsipkan karena kedaluwarsa atau alasan kebijakan.

Setiap perubahan status mencatat aktor, waktu, status sebelumnya, status baru, dan catatan publik/internal yang dipisahkan. Jangan menghapus riwayat status.

## 8. Fitur produk

### MVP — wajib untuk peluncuran awal
- Halaman publik dan peta laporan.
- Pendaftaran, login, dan pemulihan akun.
- Buat laporan dengan kategori, deskripsi, lokasi, dan foto.
- Daftar laporan, detail laporan, filter, dan pencarian.
- Panel moderator untuk tinjau, terbitkan, tolak, atau tandai duplikat.
- Riwayat status dan notifikasi dasar.
- Statistik sederhana: jumlah laporan per kategori, status, dan kelurahan.
- Halaman sumber data, panduan komunitas, kebijakan privasi, dan dokumentasi.

### Setelah MVP stabil
- Dukungan/konfirmasi warga dan komentar termoderasi.
- Deteksi kemungkinan laporan duplikat berdasarkan jarak, waktu, dan kategori.
- Foto tindak lanjut sebelum/sesudah.
- Notifikasi perubahan status.
- Ekspor dataset publik yang sudah dianonimkan.
- Tren laporan per bulan dan per kelurahan.
- PWA/offline draft untuk jaringan tidak stabil.
- APK Android melalui Capacitor dan GitHub Releases.
- API publik dengan rate limit dan dokumentasi.

### Tidak termasuk pada tahap awal
- Klaim bahwa laporan otomatis masuk ke sistem pemerintah.
- Penilaian otomatis tingkat kemiskinan individu/rumah tangga.
- Pengambilan keputusan publik hanya berdasarkan jumlah laporan.
- Pelacakan lokasi pengguna terus-menerus.
- Prediksi atau skor wilayah tanpa metodologi dan validasi yang dipublikasikan.

## 9. Pembaruan otomatis

- Setelah laporan lolos validasi server dan disimpan, daftar laporan serta peta diperbarui melalui realtime subscription atau mekanisme refresh.
- Statistik ringkas dapat diperbarui melalui database view/materialized view atau job terjadwal.
- Dataset batas wilayah dan data statistik resmi diperbarui melalui pipeline terpisah, dengan versi dan tanggal sumber.
- Perubahan status memicu notifikasi kepada pelapor dan pengikut laporan.
- Semua operasi tulis divalidasi di server; jangan mempercayai validasi di aplikasi klien saja.

GitHub Actions digunakan untuk pengujian, validasi dataset, build, dan pekerjaan terjadwal. Layanan backend yang selalu aktif menangani autentikasi, laporan masuk, file, dan realtime.

## 10. Arsitektur teknologi yang diusulkan

| Lapisan | Pilihan awal | Catatan |
|---|---|---|
| Web UI | React + TypeScript + Vite | Mobile-first |
| Android | Capacitor | Mengemas web app menjadi APK |
| Peta | Leaflet | Open source; gunakan tile provider sesuai ketentuan |
| Backend | Supabase atau backend setara | Auth, API, realtime, storage |
| Database | PostgreSQL + PostGIS | Data relasional dan geospasial |
| Foto | Object storage | Private upload, controlled public delivery |
| Data pipeline | Python, Pandas, GeoPandas | Batas wilayah dan statistik |
| CI/CD | GitHub Actions | Test, lint, validasi, build |

Keputusan layanan hosting, provider peta, dan biaya operasional harus ditinjau sebelum peluncuran publik. Supabase hosted adalah layanan terkelola; opsi self-hosting perlu dipertimbangkan jika kontrol infrastruktur menjadi prioritas.

## 11. Model data konseptual

Entitas utama:
- profiles: identitas akun publik minimal dan preferensi.
- reports: judul, deskripsi, kategori, koordinat, wilayah, status, pembuat, waktu.
- report_media: referensi file foto, status moderasi, keterangan.
- report_status_history: jejak perubahan status.
- report_comments: komentar yang termoderasi.
- report_supports: dukungan/konfirmasi anggota.
- administrative_areas: kecamatan/kelurahan dan geometri.
- moderation_actions: tindakan moderator dan alasan.
- official_datasets: sumber, tahun, definisi, level geografis, lisensi, tanggal pembaruan.

Data pribadi akun dipisahkan dari tabel laporan publik. Kebijakan retensi, akses, dan penghapusan perlu dirancang sebelum menyimpan data pengguna sungguhan.

## 12. Keamanan, privasi, dan kepercayaan

- Gunakan Row Level Security atau kontrol akses server setara.
- Pelapor hanya dapat mengubah laporan miliknya sesuai aturan status.
- Moderator memiliki izin terbatas dan seluruh tindakan tercatat.
- Batasi ukuran/jenis file, lakukan pemindaian, dan hapus EXIF sebelum publikasi.
- Terapkan rate limiting, verifikasi email, perlindungan spam, dan backup.
- Sediakan mekanisme koreksi, keberatan, dan penghapusan data.
- Pisahkan laporan yang belum diverifikasi dari laporan terverifikasi.
- Jangan mengumpulkan NIK, alamat rumah, atau data sensitif yang tidak diperlukan.
- Hindari tuduhan terhadap individu; laporan harus berfokus pada kondisi/fasilitas/layanan publik.

## 13. Indikator analitik

Analitik awal:
- Jumlah laporan masuk dan yang dipublikasikan.
- Distribusi kategori dan status.
- Sebaran laporan per kelurahan.
- Waktu median dari pengiriman ke pemeriksaan.
- Jumlah laporan duplikat dan laporan yang memerlukan informasi tambahan.
- Tren laporan bulanan.

Jumlah laporan bukan ukuran langsung tingkat kerusakan atau kemiskinan. Wilayah dengan akses internet dan partisipasi tinggi dapat menghasilkan lebih banyak laporan. Statistik harus menyertakan catatan bias partisipasi.

## 14. Tahapan implementasi

1. Pastikan batas wilayah Kota Bandar Lampung dan struktur kelurahan/kecamatan.
2. Tetapkan nama, identitas visual, dan panduan komunitas.
3. Rancang skema database, autentikasi, dan kebijakan akses.
4. Bangun peta publik dan halaman daftar/detail laporan.
5. Bangun alur pembuatan laporan dan upload foto.
6. Bangun panel moderasi dan riwayat status.
7. Tambahkan realtime, notifikasi, dan statistik.
8. Uji keamanan, privasi, performa, dan aksesibilitas.
9. Rilis web beta untuk kelompok kecil.
10. Setelah stabil, build APK Android dan publikasikan rilis open source.

## 15. Kriteria MVP dianggap siap diuji

- Pengunjung dapat melihat laporan publik tanpa login.
- Pengguna harus login untuk membuat laporan.
- Laporan menyimpan koordinat dan dapat ditampilkan pada peta.
- Foto dapat diunggah dengan batas ukuran dan pemeriksaan keamanan.
- Laporan baru tidak langsung diberi label terverifikasi.
- Moderator dapat menerbitkan, menolak, dan menandai duplikat.
- Riwayat status tidak hilang.
- Data pribadi pelapor tidak ditampilkan secara publik.
- Statistik dapat ditelusuri ke definisi dan sumbernya.
- Tersedia dokumentasi instalasi, kontribusi, lisensi, dan kebijakan privasi.

---

Dokumen ini adalah rancangan produk awal, bukan klaim bahwa fitur-fitur tersebut sudah dibangun. Semua keputusan implementasi perlu diuji bertahap.
