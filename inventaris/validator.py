"""Validasi header, baris data, dan input pengguna."""
from .errors import DataTidakValidError

KOLOM_WAJIB = ("kode", "nama", "kategori", "stok", "harga")


def validasi_header(nama_kolom):
    """Pastikan semua kolom wajib ada. Return None, lempar error bila kurang."""
    kurang = [k for k in KOLOM_WAJIB if k not in (nama_kolom or [])]
    if kurang:
        raise DataTidakValidError(f"Kolom wajib hilang: {', '.join(kurang)}")


def validasi_baris(baris, nomor):
    """Bersihkan dan validasi satu baris. Return dict baru yang bertipe benar."""
    kode = (baris.get("kode") or "").strip().upper()
    nama = (baris.get("nama") or "").strip()
    kategori = (baris.get("kategori") or "").strip().upper()
    if not kode or not nama or not kategori:
        raise DataTidakValidError(f"Baris {nomor}: kode/nama/kategori kosong")
    try:
        stok = int(baris["stok"])
        harga = float(baris["harga"])
    except (TypeError, ValueError):
        raise DataTidakValidError(
            f"Baris {nomor}: stok/harga bukan angka "
            f"(stok={baris.get('stok')!r}, harga={baris.get('harga')!r})"
        )
    if stok < 0 or harga < 0:
        raise DataTidakValidError(f"Baris {nomor}: stok/harga tidak boleh negatif")
    return {"kode": kode, "nama": nama, "kategori": kategori,
            "stok": stok, "harga": harga}


def validasi_batas(teks):
    """Ubah input batas stok menjadi int >= 0, atau lempar error."""
    try:
        nilai = int(teks)
    except (TypeError, ValueError):
        raise DataTidakValidError(f"Batas stok harus bilangan bulat: {teks!r}")
    if nilai < 0:
        raise DataTidakValidError("Batas stok tidak boleh negatif")
    return nilai
