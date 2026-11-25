# Aplikasi Pengolah Inventaris (CLI)

Aplikasi command line berbasis **Python 3.8+** dan **standard library saja** (`argparse`, `csv`, `json`, `logging`). Tidak ada dependency eksternal, jadi tidak perlu `pip install`.

## 1. Deskripsi Masalah
- **Masalah:** pemilik toko kecil mencatat stok di spreadsheet, sulit mencari barang, memantau stok menipis, dan membuat rekap.
- **Tujuan:** mengolah file CSV stok menjadi informasi cepat lewat terminal.
- **Target pengguna:** pemilik/penjaga toko kecil dan mahasiswa yang belajar pengolahan data.
- **Format input:** CSV dengan kolom `kode,nama,kategori,stok,harga`.
- **Format output:** tabel teks di terminal dan (opsional) file JSON.
- **Fitur utama:** (1) `cari` barang, (2) `menipis` (stok di bawah batas), (3) `rekap` stok dan nilai per kategori.

## 2. Struktur Program
```
.
├── main.py                  # entry point CLI + penanganan error tingkat atas
├── data/
│   ├── input.csv            # contoh input (berisi data valid + data bermasalah)
│   ├── input_kosong.csv     # edge case: hanya header
│   ├── input_header_salah.csv  # skenario error: kolom wajib hilang
│   └── output_rekap.json    # contoh output
└── inventaris/              # package buatan sendiri
    ├── __init__.py
    ├── errors.py            # exception kustom
    ├── validator.py         # validasi header, baris, dan input pengguna
    ├── io_utils.py          # baca CSV, simpan JSON
    └── analisis.py          # duplikat, cari, filter, kelompok, rekap
```
**Alur dependensi:** `main.py` → `analisis`, `io_utils`, `validator`, `errors`; `io_utils` → `validator`, `errors`; `validator` → `errors`; `analisis` tidak bergantung module lain.

## 3. Struktur Data
| Struktur | Dipakai untuk | Alasan |
|---|---|---|
| `list` of `dict` | daftar barang | urutan terjaga, mudah diiterasi dan diurutkan, tiap barang punya field bernama |
| `dict` | pengelompokan per kategori dan hasil rekap | akses cepat berdasarkan kunci (kategori) |
| `set` | deteksi kode duplikat | pengecekan keanggotaan O(1) |

Comprehension yang dipakai: list comprehension (`cari`, `stok_menipis`) dan dict comprehension (`rekap`).

## 4. Cara Menjalankan
```bash
python main.py cari --kata pulpen
python main.py menipis --batas 10
python main.py rekap --output data/output_rekap.json
python main.py rekap --input data/input_kosong.csv        # edge case data kosong
python main.py rekap --input tidak_ada.csv                # error: file tidak ditemukan
```
Opsi `--input` (default `data/input.csv`) dan `--output` berlaku untuk semua perintah.

## 5. Penanganan Error
| Kondisi | Perilaku | Exit code |
|---|---|---|
| File tidak ditemukan | pesan error jelas | 2 |
| Header kurang kolom / batas stok bukan angka | `DataTidakValidError` | 3 |
| Baris stok/harga tidak valid, negatif, atau kosong | baris dilewati + warning, program lanjut | 0 |
| Kode duplikat | diabaikan (ambil yang pertama) + warning | 0 |
| Error tak terduga | traceback dicatat lewat `logging` | 1 |

## 6. Skenario Debugging
**Gejala:** saat menguji, perintah `python main.py rekap --output data/output_rekap.json` gagal dengan pesan `main.py: error: unrecognized arguments: --output data/output_rekap.json` (exit code 2), padahal opsi `--output` sudah didefinisikan.
**Penyebab:** `--input` dan `--output` awalnya didaftarkan pada parser utama, sehingga argparse hanya menerimanya *sebelum* sub-perintah (`python main.py --output x.json rekap`). Jika diletakkan setelah sub-perintah, opsi dianggap tidak dikenal oleh parser sub-perintah.
**Perbaikan:** opsi umum dipindah ke parser induk (`argparse.ArgumentParser(add_help=False)`) dan dipasang ke setiap sub-perintah lewat `parents=[umum]` di `buat_parser()`.
**Verifikasi:** jalankan ulang perintah yang sama; kini berhasil (exit code 0) dan `data/output_rekap.json` terbentuk. Opsi juga bisa diletakkan setelah sub-perintah mana pun.

## 7. Edge Case yang Diuji
- Data kosong (hanya header): rekap bernilai 0 tanpa error.
- Stok 0 dan stok menipis diurutkan benar.
- Baris stok `abc`, negatif, dan kode kosong di `input.csv` dilewati.

## 8. Sumber Referensi dan Bantuan AI
- Dokumentasi Python: argparse, csv, json, logging (docs.python.org).
- Kerangka dan kode awal dibantu Claude (Anthropic), lalu diuji dan disesuaikan sendiri. *(Sesuaikan catatan ini dengan kontribusimu.)*
