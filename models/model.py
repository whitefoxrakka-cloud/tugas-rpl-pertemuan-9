"""Layer Model: hanya mengurus struktur tabel database."""

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Mahasiswa(Base):
    """Tabel mahasiswa berisi data input dan hasil prediksi kelulusan."""

    __tablename__ = "mahasiswa"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    ipk = Column(Float, nullable=False)
    sks = Column(Integer, nullable=False)
    status_kelulusan = Column(String, nullable=False)
