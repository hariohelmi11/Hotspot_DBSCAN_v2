# SRS Addendum - Frontend UX/UI Specification
## Web GIS Analisis Hotspot Kerawanan Ketertiban Umum DKI Jakarta

### Dataset
- Data Rawan Ketertiban Umum Tahun 2024 (Satu Data Jakarta)
- Data Tahun 2025-2026 hasil ETL Web Scraping + Geocoding

---

# Tujuan Frontend

Menyediakan visualisasi spasial yang interaktif sehingga pengguna dapat:

- Mengidentifikasi hotspot kerawanan.
- Melihat tren kejadian berdasarkan tahun.
- Menelusuri riwayat kejadian dalam suatu hotspot.
- Membandingkan kerawanan antar wilayah.

---

# Layout Utama

```text
+----------------------------------------------------+
| Header                                             |
+----------------------------------------------------+
| Filter Panel                                       |
| Tahun | Wilayah | Jenis Kejadian | Sumber Data     |
+----------------------------------------------------+
|                                                    |
|                 Leaflet Map                        |
|                                                    |
+----------------------------------------------------+
| Dashboard Statistics                               |
+----------------------------------------------------+
```

---

# Layer GIS

Pengguna dapat mengaktifkan atau menonaktifkan layer:

- Incident Marker
- Heatmap Layer
- Hotspot Cluster Layer
- Administrative Boundary Layer

---

# Hover Marker

Saat mouse diarahkan ke marker:

```text
Tawuran

15 Januari 2025

Jakarta Barat
```

---

# Hover Hotspot

Saat mouse diarahkan ke hotspot:

```text
━━━━━━━━━━━━━━━━━━━
HOTSPOT H-12
━━━━━━━━━━━━━━━━━━━

48 Kejadian

Risk Level : HIGH

Jenis Dominan :
Tawuran
```

---

# Klik Hotspot

Menampilkan popup:

```text
HOTSPOT H-12

Jumlah Kejadian : 48

Risk Score : 125

Jenis Dominan :
Tawuran

Klik untuk detail →
```

---

# Side Panel Detail Hotspot

```text
HOTSPOT DETAIL

Cluster ID : H-12

Risk Level : HIGH

Risk Score : 125

Total Kejadian : 48

Jenis Dominan : Tawuran

Radius Cluster : 250 Meter

Periode Data : 2025
```

---

# Timeline Kejadian

```text
15 Jan 2025
Tawuran
Jl Mangga Besar

18 Jan 2025
Gangguan Ketertiban
Jl Hayam Wuruk

25 Jan 2025
Tawuran
Jl Gajah Mada
```

---

# Filter Tahun

```text
Semua Tahun
2024
2025
2026
```

Perilaku:

- 2024 → dataset pemerintah.
- 2025 → data hasil scraping.
- 2026 → data hasil scraping.
- Semua Tahun → seluruh data digabung.

---

# Filter Sumber Data

```text
☑ Pemerintah
☑ Scraping
```

Fitur ini memungkinkan pengguna membandingkan sumber data.

---

# Filter Wilayah

- Kota Administrasi
- Kecamatan
- Kelurahan

---

# Dashboard Statistik

## Card Summary

```text
Total Incident

Total Hotspot

High Risk Area

Critical Area
```

## Chart

- Tren Kejadian Tahunan
- Distribusi Jenis Kejadian
- Distribusi Risk Level
- Top 10 Wilayah Rawan

---

# Historical Comparison Feature

Ketika hotspot dipilih:

```text
HOTSPOT H-12

2024 : 12 Kejadian
2025 : 31 Kejadian
2026 : 48 Kejadian

Trend : Meningkat
```

Tujuan:

- Menampilkan perkembangan hotspot dari tahun ke tahun.
- Mendukung analisis temporal.

---

# Heatmap Feature

Layer heatmap digunakan untuk:

- Menampilkan kepadatan kejadian.
- Membantu identifikasi area rawan secara visual.

Plugin:

```text
Leaflet.heat
```

---

# User Experience Flow

```text
Pilih Tahun
      ↓
Pilih Wilayah
      ↓
Peta Diperbarui
      ↓
Hover Hotspot
      ↓
Klik Hotspot
      ↓
Lihat Detail
      ↓
Analisis Riwayat Kejadian
```
