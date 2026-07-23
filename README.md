# Web GIS Analisis Hotspot Kerawanan Ketertiban Umum DKI Jakarta

> **Sistem Informasi Geografis berbasis Web** untuk mengidentifikasi, menganalisis, dan memvisualisasikan hotspot kerawanan ketertiban umum di wilayah DKI Jakarta menggunakan algoritma **DBSCAN (Density-Based Spatial Clustering of Applications with Noise)**.

---

## Daftar Isi

- [Gambaran Umum](#gambaran-umum)
- [Fitur Utama](#fitur-utama)
- [Tech Stack](#tech-stack)
- [Arsitektur Sistem](#arsitektur-sistem)
- [Struktur Project](#struktur-project)
- [Prasyarat](#prasyarat)
- [Instalasi & Menjalankan](#instalasi--menjalankan)
- [Konfigurasi](#konfigurasi)
- [Dataset](#dataset)
- [ETL Pipeline](#etl-pipeline)
- [Algoritma DBSCAN](#algoritma-dbscan)
- [Risk Scoring](#risk-scoring)
- [API Reference](#api-reference)
- [Antarmuka Web](#antarmuka-web)
- [Testing](#testing)
- [Deployment Production](#deployment-production)
- [Hasil Analisis](#hasil-analisis)
- [Troubleshooting](#troubleshooting)

---

## Gambaran Umum

Sistem ini dibangun sebagai tugas akhir mata kuliah **Sistem Informasi Geografis** dengan tujuan:

1. Mengintegrasikan dataset kerawanan ketertiban umum dari **Satu Data Jakarta tahun 2024**
2. Mengumpulkan data tahun 2025–2026 melalui **web scraping** berita
3. Melakukan **geocoding** otomatis pada data yang tidak memiliki koordinat
4. Menyimpan seluruh data geospasial pada **PostgreSQL + PostGIS**
5. Menjalankan **clustering DBSCAN** untuk mendeteksi hotspot
6. Menghitung **Risk Score** per cluster berdasarkan jenis dan jumlah kejadian
7. Menyajikan hasil melalui **REST API** dan **dashboard Web GIS interaktif**

---

## Fitur Utama

### Peta GIS Interaktif

- **Incident Marker Layer** — titik kejadian per lokasi dengan warna berdasarkan jenis kejadian
- **Heatmap Layer** — kepadatan kejadian menggunakan Leaflet.heat (gradient severity)
- **Hotspot Cluster Layer** — lingkaran cluster DBSCAN dengan warna berdasarkan risk level
- **Layer Control** — toggle setiap layer secara independen
- **Base Map** — OpenStreetMap & CartoDB Dark

### Interaksi Hotspot

- **Hover Marker** — tampil informasi lengkap:
  - Jenis Kejadian, Tanggal
  - Wilayah (Kota Administrasi)
  - Kecamatan & Kelurahan
  - Koordinat GPS (latitude, longitude)
  - Sumber data (pemerintah / scraping)
- **Hover Hotspot** — tampil Cluster ID, jumlah kejadian, risk level, jenis dominan
- **Klik Hotspot** — buka Side Panel detail dengan:
  - Cluster ID, Risk Level, Risk Score, Radius
  - Timeline chronological kejadian
  - **Historical Comparison** (2024 vs 2025 vs 2026 + indikator tren)

### Filter Data

- Filter **Tahun** (2024 / 2025 / 2026 / Semua)
- Filter **Jenis Kejadian** (Tawuran, PKL, Pengemis, dll)
- Filter **Sumber Data** (Pemerintah / Scraping)
- Filter **Wilayah** (free-text kota/kecamatan)

### Dashboard Statistik

- **4 KPI Card**: Total Kejadian, Total Hotspot, High Risk Area, Critical Area
- **Tren Kejadian Tahunan** (Line Chart)
- **Distribusi Jenis Kejadian** (Bar Chart) — dilengkapi **legenda warna** di bawah grafik
- **Distribusi Risk Level** (Pie Chart)
- **Top 10 Wilayah Rawan** (Horizontal Bar Chart)

### Admin Panel

- Trigger **ETL Pipeline** (pemerintah / news / semua)
- Trigger **DBSCAN Analysis** per tahun
- Link ke **Swagger API Docs**

---

## Tech Stack

| Komponen             | Teknologi                                     |
| -------------------- | --------------------------------------------- |
| **Backend**          | Python 3.12, FastAPI 0.111, Uvicorn           |
| **ORM / GIS**        | SQLAlchemy 2.0, GeoAlchemy2, Alembic          |
| **Database**         | PostgreSQL 16 + PostGIS 3.4                   |
| **Machine Learning** | Scikit-Learn (DBSCAN), NumPy                  |
| **ETL**              | Pandas, xlrd, BeautifulSoup4, httpx, geopy    |
| **Scheduler**        | APScheduler 3.10                              |
| **Frontend**         | React 18, Vite 5, TypeScript 5                |
| **UI Framework**     | Bootstrap 5.3                                 |
| **Peta**             | Leaflet.js 1.9, React-Leaflet 4, Leaflet.heat |
| **Chart**            | Chart.js 4, React-ChartJS-2                   |
| **HTTP Client**      | Axios                                         |
| **Deployment**       | Docker, Docker Compose, Nginx                 |

---

## Arsitektur Sistem

```
Dataset Pemerintah (data-rawan.xls 2024)
              +
Scraping Berita (Detik / Kompas / Antara 2025-2026)
              │
              ▼
        ┌─────────────┐
        │ ETL Pipeline│  ← Extract → Clean → Dedup → Geocode → Load
        └──────┬──────┘
               │
               ▼
     ┌──────────────────┐
     │ PostgreSQL +      │
     │ PostGIS           │  ← geometry(Point,4326) + GIST index
     └────────┬─────────┘
              │
              ▼
     ┌──────────────────┐
     │ DBSCAN Service   │  ← eps=0.003° (~333m), min_samples=5
     │ Risk Scoring     │  ← Severity × Count per cluster
     └────────┬─────────┘
              │
              ▼
     ┌──────────────────┐
     │ FastAPI REST API │  ← /api/v1/...
     └────────┬─────────┘
              │
              ▼
     ┌──────────────────┐
     │   Nginx Proxy    │
     └────────┬─────────┘
              │
         ┌────┴────┐
         ▼         ▼
    React SPA   /api/*
    Leaflet.js  FastAPI
```

### Docker Services

```
┌─────────────────────────────────┐
│         hotspot_nginx (:80)     │
│    proxy /api → backend         │
│    proxy /    → frontend        │
└──────────┬───────────┬──────────┘
           │           │
           ▼           ▼
  ┌──────────────┐  ┌──────────────┐
  │   backend    │  │   frontend   │
  │   (:8000)    │  │   (:80)      │
  │   FastAPI    │  │   Nginx SPA  │
  └──────┬───────┘  └──────────────┘
         │
         ▼
  ┌──────────────┐
  │      db      │
  │   (:5432)    │
  │  PostGIS 16  │
  └──────────────┘
```

---

## Struktur Project

```
Hotspot_DBSCAN_v2/
├── docker-compose.yml
├── nginx/
│   └── nginx.conf
├── data/
│   └── data-rawan.xls              ← Dataset pemerintah 2024
├── docs/
│   ├── SRS_V3_WebGIS_Ketertiban_Umum_Complete.md
│   ├── SRS_Frontend_UX_Ketertiban_Umum.md
│   ├── activity-diagram.md
│   └── prompt-generator.md
├── backend/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── 001_initial_schema.py
│   ├── app/
│   │   ├── main.py                 ← FastAPI app + lifespan
│   │   ├── config.py               ← Settings (env-based)
│   │   ├── database.py             ← SQLAlchemy engine + session
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── incident.py         ← public_order_incidents
│   │   │   ├── hotspot.py          ← hotspot_clusters
│   │   │   └── scrape_log.py
│   │   ├── schemas/
│   │   │   ├── incident.py
│   │   │   ├── hotspot.py
│   │   │   └── dashboard.py
│   │   ├── repositories/
│   │   │   ├── incident_repository.py
│   │   │   └── hotspot_repository.py
│   │   ├── services/
│   │   │   ├── etl/
│   │   │   │   ├── government_collector.py  ← Baca XLS + konversi koordinat
│   │   │   │   ├── news_collector.py        ← Web scraping
│   │   │   │   ├── cleaner.py               ← Cleaning + dedup
│   │   │   │   ├── geocoder.py              ← Nominatim geocoding
│   │   │   │   └── pipeline.py              ← Orchestrator ETL
│   │   │   ├── dbscan_service.py            ← DBSCAN + risk scoring
│   │   │   └── dashboard_service.py
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── dashboard.py
│   │   │       ├── hotspots.py
│   │   │       ├── incidents.py
│   │   │       ├── geojson.py
│   │   │       └── jobs.py
│   │   └── jobs/
│   │       └── scheduler.py        ← APScheduler cron jobs
│   └── tests/
│       ├── test_etl.py
│       └── test_api.py
└── frontend/
    ├── Dockerfile
    ├── nginx.conf
    ├── package.json
    ├── vite.config.ts
    ├── tsconfig.json
    └── src/
        ├── main.tsx
        ├── App.tsx
        ├── index.css
        ├── types/index.ts
        ├── services/api.ts
        ├── hooks/
        │   ├── useDashboard.ts
        │   ├── useHotspots.ts
        │   └── useIncidents.ts
        ├── components/
        │   ├── Header.tsx
        │   ├── Filter/FilterPanel.tsx
        │   ├── Dashboard/
        │   │   ├── StatsCards.tsx
        │   │   └── Charts.tsx
        │   ├── Map/
        │   │   ├── MapView.tsx
        │   │   ├── MarkerLayer.tsx
        │   │   ├── HotspotLayer.tsx
        │   │   └── HeatmapLayer.tsx
        │   └── HotspotDetail/SidePanel.tsx
        └── pages/
            ├── MapPage.tsx
            └── AdminPage.tsx
```

---

## Prasyarat

| Software       | Versi Minimum | Keterangan                                |
| -------------- | ------------- | ----------------------------------------- |
| Docker Desktop | 4.x           | Wajib                                     |
| Docker Compose | v2.x          | Sudah include di Docker Desktop           |
| RAM            | 4 GB          | Minimal untuk menjalankan semua container |
| Disk           | 5 GB          | Untuk image Docker dan data PostgreSQL    |

> **Tidak perlu** menginstall Python, Node.js, atau PostgreSQL secara lokal. Semua berjalan di dalam Docker.

---

## Instalasi & Menjalankan

### 1. Clone / Download Project

```bash
cd Hotspot_DBSCAN_v2
```

Pastikan file dataset tersedia di:

```
data/data-rawan.xls
```

### 2. Jalankan dengan Docker Compose

```bash
docker-compose up --build
```

Proses pertama kali membutuhkan waktu **5–10 menit** untuk:

- Download Docker images (Python, Node, Nginx, PostGIS)
- Install Python dependencies (~30 packages)
- Install Node.js dependencies (~103 packages)
- Build React app (TypeScript compile + Vite bundle)
- Jalankan Alembic migrations (buat tabel + PostGIS extension)
- **ETL otomatis** — load `data-rawan.xls` ke database
- **DBSCAN otomatis** — generate hotspot clusters

### 3. Akses Aplikasi

| URL                                      | Deskripsi                              |
| ---------------------------------------- | -------------------------------------- |
| `http://localhost`                       | Aplikasi Web GIS utama                 |
| `http://localhost/docs`                  | Swagger API Documentation (interaktif) |
| `http://localhost:8000/health`           | Backend health check                   |
| `http://localhost:8000/api/v1/dashboard` | Dashboard API langsung                 |

### 4. Menghentikan Aplikasi

```bash
# Stop tanpa hapus data
docker-compose stop

# Stop dan hapus container (data DB tetap ada di volume)
docker-compose down

# Stop dan hapus SEMUA termasuk database volume
docker-compose down -v
```

### 5. Menjalankan Ulang (tanpa rebuild)

```bash
docker-compose up
```

---

## Konfigurasi

Konfigurasi backend melalui environment variable di `docker-compose.yml`:

| Variable             | Default                                                     | Deskripsi                              |
| -------------------- | ----------------------------------------------------------- | -------------------------------------- |
| `DATABASE_URL`       | `postgresql://hotspot_user:hotspot_pass@db:5432/hotspot_db` | Koneksi PostgreSQL                     |
| `SECRET_KEY`         | `change-this-secret-key-in-production`                      | JWT secret key                         |
| `DATA_DIR`           | `/app/data`                                                 | Direktori dataset                      |
| `DBSCAN_EPS`         | `0.003`                                                     | Radius cluster DBSCAN (derajat, ≈333m) |
| `DBSCAN_MIN_SAMPLES` | `5`                                                         | Minimum titik per cluster              |
| `RISK_CRITICAL`      | `100`                                                       | Threshold Risk Score → CRITICAL        |
| `RISK_HIGH`          | `50`                                                        | Threshold Risk Score → HIGH            |
| `RISK_MEDIUM`        | `25`                                                        | Threshold Risk Score → MEDIUM          |

Untuk production, buat file `.env` di folder `backend/`:

```env
DATABASE_URL=postgresql://user:password@db:5432/hotspot_db
SECRET_KEY=your-very-long-random-secret-key-here
DATA_DIR=/app/data
DBSCAN_EPS=0.003
DBSCAN_MIN_SAMPLES=5
```

---

## Dataset

### Data Pemerintah (2024)

- **Sumber**: Portal Satu Data Jakarta
- **File**: `data/data-rawan.xls`
- **Jumlah Record**: 1.018 baris (813 valid setelah validasi koordinat)
- **Kolom**:

| Kolom          | Tipe    | Keterangan                                           |
| -------------- | ------- | ---------------------------------------------------- |
| `periode_data` | Integer | Tahun data (2024)                                    |
| `wilayah`      | String  | Kota Administrasi (e.g., KOTA ADM. JAKARTA TIMUR)    |
| `kecamatan`    | String  | Nama Kecamatan                                       |
| `kelurahan`    | String  | Nama Kelurahan                                       |
| `latitude`     | Float   | Latitude × 1.000.000 (e.g., -6170529 → -6.170529)    |
| `longitude`    | Float   | Longitude × 1.000.000 (e.g., 106819195 → 106.819195) |
| `jenis_rawan`  | String  | Jenis kejadian (e.g., TAWURAN, PKL, PENGEMIS)        |

> **Catatan penting**: Koordinat dalam file XLS disimpan sebagai integer yang sudah dikali 1.000.000. Sistem ini otomatis melakukan konversi ke WGS84 decimal degrees.

### Data Scraping (2025–2026)

- **Sumber**: Detik.com, Kompas.com, Antara
- **Metode**: HTTP scraping + BeautifulSoup parsing
- **Geocoding**: OpenStreetMap Nominatim (rate limit 1 req/detik)
- **Keywords**: `tawuran jakarta`, `gangguan ketertiban umum jakarta`, `kerawanan wilayah jakarta`

---

## ETL Pipeline

```
┌─────────────────────────────────────────────────────────┐
│                     ETL Pipeline                        │
│                                                         │
│  1. EXTRACT                                             │
│     ├── government_collector.py → baca data-rawan.xls  │
│     └── news_collector.py       → scraping berita      │
│                                                         │
│  2. TRANSFORM                                           │
│     ├── cleaner.py → normalize string, tanggal         │
│     ├── cleaner.py → deduplikasi (district+type+year)  │
│     └── geocoder.py → Nominatim geocoding (jika perlu) │
│                                                         │
│  3. LOAD                                                │
│     └── pipeline.py → bulk insert ke PostGIS           │
│         (geom = WKTElement POINT(lon lat) SRID 4326)   │
└─────────────────────────────────────────────────────────┘
```

### Trigger ETL

**Via Admin Panel** (http://localhost → tab Admin):

- Pilih sumber data dan tahun, klik "Jalankan ETL"

**Via API**:

```bash
# Load dataset pemerintah 2024
curl -X POST http://localhost:8000/api/v1/etl/run \
  -H "Content-Type: application/json" \
  -d '{"source": "government", "year": 2024}'

# Scraping berita 2025-2026
curl -X POST http://localhost:8000/api/v1/etl/run \
  -H "Content-Type: application/json" \
  -d '{"source": "news", "year": 2025}'

# Semua sumber
curl -X POST http://localhost:8000/api/v1/etl/run \
  -H "Content-Type: application/json" \
  -d '{"source": "all", "year": 2024}'
```

### Scheduled Jobs (Otomatis)

| Job            | Jadwal                    | Fungsi                       |
| -------------- | ------------------------- | ---------------------------- |
| Daily News ETL | Setiap hari pukul 02.00   | Scraping berita terbaru 2026 |
| Weekly DBSCAN  | Setiap Minggu pukul 03.00 | Re-generate hotspot clusters |

---

## Algoritma DBSCAN

### Parameter

```python
DBSCAN(
    eps=0.003,           # ~333 meter radius (dalam derajat)
    min_samples=5,       # minimum 5 titik per cluster
    algorithm='ball_tree',
    metric='haversine'   # jarak geodetik
)
```

> `eps=0.003` derajat dikonversi ke radian (`np.radians(0.003) ≈ 0.0000524`) sebelum dipakai dengan metric haversine, setara dengan radius **±333 meter** di permukaan bumi.

### Proses

1. Ambil semua incident yang memiliki koordinat valid
2. Bentuk matrix koordinat `[latitude, longitude]` dalam radian
3. Jalankan DBSCAN → setiap titik mendapat label cluster (`-1` = noise/outlier)
4. Untuk setiap cluster:
   - Hitung **centroid** (rata-rata lat/lon)
   - Hitung **radius** (jarak haversine maksimum dari centroid ke titik terjauh)
   - Hitung **Risk Score** = Σ severity semua kejadian dalam cluster
   - Tentukan **jenis dominan** (mode dari incident_type)
5. Simpan ke tabel `hotspot_clusters`
6. Update kolom `hotspot_cluster_id` pada tabel `public_order_incidents`

### Output Cluster

| Field                | Deskripsi                      |
| -------------------- | ------------------------------ |
| `cluster_display_id` | Label tampilan (H-1, H-2, ...) |
| `centroid_lat/lon`   | Pusat geometri cluster         |
| `radius_meters`      | Jangkauan cluster dalam meter  |
| `total_incidents`    | Jumlah kejadian dalam cluster  |
| `dominant_type`      | Jenis kejadian terbanyak       |
| `risk_score`         | Total severity semua kejadian  |
| `hotspot_level`      | LOW / MEDIUM / HIGH / CRITICAL |

---

## Risk Scoring

### Severity per Jenis Kejadian

| Jenis Kejadian                                  | Severity Score |
| ----------------------------------------------- | -------------- |
| TAWURAN (WARGA / PELAJAR)                       | **5**          |
| KRIMINALITAS, PREMANISME, NARKOBA               | **4**          |
| GANGGUAN KETERTIBAN, PKL, MIRAS, BALAP LIAR     | **3**          |
| PENGEMIS, GELANDANGAN, PARKIR LIAR, PELANGGARAN | **2**          |
| Lainnya                                         | **2**          |

### Rumus Risk Score

```
Risk Score = Σ severity_score semua kejadian dalam cluster
```

### Kategori Risk Level

| Risk Level  | Threshold        | Warna  |
| ----------- | ---------------- | ------ |
| 🟢 LOW      | Score < 25       | Hijau  |
| 🟡 MEDIUM   | 25 ≤ Score < 50  | Kuning |
| 🟠 HIGH     | 50 ≤ Score < 100 | Oranye |
| 🔴 CRITICAL | Score ≥ 100      | Merah  |

---

## API Reference

Base URL: `http://localhost:8000/api/v1`

> Dokumentasi interaktif tersedia di `http://localhost/docs` (Swagger UI)

### Dashboard

```http
GET /dashboard
GET /dashboard?year=2024
```

Response:

```json
{
  "stats": {
    "total_incidents": 3252,
    "total_hotspots": 75,
    "high_risk_areas": 6,
    "critical_areas": 1
  },
  "trend": [{ "year": 2024, "count": 3252 }],
  "type_distribution": [{ "incident_type": "PKL", "count": 1228 }],
  "risk_distribution": [{ "risk_level": "CRITICAL", "count": 1 }],
  "top_wilayah": [{ "wilayah": "KOTA ADM. JAKARTA TIMUR", "count": 880 }]
}
```

### Hotspots

```http
GET /hotspots
GET /hotspots?year=2024&risk_level=HIGH
GET /hotspots/{id}
```

Response hotspot detail:

```json
{
  "id": 1,
  "cluster_display_id": "H-1",
  "total_incidents": 56,
  "dominant_type": "PENYALAHGUNAAN (FASUM/FASOS)",
  "risk_score": 132.0,
  "hotspot_level": "CRITICAL",
  "radius_meters": 823.9,
  "analysis_year": 2024,
  "centroid_lat": -6.205,
  "centroid_lon": 106.849,
  "incidents": [...],
  "historical": {
    "2024": 56,
    "trend": "Data tidak cukup"
  }
}
```

### Incidents

```http
GET /incidents?year=2024&district=JAKARTA+TIMUR&page=1&page_size=100
GET /incidents/{id}
```

Query Parameters:
| Parameter | Tipe | Contoh |
|---|---|---|
| `year` | int | `2024` |
| `district` | string | `JAKARTA TIMUR` |
| `subdistrict` | string | `GAMBIR` |
| `incident_type` | string | `TAWURAN` |
| `source` | string | `pemerintah` |
| `page` | int | `1` |
| `page_size` | int | `100` (max 500) |

### GeoJSON

```http
GET /geojson/hotspots
GET /geojson/hotspots?year=2024&risk_level=HIGH
GET /geojson/incidents
GET /geojson/incidents?year=2024&incident_type=TAWURAN
```

Response format GeoJSON FeatureCollection standar (RFC 7946), siap digunakan langsung di Leaflet.js.

Properties tiap feature incident:

| Property         | Keterangan                        |
| ---------------- | --------------------------------- |
| `id`             | ID kejadian                       |
| `incident_type`  | Jenis kejadian                    |
| `incident_date`  | Tanggal kejadian                  |
| `location_name`  | Kelurahan + Kecamatan             |
| `district`       | Kota Administrasi                 |
| `subdistrict`    | Kecamatan                         |
| `severity_score` | Skor keparahan (1–5)              |
| `source`         | Sumber data (pemerintah/scraping) |
| `latitude`       | Koordinat lintang (WGS84)         |
| `longitude`      | Koordinat bujur (WGS84)           |

### Jobs (Admin)

```http
POST /etl/run
Content-Type: application/json
{"source": "government", "year": 2024}

POST /dbscan/run
Content-Type: application/json
{"year": 2024}
```

Kedua endpoint menjalankan proses di **background task** — response langsung dikembalikan.

---

## Antarmuka Web

### Tab Peta GIS

```
┌─────────────────────────────────────────────────────────┐
│  🗺️ Web GIS Hotspot Kerawanan Ketertiban Umum DKI Jakarta│
├─────────────────────────────────────────────────────────┤
│  Tahun ▼  │  Jenis Kejadian ▼  │  Sumber ▼  │ Wilayah  │
├──────────────────────────────────────┬──────────────────┤
│                                      │  HOTSPOT DETAIL  │
│         🗺️  Leaflet Map              │  H-1             │
│                                      │  Risk: CRITICAL  │
│   [📍 Marker][🌡️ Heatmap][🔥 Hotspot] │  Score: 132     │
│                                      │  56 Kejadian     │
│                                      │  ──────────────  │
│                                      │  Timeline:       │
│                                      │  PKL - Kel. A    │
│                                      │  Tawuran - Kel B │
├──────────────────────────────────────┴──────────────────┤
│  📋 813  │  🔥 26  │  ⚠️ 6  │  🚨 1                      │
├─────────────────────────────────────────────────────────┤
│  📈 Tren  │  📊 Distribusi Jenis  │  🎯 Risk  │  🏙️ Top10 │
└─────────────────────────────────────────────────────────┘
```

### Warna Hotspot Cluster pada Peta

| Warna               | Risk Level |
| ------------------- | ---------- |
| 🔴 Merah (#dc3545)  | CRITICAL   |
| 🟠 Oranye (#fd7e14) | HIGH       |
| 🟡 Kuning (#ffc107) | MEDIUM     |
| 🟢 Hijau (#28a745)  | LOW        |

### Warna Marker Incident pada Peta

Warna marker **konsisten** dengan warna batang pada grafik Distribusi Jenis Kejadian:

| Warna                  | Jenis Kejadian             |
| ---------------------- | -------------------------- |
| 🔴 Merah (#dc3545)     | PKL                        |
| 🟠 Oranye (#fd7e14)    | Penyalahgunaan FASUM/FASOS |
| 🟡 Kuning (#ffc107)    | Pak Ogah                   |
| 🟢 Hijau (#28a745)     | Tawuran (Warga / Pelajar)  |
| 🩵 Biru Muda (#0dcaf0) | Pengemis                   |
| 🟣 Ungu (#6f42c1)      | Kriminalitas               |
| 🩵 Teal (#20c997)      | Pengamen                   |
| 🔵 Biru (#0d6efd)      | Pedagang Asongan           |
| ⚪ Abu (#adb5bd)       | Ormas / Warga              |
| ⚫ Gelap (#343a40)     | Pengamen (Manusia Silver)  |

---

## Testing

### Unit Tests (ETL & Cleaner)

```bash
# Jalankan di dalam container
docker exec hotspot_backend pytest tests/ -v

# Atau dari host
docker exec hotspot_backend pytest tests/test_etl.py -v
docker exec hotspot_backend pytest tests/test_api.py -v
```

Contoh output:

```
tests/test_etl.py::TestCleaner::test_clean_valid_record PASSED
tests/test_etl.py::TestCleaner::test_clean_invalid_record_no_type PASSED
tests/test_etl.py::TestCleaner::test_deduplicate PASSED
tests/test_etl.py::TestSeverity::test_tawuran_severity PASSED
tests/test_etl.py::TestSeverity::test_pkl_severity PASSED
tests/test_api.py::TestHealthEndpoint::test_health PASSED
tests/test_api.py::TestDashboardEndpoint::test_get_dashboard PASSED
tests/test_api.py::TestGeoJSONEndpoint::test_hotspots_geojson PASSED
```

### Manual API Testing

```bash
# 1. Health check
curl http://localhost:8000/health

# 2. Dashboard stats
curl http://localhost:8000/api/v1/dashboard | python -m json.tool

# 3. Daftar hotspot
curl http://localhost:8000/api/v1/hotspots

# 4. Detail hotspot ID 1
curl http://localhost:8000/api/v1/hotspots/1

# 5. GeoJSON hotspot
curl http://localhost:8000/api/v1/geojson/hotspots

# 6. Incidents dengan filter
curl "http://localhost:8000/api/v1/incidents?year=2024&district=JAKARTA+TIMUR"

# 7. Trigger ETL manual
curl -X POST http://localhost:8000/api/v1/etl/run \
  -H "Content-Type: application/json" \
  -d '{"source": "government", "year": 2024}'

# 8. Trigger DBSCAN manual
curl -X POST http://localhost:8000/api/v1/dbscan/run \
  -H "Content-Type: application/json" \
  -d '{"year": 2024}'
```

---

## Deployment Production

### Persiapan

1. **Ganti Secret Key** di `docker-compose.yml`:

   ```yaml
   SECRET_KEY: your-long-random-secret-key-minimum-32-chars
   ```

2. **Ganti password database**:

   ```yaml
   POSTGRES_PASSWORD: your-strong-database-password
   DATABASE_URL: postgresql://hotspot_user:your-strong-database-password@db:5432/hotspot_db
   ```

3. **Aktifkan HTTPS** — tambahkan sertifikat SSL ke Nginx config

4. **Batasi CORS** di `backend/app/main.py`:
   ```python
   allow_origins=["https://your-domain.com"]
   ```

### Build Production

```bash
# Build tanpa cache untuk memastikan versi terbaru
docker-compose build --no-cache

# Jalankan di background
docker-compose up -d

# Lihat logs
docker-compose logs -f backend
```

---

## Hasil Analisis

Data terkini dari sistem (per 14 Juli 2026):

| Metrik                         | Nilai     |
| ------------------------------ | --------- |
| Total Kejadian Terdata         | **3.252** |
| Total Hotspot Cluster          | **75**    |
| Cluster CRITICAL (score ≥ 100) | **1**     |
| Cluster HIGH (score 50–99)     | **6**     |
| Cluster MEDIUM (score 25–49)   | **24**    |
| Cluster LOW (score < 25)       | **45**    |

### Top 5 Hotspot Tertinggi

| Cluster | Kejadian | Jenis Dominan              | Risk Score | Level    |
| ------- | -------- | -------------------------- | ---------- | -------- |
| H-1     | 56       | PENYALAHGUNAAN FASUM/FASOS | 132        | CRITICAL |
| H-27    | 24       | PKL                        | 66         | HIGH     |
| H-2     | 26       | PENGEMIS                   | 64         | HIGH     |
| H-38    | 16       | TAWURAN (WARGA/PELAJAR)    | 60         | HIGH     |
| H-10    | 16       | PKL                        | 54         | HIGH     |

### Top 5 Wilayah Kejadian Terbanyak

| Wilayah                   | Jumlah Kejadian |
| ------------------------- | --------------- |
| Kota Adm. Jakarta Timur   | 880             |
| Kota Adm. Jakarta Pusat   | 712             |
| Kota Adm. Jakarta Selatan | 672             |
| Kota Adm. Jakarta Barat   | 544             |
| Kota Adm. Jakarta Utara   | 444             |

### Top 5 Jenis Kejadian

| Jenis                      | Jumlah |
| -------------------------- | ------ |
| PKL (Pedagang Kaki Lima)   | 1.228  |
| Penyalahgunaan FASUM/FASOS | 560    |
| Pak Ogah                   | 404    |
| Tawuran (Warga / Pelajar)  | 280    |
| Kriminalitas               | 160    |

---

## Troubleshooting

### Container tidak mau start

```bash
# Lihat logs semua container
docker-compose logs

# Lihat logs backend saja
docker-compose logs backend

# Lihat logs database
docker-compose logs db
```

### Database connection error

```bash
# Cek apakah db container healthy
docker ps

# Masuk ke container database
docker exec -it hotspot_db psql -U hotspot_user -d hotspot_db

# Cek tabel
\dt
\q
```

### Data tidak muncul di peta

```bash
# Cek apakah data sudah ada di database
curl http://localhost:8000/api/v1/dashboard

# Jika total_incidents = 0, jalankan ETL ulang
curl -X POST http://localhost:8000/api/v1/etl/run \
  -H "Content-Type: application/json" \
  -d '{"source": "government", "year": 2024}'

# Jika total_hotspots = 0, jalankan DBSCAN
curl -X POST http://localhost:8000/api/v1/dbscan/run \
  -H "Content-Type: application/json" \
  -d '{"year": 2024}'
```

### Port sudah terpakai

Edit `docker-compose.yml`, ubah port mapping:

```yaml
# Ganti port 80 ke port lain, misalnya 8080
nginx:
  ports:
    - "8080:80"
```

### Reset penuh (hapus semua data)

```bash
docker-compose down -v   # hapus container + volume database
docker-compose up --build
```

---

## Lisensi & Referensi

- **Dataset**: [Portal Satu Data Jakarta](https://data.jakarta.go.id) — Data Rawan Ketertiban Umum 2024
- **Geocoding**: [OpenStreetMap Nominatim](https://nominatim.openstreetmap.org)
- **Base Map**: © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright)
- **Algoritma**: Ester, M., et al. (1996). _A density-based algorithm for discovering clusters_. KDD-96.

---

_Dibuat untuk keperluan tugas akhir mata kuliah Sistem Informasi Geografis — Universitas Mercu Buana, Semester Genap 2025/2026._
