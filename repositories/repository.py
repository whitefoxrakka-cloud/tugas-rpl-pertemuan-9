"""Layer Repository: hanya mengurus simpan dan ambil data dari database."""

from sqlalchemy.orm import Session

from models.model import Mahasiswa


class MahasiswaRepository:
    """Pintu masuk tunggal untuk operasi database tabel mahasiswa."""

    def __init__(self, db_session: Session):
        self.db = db_session

    def simpan_data(self, nama: str, ipk: float, sks: int, status: str) -> Mahasiswa:
        """Menyimpan satu baris data prediksi lalu mengembalikan objeknya."""
        data_baru = Mahasiswa(nama=nama, ipk=ipk, sks=sks, status_kelulusan=status)
        self.db.add(data_baru)
        self.db.commit()
        self.db.refresh(data_baru)
        return data_baru

    def ambil_semua_data(self) -> list[Mahasiswa]:
        """Mengambil seluruh riwayat prediksi, data terbaru di urutan teratas."""
        return self.db.query(Mahasiswa).order_by(Mahasiswa.id.desc()).all()
