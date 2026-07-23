# SRS V3 - Web GIS Analisis Hotspot Kerawanan Ketertiban Umum DKI Jakarta

## 1. Informasi Dokumen

### Nama Sistem
Web GIS Analisis Hotspot Kerawanan Ketertiban Umum DKI Jakarta

### Versi
3.0

### Tujuan
Membangun platform Web GIS untuk mengintegrasikan data kerawanan ketertiban umum dari sumber pemerintah dan hasil scraping, melakukan analisis hotspot menggunakan DBSCAN, serta menyajikan hasilnya melalui dashboard dan peta interaktif.

---

# 2. Latar Belakang

Dataset kerawanan ketertiban umum tersedia pada portal Satu Data Jakarta sebagai sumber data resmi historis. Sistem ini akan menggunakan data tahun 2024 sebagai baseline serta melengkapi data tahun 2025–2026 melalui proses scraping dan geocoding.

---

# 3. Business Objective

- Mengidentifikasi hotspot kerawanan ketertiban umum.
- Menyediakan analisis spasial berbasis DBSCAN.
- Menampilkan perkembangan hotspot antar tahun.
- Mendukung pengambilan keputusan berbasis lokasi.

---

# 4. Scope

## In Scope

- Integrasi dataset pemerintah 2024
- Web scraping 2025-2026
- Geocoding lokasi kejadian
- ETL Pipeline
- PostgreSQL + PostGIS
- Analisis DBSCAN
- Risk Scoring
- Dashboard Statistik
- REST API
- GeoJSON API
- Web GIS Leaflet

## Out of Scope

- Mobile Application
- Deep Learning Prediction
- CCTV Analytics

---

# 5. Stakeholder

- Administrator
- Analis SIG
- Dinas Terkait
- Masyarakat

---

# 6. Arsitektur Sistem

```text
Dataset Pemerintah (2024)
            +
Scraping Berita (2025–2026)
            |
            v
       ETL Pipeline
            |
            v
        Geocoding
            |
            v
   PostgreSQL + PostGIS
            |
            v
     Spatial Analytics
         (DBSCAN)
            |
            v
          FastAPI
            |
            v
        Leaflet.js
```

---

# 7. Data Acquisition Strategy

## Data Pemerintah

- Satu Data Jakarta
- Data Rawan Ketertiban Umum 2024

## Data Scraping

Sumber:

- Detik
- Kompas
- Antara

Keyword:

- tawuran jakarta
- gangguan ketertiban umum
- kerawanan wilayah
- pelanggaran ketertiban

## Geocoding

Menggunakan OpenStreetMap Nominatim.

---

# 8. ETL Design

## Extract

- Dataset Pemerintah
- Data Hasil Scraping

## Transform

- Cleaning
- Standardisasi tanggal
- Deduplikasi
- Geocoding
- Validasi koordinat
- Penentuan severity

## Load

- PostgreSQL
- PostGIS Geometry

---

# 9. Severity dan Risk Score

## Severity

- Tawuran = 5
- Kriminalitas Lingkungan = 4
- Gangguan Ketertiban = 3
- Pelanggaran Umum = 2
- Keluhan = 1

## Risk Score

```text
Risk Score = Total Severity dalam Cluster
```

Kategori:

- LOW
- MEDIUM
- HIGH
- CRITICAL

---

# 10. Functional Requirements

## FR-01 Dashboard

Menampilkan:

- Total Incident
- Total Hotspot
- High Risk Area
- Critical Area

## FR-02 Interactive Map

- Zoom
- Pan
- Fullscreen
- Layer Control

## FR-03 Incident Marker

Menampilkan:

- Jenis Kejadian
- Tanggal
- Lokasi
- Sumber Data

## FR-04 Hover Hotspot

Menampilkan:

- Cluster ID
- Total Kejadian
- Risk Level
- Jenis Dominan

## FR-05 Detail Hotspot

Side panel:

