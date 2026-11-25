"""Entry point CLI aplikasi inventaris.

Contoh:
    python main.py cari --kata pulpen
    python main.py menipis --batas 10
    python main.py rekap --output data/output_rekap.json
"""
import argparse
import logging
import sys

from inventaris import analisis, io_utils
from inventaris.errors import InventarisError
from inventaris.validator import validasi_batas

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("inventaris")


def buat_parser():
    """Bangun parser argumen CLI beserta sub-perintah."""
    umum = argparse.ArgumentParser(add_help=False)
    umum.add_argument("--input", default="data/input.csv", help="path file CSV input")
    umum.add_argument("--output", help="simpan hasil ke file JSON (opsional)")
    p = argparse.ArgumentParser(description="Pengolah data inventaris toko (CSV/JSON).")
    sub = p.add_subparsers(dest="perintah", required=True)
    c = sub.add_parser("cari", parents=[umum], help="cari barang berdasarkan nama/kode")
    c.add_argument("--kata", required=True)
    m = sub.add_parser("menipis", parents=[umum], help="tampilkan barang stok menipis")
    m.add_argument("--batas", default="10")
    sub.add_parser("rekap", parents=[umum], help="rekap stok per kategori")
    return p


def cetak_tabel(items):
    """Cetak daftar barang dalam bentuk tabel teks."""
    if not items:
        print("(tidak ada data)")
        return
    print(f"{'KODE':<8}{'NAMA':<22}{'KATEGORI':<14}{'STOK':>6}{'HARGA':>12}")
    for b in items:
        print(f"{b['kode']:<8}{b['nama']:<22}{b['kategori']:<14}{b['stok']:>6}{b['harga']:>12,.0f}")


def jalankan(args):
    """Jalankan perintah terpilih. Return hasil (untuk disimpan ke JSON)."""
    data, galat = io_utils.baca_csv(args.input)
    for pesan in galat:
        log.warning("Dilewati -> %s", pesan)
    data, duplikat = analisis.hapus_duplikat(data)
    if duplikat:
        log.warning("Kode duplikat diabaikan: %s", ", ".join(duplikat))
    log.info("%d barang valid dimuat.", len(data))

    if args.perintah == "cari":
        hasil = analisis.cari(data, args.kata)
        cetak_tabel(hasil)
    elif args.perintah == "menipis":
        hasil = analisis.stok_menipis(data, validasi_batas(args.batas))
        cetak_tabel(hasil)
    else:
        hasil = analisis.rekap(data)
        print(f"Jenis barang : {hasil['jumlah_jenis']}")
        print(f"Total stok   : {hasil['total_stok']}")
        print(f"Nilai total  : Rp {hasil['nilai_total']:,.0f}")
        for kat, r in hasil["per_kategori"].items():
            print(f"  - {kat:<12} {r['jumlah_jenis']} jenis, stok {r['total_stok']}, Rp {r['nilai_stok']:,.0f}")
    return hasil


def main():
    """Fungsi utama dengan penanganan error tingkat atas."""
    args = buat_parser().parse_args()
    try:
        hasil = jalankan(args)
        if args.output:
            io_utils.simpan_json(hasil, args.output)
            log.info("Hasil disimpan ke %s", args.output)
    except FileNotFoundError:
        log.error("File tidak ditemukan: %s", args.input)
        return 2
    except InventarisError as e:
        log.error("Data tidak valid: %s", e)
        return 3
    except Exception:
        log.exception("Kesalahan tak terduga")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
