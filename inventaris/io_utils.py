"""Baca/tulis file CSV dan JSON."""
import csv
import json
from .errors import DataTidakValidError
from .validator import validasi_header, validasi_baris


def baca_csv(path):
    """Baca CSV inventaris.

    Return (data_valid, daftar_pesan_error). Baris yang tidak valid dilewati
    dan dicatat; FileNotFoundError dan error header dibiarkan naik ke pemanggil.
    """
    data, galat = [], []
    with open(path, newline="", encoding="utf-8") as f:
        pembaca = csv.DictReader(f)
        validasi_header(pembaca.fieldnames)
        for nomor, baris in enumerate(pembaca, start=2):  # baris 1 = header
            try:
                data.append(validasi_baris(baris, nomor))
            except DataTidakValidError as e:
                galat.append(str(e))
    return data, galat


def simpan_json(isi, path):
    """Simpan dict/list ke file JSON dengan format rapi."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(isi, f, indent=2, ensure_ascii=False)