- Cluster ID
- Risk Score
- Risk Level
- Radius
- Dominant Incident
- Timeline Kejadian

## FR-06 Historical Comparison

Menampilkan:

- Data 2024
- Data 2025
- Data 2026
- Tren Naik/Turun

## FR-07 Filter Data

- Tahun
- Kota Administrasi
- Kecamatan
- Kelurahan
- Jenis Kejadian
- Sumber Data

## FR-08 Heatmap

Menampilkan kepadatan kejadian.

---

# 11. Non Functional Requirements

## Performance

Response API < 2 detik.

## Scalability

500.000+ record.

## Availability

99%.

## Security

- JWT
- HTTPS
- Role Based Access

---

# 12. Database Design

## users

```sql
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  username VARCHAR(100),
  password_hash TEXT,
  role VARCHAR(50)
);
```

## public_order_incidents

```sql
CREATE TABLE public_order_incidents (
  id BIGSERIAL PRIMARY KEY,
  incident_date DATE,
  incident_year INTEGER,
  location_name TEXT,
  district VARCHAR(100),
  subdistrict VARCHAR(100),
  incident_type VARCHAR(100),
  severity_score INTEGER,
  source VARCHAR(50),
  article_url TEXT,
  latitude DOUBLE PRECISION,
  longitude DOUBLE PRECISION,
  geom geometry(Point,4326),
  created_at TIMESTAMP
);
```

## hotspot_clusters

```sql
CREATE TABLE hotspot_clusters (
  id BIGSERIAL PRIMARY KEY,
  cluster_id INTEGER,
  total_incidents INTEGER,
  dominant_type VARCHAR(100),
  risk_score NUMERIC,
  hotspot_level VARCHAR(50),
  centroid geometry(Point,4326)
);
```

## scrape_logs

```sql
CREATE TABLE scrape_logs (
  id BIGSERIAL PRIMARY KEY,
  execution_time TIMESTAMP,
  total_records INTEGER,
  success BOOLEAN
);
```

---

# 13. Spatial Design

```sql
CREATE INDEX idx_incident_geom
ON public_order_incidents
USING GIST(geom);
```

---

# 14. DBSCAN Design

```python
DBSCAN(
    eps=0.003,
    min_samples=5
)
```

Output:

- cluster_id
- centroid
- radius
- member_count
- risk_score

---

# 15. REST API

## Dashboard
GET /api/v1/dashboard

## Hotspot
GET /api/v1/hotspots
GET /api/v1/hotspots/{id}

## Incident
GET /api/v1/incidents/{id}

## GeoJSON
GET /api/v1/geojson/hotspots

## ETL
POST /api/v1/etl/run

## DBSCAN
POST /api/v1/dbscan/run

---

# 16. Frontend Design

## GIS Layers

- Incident Marker Layer
- Heatmap Layer
- Hotspot Layer
- Administrative Boundary Layer

## Hover Marker

- Jenis Kejadian
- Tanggal
- Wilayah

## Hover Hotspot

- Cluster ID
- Risk Level
- Total Kejadian

## Klik Hotspot

Menampilkan side panel detail dan timeline kejadian.

---

# 17. Activity Flow

```text
Extract
 ↓
Transform
 ↓
Geocoding
 ↓
Load PostGIS
 ↓
DBSCAN
 ↓
Hotspot Layer
 ↓
FastAPI
 ↓
Leaflet
```

---

# 18. Project Structure

```text
backend/
frontend/
docs/

backend/
├── api/
├── services/
├── models/
├── repositories/
├── jobs/
├── db/
└── utils/
```

---

# 19. Deployment Architecture

```text
Nginx
 |
FastAPI
 |
PostgreSQL + PostGIS
```

Docker Services:

- nginx
- fastapi
- postgres
- postgis
- frontend

---

# 20. Future Enhancement

- Prediksi Tren Hotspot
- Real-time Data Collector
- Mobile Responsive PWA
- Multi-City Support
