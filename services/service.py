"""Layer Service: hanya mengurus logika bisnis penentuan kelulusan."""


class PrediksiService:
    """Aturan kelulusan mahasiswa, tanpa campur tangan database atau tampilan."""

    BATAS_IPK_MINIMAL = 3.0
    BATAS_SKS_MINIMAL = 140

    def tentukan_kelulusan(self, ipk: float, sks: int) -> str:
        """Mengembalikan status kelulusan berdasarkan IPK dan total SKS."""
        lulus_ipk = ipk >= self.BATAS_IPK_MINIMAL
        lulus_sks = sks >= self.BATAS_SKS_MINIMAL

        if lulus_ipk and lulus_sks:
            return "Lulus Tepat Waktu"

        return "Tidak Lulus"
