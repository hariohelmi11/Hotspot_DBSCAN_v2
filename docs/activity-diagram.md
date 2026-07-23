# Activity Diagram - Web GIS Analisis Hotspot Kerawanan Ketertiban Umum

## 1. Activity Diagram Utama (End-to-End)

```text
┌─────────┐
│ Start   │
└────┬────┘
     │
     ▼
┌──────────────────────────┐
│ Scheduler / Admin Trigger│
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Ambil Dataset Pemerintah │
│ (Data 2024)             │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Scraping Berita          │
│ (Data 2025-2026)         │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Data Cleaning            │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Deduplication            │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Geocoding Lokasi         │
└────────────┬─────────────┘
             │
             ▼
      ┌───────────────┐
      │ Valid?        │
      └───────┬───────┘
          No  │ Yes
              │
              ▼
┌──────────────────────────┐
│ Simpan ke PostGIS        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Jalankan DBSCAN          │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Hitung Risk Score        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Generate Hotspot Layer   │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Publish API FastAPI      │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Tampilkan di Leaflet.js  │
└────────────┬─────────────┘
             │
             ▼
         ┌───────┐
         │  End  │
         └───────┘
```

---

## 2. Activity Diagram ETL

```text
Start
  │
  ▼
Extract Data Pemerintah
  │
  ▼
Scraping Data Berita
  │
  ▼
Gabungkan Dataset
  │
  ▼
Data Cleaning
  │
  ▼
Normalisasi Tanggal
  │
  ▼
Deduplication
  │
  ▼
Geocoding
  │
  ▼
Validasi Koordinat
  │
  ▼
Load ke PostGIS
  │
  ▼
End
```

---

## 3. Activity Diagram Analisis DBSCAN

```text
Start
  │
  ▼
Ambil Data Incident
  │
  ▼
Ambil Latitude Longitude
  │
  ▼
Jalankan DBSCAN
  │
  ▼
Identifikasi Cluster
  │
  ▼
Hitung Severity Score
  │
  ▼
Hitung Risk Score
  │
  ▼
Simpan Hotspot
  │
  ▼
Publish GeoJSON
  │
  ▼
End
```

---

## 4. Activity Diagram User

```text
Start
  │
  ▼
Buka Aplikasi
  │
  ▼
Pilih Tahun
  │
  ▼
Pilih Wilayah
  │
  ▼
Load Hotspot
  │
  ▼
Hover Hotspot
  │
  ▼
Lihat Summary
  │
  ▼
Klik Hotspot
  │
  ▼
Load Detail Cluster
  │
  ▼
Tampilkan Side Panel
  │
  ▼
Lihat Riwayat Kejadian
  │
  ▼
End
```

---

## 5. Activity Diagram Admin

```text
Start
  │
  ▼
Login
  │
  ▼
Buka Dashboard Admin
  │
  ▼
Jalankan ETL
  │
  ▼
Monitoring Hasil
  │
  ▼
Jalankan DBSCAN
  │
  ▼
Generate Hotspot
  │
  ▼
Publish Layer
  │
  ▼
Selesai
```
