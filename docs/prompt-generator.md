# Prompt Generator - VS Code AI Agent

## Tujuan

Gunakan dokumen berikut sebagai source of truth:

- SRS_V3_WebGIS_Ketertiban_Umum_Complete.md
- SRS_Frontend_UX_Ketertiban_Umum.md
- activity-diagram.md

Jika terjadi konflik spesifikasi:

1. SRS_V3_WebGIS_Ketertiban_Umum_Complete.md
2. SRS_Frontend_UX_Ketertiban_Umum.md
3. activity-diagram.md

---

# MASTER PROMPT

```text
ROLE

Anda adalah Senior GIS Engineer, Senior Backend Engineer, Senior Data Engineer, dan Senior Software Architect.

Bangun aplikasi production-ready berdasarkan seluruh dokumen pada folder docs.

Jangan membuat asumsi yang bertentangan dengan dokumen.

PROJECT

Web GIS Analisis Hotspot Kerawanan Ketertiban Umum DKI Jakarta.

OBJECTIVE

Membangun aplikasi yang mampu:

- Mengintegrasikan dataset pemerintah tahun 2024.
- Mengumpulkan data tahun 2025 dan 2026 melalui scraping.
- Melakukan geocoding otomatis.
- Menyimpan data pada PostgreSQL + PostGIS.
- Menjalankan clustering DBSCAN.
- Menghitung Risk Score.
- Menyediakan REST API.
- Menampilkan Web GIS interaktif menggunakan Leaflet.
- Menyediakan dashboard statistik.
- Menampilkan historical comparison per tahun.

TECH STACK

Backend:
- Python 3.12
- FastAPI
- SQLAlchemy
- GeoAlchemy2
- Alembic
- Pandas
- Scikit-Learn
- APScheduler

Database:
- PostgreSQL
- PostGIS

Frontend:
- React
- Vite
- TypeScript
- Leaflet.js
- Axios
- Bootstrap

Deployment:
- Docker
- Docker Compose
- Nginx

ARCHITECTURE

Gunakan Clean Architecture.

Buat folder structure yang rapi dan scalable.

DATABASE

Implementasikan tabel:

- users
- public_order_incidents
- hotspot_clusters
- scrape_logs

Gunakan geometry(Point,4326).

Tambahkan spatial index GIST.

ETL

Tahapan:

1. Extract
2. Cleaning
3. Deduplication
4. Geocoding
5. Validation
6. Load

Buat ETL modular.

SCRAPING

Implementasikan collector terpisah:

- government_collector
- news_collector

DBSCAN

Gunakan:

eps = 0.003
min_samples = 5

Output:

- cluster_id
- centroid
- radius
- risk_score

RISK SCORE

Severity:

Tawuran = 5
Kriminalitas Lingkungan = 4
Gangguan Ketertiban = 3
Pelanggaran Umum = 2
Keluhan = 1

Hitung total risk score untuk setiap hotspot.

API

Implementasikan:

GET /api/v1/dashboard
GET /api/v1/hotspots
GET /api/v1/hotspots/{id}
GET /api/v1/incidents/{id}
POST /api/v1/etl/run
POST /api/v1/dbscan/run

GEOJSON

Buat endpoint GeoJSON.

FRONTEND

Implementasikan:

- Dashboard Page
- GIS Map Page
- Admin Page
- Detail Hotspot Side Panel

LEAFLET FEATURES

- Marker Layer
- Hotspot Layer
- Heatmap Layer
- Administrative Boundary Layer
- Layer Control
- Fullscreen

USER INTERACTION

Hover Marker:

- jenis kejadian
- tanggal
- wilayah

Hover Hotspot:

- cluster id
- jumlah kejadian
- risk level
- jenis dominan

Klik Hotspot:

Tampilkan side panel:

- cluster id
- risk score
- risk level
- dominant incident
- radius
- timeline kejadian

FILTER

- Tahun
- Kota
- Kecamatan
- Kelurahan
- Jenis Kejadian
- Sumber Data

HISTORICAL COMPARISON

Tampilkan:

2024
2025
2026

serta tren kenaikan atau penurunan kejadian.

DOCKER

Buat:

- docker-compose.yml
- Dockerfile backend
- Dockerfile frontend
- nginx configuration

TESTING

Implementasikan:

- unit test
- integration test

README

Buat README lengkap.

OUTPUT

Kerjakan bertahap:

1. Folder Structure
2. Database Models
3. Alembic Migration
4. ETL Services
5. DBSCAN Service
6. API
7. React Frontend
8. Docker
9. Testing
10. README

Jika membuat file:

Selalu tampilkan:

1. Path file
2. Isi file lengkap

Jangan menggunakan mock implementation.

Buat kode yang dapat langsung dijalankan.
```

---

# REVIEW PROMPT

```text
Lakukan code review terhadap seluruh project.

Periksa:

- Bug
- Security issue
- Code smell
- Duplicated code
- Performance bottleneck
- GIS best practice
- Database optimization

Lakukan refactor langsung pada source code.

Jangan hanya membuat laporan.
```

---

# FINAL HARDENING PROMPT

```text
Optimalkan seluruh aplikasi untuk production.

Tambahkan:

- Swagger Documentation
- Spatial Index Optimization
- GeoJSON Validation
- Error Handling Global
- Logging
- Health Check Endpoint
- Database Connection Pool
- Pagination
- Docker Healthcheck
- Nginx Reverse Proxy

Update seluruh source code yang terdampak.
```
