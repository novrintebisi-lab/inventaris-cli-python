"""Fitur analisis: duplikat, pencarian, stok menipis, rekap per kategori."""


def hapus_duplikat(data):
    """Hapus baris dengan kode sama (ambil yang pertama) memakai set.

    Return (data_unik, daftar_kode_duplikat).
    """
    terlihat, unik, duplikat = set(), [], []
    for item in data:
        if item["kode"] in terlihat:
            duplikat.append(item["kode"])
        else:
            terlihat.add(item["kode"])
            unik.append(item)
    return unik, duplikat


def cari(data, kata):
    """Cari barang berdasarkan kata di nama atau kode (tidak peka huruf besar)."""
    kata = kata.strip().lower()
    return [b for b in data if kata in b["nama"].lower() or kata in b["kode"].lower()]


def stok_menipis(data, batas):
    """Barang dengan stok <= batas, diurutkan dari stok terkecil."""
    return sorted((b for b in data if b["stok"] <= batas), key=lambda b: b["stok"])


def kelompok_per_kategori(data):
    """Kelompokkan barang ke dict {kategori: [barang, ...]}."""
    hasil = {}
    for item in data:
        hasil.setdefault(item["kategori"], []).append(item)
    return hasil


def rekap(data):
    """Hitung rekap total dan per kategori. Aman untuk data kosong."""
    per_kategori = {
        kat: {
            "jumlah_jenis": len(items),
            "total_stok": sum(i["stok"] for i in items),
            "nilai_stok": sum(i["stok"] * i["harga"] for i in items),
        }
        for kat, items in kelompok_per_kategori(data).items()
    }
    return {
        "jumlah_jenis": len(data),
        "total_stok": sum(i["stok"] for i in data),
        "nilai_total": sum(i["stok"] * i["harga"] for i in data),
        "per_kategori": per_kategori,
    }
