"""Mengambil tangkapan layar aplikasi Streamlit yang sedang berjalan."""

from playwright.sync_api import sync_playwright


def ambil_tangkapan_layar(alamat: str, berkas_keluaran: str) -> None:
    with sync_playwright() as pemutar:
        peramban = pemutar.chromium.launch(channel="chrome", headless=True)
        halaman = peramban.new_page(viewport={"width": 1100, "height": 1250})
        halaman.goto(alamat, wait_until="networkidle", timeout=60000)
        halaman.wait_for_selector("text=Sistem Prediksi Kelulusan", timeout=60000)
        halaman.wait_for_timeout(2500)
        halaman.screenshot(path=berkas_keluaran, full_page=True)
        peramban.close()
    print("Tangkapan layar disimpan:", berkas_keluaran)


def uji_lewat_browser(alamat: str, berkas_keluaran: str) -> None:
    """Mengisi form dua kali, menekan tombol, lalu memotret hasilnya."""
    with sync_playwright() as pemutar:
        peramban = pemutar.chromium.launch(channel="chrome", headless=True)
        halaman = peramban.new_page(viewport={"width": 1100, "height": 1250})
        halaman.goto(alamat, wait_until="networkidle", timeout=60000)
        halaman.wait_for_selector("text=Sistem Prediksi Kelulusan", timeout=60000)

        halaman.get_by_label("Nama Mahasiswa").fill("Budi Santoso")
        halaman.get_by_label("IPK (0.0 - 4.0)").fill("3.72")
        halaman.get_by_label("Total SKS").fill("152")
        halaman.get_by_role("button", name="Prediksi & Simpan").click()
        halaman.wait_for_selector("text=dinyatakan", timeout=60000)
        halaman.wait_for_timeout(1500)

        halaman.get_by_label("Nama Mahasiswa").fill("Siti Aminah")
        halaman.get_by_label("IPK (0.0 - 4.0)").fill("2.85")
        halaman.get_by_label("Total SKS").fill("132")
        halaman.get_by_role("button", name="Prediksi & Simpan").click()
        halaman.wait_for_selector("text=dinyatakan", timeout=60000)
        halaman.wait_for_timeout(2500)
        halaman.screenshot(path=berkas_keluaran, full_page=True)
        print("Tangkapan layar interaksi disimpan:", berkas_keluaran)
        peramban.close()


if __name__ == "__main__":
    uji_lewat_browser("http://127.0.0.1:8501", "gambar/aplikasi_berjalan.png")
