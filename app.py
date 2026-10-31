"""Layer View: mengurus tampilan Streamlit dan merangkai semua layer."""

import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.model import Base
from repositories.repository import MahasiswaRepository
from services.service import PrediksiService


def inisialisasi_database():
    """Membuat engine, tabel, dan sesi database satu kali saja."""
    load_dotenv()
    alamat_database = os.getenv("DATABASE_URL", "sqlite:///data_prediksi.db")
    engine = create_engine(alamat_database, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    pembuat_sesi = sessionmaker(bind=engine)
    return pembuat_sesi()


@st.cache_resource
def ambil_sesi_database():
    """Streamlit menyimpan sesi database agar tidak dibuat ulang tiap klik."""
    return inisialisasi_database()


def tampilkan_form_input():
    """Menampilkan form input dan mengembalikan nilainya saat tombol ditekan."""
    with st.form("form_input"):
        nama = st.text_input("Nama Mahasiswa")
        ipk = st.number_input("IPK (0.0 - 4.0)", min_value=0.0, max_value=4.0, step=0.01)
        sks = st.number_input("Total SKS", min_value=0, step=1)
        tombol_proses = st.form_submit_button("Prediksi & Simpan")

    return nama, ipk, int(sks), tombol_proses


def proses_prediksi(nama: str, ipk: float, sks: int) -> None:
    """Meminta status ke service, menyimpan lewat repository, lalu memberi umpan balik."""
    hasil_status = service.tentukan_kelulusan(ipk, sks)
    repo.simpan_data(nama, ipk, sks, hasil_status)

    if hasil_status == "Lulus Tepat Waktu":
        st.success(f"**{nama}** dinyatakan **{hasil_status}**!")
    else:
        st.error(f"**{nama}** dinyatakan **{hasil_status}**.")

    st.toast("Data berhasil disimpan!")


def tampilkan_riwayat():
    """Menampilkan seluruh data yang tersimpan di database sebagai tabel."""
    st.divider()
    st.subheader("Riwayat Prediksi")

    data_database = repo.ambil_semua_data()

    if not data_database:
        st.info("Belum ada data. Silakan isi form di atas.")
        return

    semua_data = [
        {
            "Nama": data.nama,
            "IPK": data.ipk,
            "SKS": data.sks,
            "Status": data.status_kelulusan,
        }
        for data in data_database
    ]
    st.dataframe(pd.DataFrame(semua_data), width="stretch")
    st.caption(f"Total data tersimpan: {len(semua_data)}")


# 1. Konfigurasi halaman
st.set_page_config(page_title="Sistem Prediksi Kelulusan", layout="centered")

# 2. Merangkai dependency (dependency injection)
db_session = ambil_sesi_database()
repo = MahasiswaRepository(db_session)
service = PrediksiService()

# 3. Membangun UI
st.title("Sistem Prediksi Kelulusan")
st.caption("Masukkan data mahasiswa, sistem akan memprediksi status kelulusannya.")

nama_mahasiswa, ipk_mahasiswa, sks_mahasiswa, tombol_proses = tampilkan_form_input()

if tombol_proses:
    if not nama_mahasiswa.strip():
        st.warning("Nama tidak boleh kosong!")
    else:
        proses_prediksi(nama_mahasiswa.strip(), ipk_mahasiswa, sks_mahasiswa)

# 4. Menampilkan riwayat data
tampilkan_riwayat()
