# Praktikum RPL 9 - Sistem Prediksi Kelulusan

Aplikasi contoh penerapan arsitektur berlapis (Layered Architecture), prinsip SOLID
(Single Responsibility Principle), dan Clean Code memakai Streamlit, SQLAlchemy, dan SQLite.

## Struktur Proyek

```
Praktikum_RPL_9/
├── app.py                       # View layer: tampilan Streamlit dan perangkaian komponen
├── models/
│   └── model.py                 # Model layer: struktur tabel database
├── repositories/
│   └── repository.py            # Repository layer: simpan dan ambil data
├── services/
│   └── service.py               # Service layer: logika bisnis kelulusan
├── uji/
│   ├── uji_aplikasi.py          # Uji otomatis memakai streamlit.testing
│   └── ambil_tangkapan_layar.py # Uji lewat browser dan tangkapan layar
├── mockup/
│   └── mockup_ui.html           # Sumber rancangan antarmuka
├── gambar/
│   ├── mockup_ui.png            # Gambar mockup UI
│   └── aplikasi_berjalan.png    # Bukti aplikasi berjalan
├── .env                         # Alamat database lokal
├── requirements.txt
└── README.md
```

## Pembagian Tanggung Jawab (SRP)

| Layer | Berkas | Tanggung jawab | Tidak boleh tahu soal |
|---|---|---|---|
| Model | `models/model.py` | Struktur tabel `mahasiswa` | Tampilan, aturan kelulusan |
| Repository | `repositories/repository.py` | Query simpan dan ambil data | Tampilan, aturan kelulusan |
| Service | `services/service.py` | Aturan IPK >= 3.0 dan SKS >= 140 | Database, tampilan |
| View | `app.py` | Form, tabel riwayat, perangkaian dependency | Query database langsung |

## Cara Menjalankan

```powershell
cd "D:\tugas baru yang harus di kerjakan\RPL\tugas baru\Praktikum_RPL_9"
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

Bila memakai Python lain, pasang dulu paketnya:

```powershell
pip install -r requirements.txt
```

Aplikasi terbuka di `http://localhost:8501`. Isi form lalu tekan **Prediksi & Simpan**.
Data tersimpan pada `data_prediksi.db` di folder proyek.

## Pengujian yang Sudah Dijalankan

1. Uji otomatis antarmuka memakai `streamlit.testing`:

   ```powershell
   .\.venv\Scripts\python.exe uji\uji_aplikasi.py
   ```

   Hasil: tiga pengujian lulus (nama kosong ditolak, prediksi lulus tersimpan,
   prediksi tidak lulus tampil).

2. Uji lewat browser sungguhan (Playwright memakai Chrome terpasang) sekaligus
   mengambil gambar `gambar/aplikasi_berjalan.png`.

## Bukti untuk Lembar Evaluasi

| No | Aspek | Bukti |
|---|---|---|
| 1 | Mockup | `gambar/mockup_ui.png` dan `mockup/mockup_ui.html` |
| 2 | SOLID (SRP) | Empat berkas terpisah: `model.py`, `repository.py`, `service.py`, `app.py` |
| 3 | Clean Code (Penamaan) | `nama_mahasiswa`, `ipk_mahasiswa`, `sks_mahasiswa`, `data_database`, `hasil_status` |
| 4 | Clean Code (Fungsi) | `tampilkan_form_input`, `proses_prediksi`, `tampilkan_riwayat`, `tentukan_kelulusan` |
| 5 | Integrasi UI | `gambar/aplikasi_berjalan.png`: form, pesan status, tabel riwayat dari SQLite |

## Catatan Teknis

- Versi paket yang dipakai saat pengujian: Streamlit 1.66.1, SQLAlchemy 2.1.6,
  pandas 3.1.0, python-dotenv 1.2.4, Python 3.14.5.
- `check_same_thread=False` dipakai karena Streamlit menjalankan skrip di thread berbeda.
- Konstanta batas kelulusan disimpan sebagai atribut kelas `PrediksiService`
  agar tidak ada angka ajaib di dalam fungsi.
