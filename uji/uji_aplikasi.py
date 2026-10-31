"""Uji otomatis aplikasi memakai streamlit.testing (tanpa membuka browser)."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

BERKAS_APLIKASI = str(Path(__file__).resolve().parent.parent / "app.py")


def uji_nama_kosong():
    """Nama kosong harus ditolak dengan peringatan, bukan disimpan."""
    aplikasi = AppTest.from_file(BERKAS_APLIKASI, default_timeout=30).run()
    aplikasi.text_input[0].set_value("   ")
    aplikasi.button[0].click().run()

    assert len(aplikasi.warning) == 1, "Peringatan nama kosong tidak muncul"
    print("LULUS uji nama kosong: peringatan tampil, data tidak disimpan")


def uji_prediksi_dan_simpan():
    """Input valid harus menghasilkan status dari service dan tersimpan ke tabel."""
    aplikasi = AppTest.from_file(BERKAS_APLIKASI, default_timeout=30).run()
    aplikasi.text_input[0].set_value("Hasan")
    aplikasi.number_input[0].set_value(3.45)
    aplikasi.number_input[1].set_value(148)
    aplikasi.button[0].click().run()

    assert len(aplikasi.success) == 1, "Pesan sukses tidak muncul"
    assert "Lulus Tepat Waktu" in aplikasi.success[0].value
    assert len(aplikasi.dataframe) == 1, "Tabel riwayat tidak muncul"

    tabel = aplikasi.dataframe[0].value
    assert "Hasan" in tabel["Nama"].tolist(), "Data baru tidak ada di tabel"
    print("LULUS uji prediksi lulus:", aplikasi.success[0].value)
    print(tabel.to_string(index=False))


def uji_tidak_lulus():
    """Nilai di bawah batas harus menghasilkan status Tidak Lulus."""
    aplikasi = AppTest.from_file(BERKAS_APLIKASI, default_timeout=30).run()
    aplikasi.text_input[0].set_value("Siti")
    aplikasi.number_input[0].set_value(2.85)
    aplikasi.number_input[1].set_value(132)
    aplikasi.button[0].click().run()

    assert len(aplikasi.error) == 1, "Pesan error tidak muncul"
    assert "Tidak Lulus" in aplikasi.error[0].value
    print("LULUS uji prediksi tidak lulus:", aplikasi.error[0].value)


if __name__ == "__main__":
    uji_nama_kosong()
    uji_prediksi_dan_simpan()
    uji_tidak_lulus()
    print("Semua pengujian selesai tanpa kegagalan.")
