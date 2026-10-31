"""Memeriksa isi database SQLite secara langsung."""

import sqlite3

koneksi = sqlite3.connect("data_prediksi.db")
baris = koneksi.execute(
    "SELECT id, nama, ipk, sks, status_kelulusan FROM mahasiswa ORDER BY id"
).fetchall()

for data in baris:
    print(data)

print("Jumlah baris:", len(baris))
