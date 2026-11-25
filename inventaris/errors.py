"""Exception buatan sendiri agar penanganan error lebih spesifik."""


class InventarisError(Exception):
    """Kelas dasar semua error aplikasi inventaris."""


class DataTidakValidError(InventarisError):
    """Dilempar saat format atau isi data tidak sesuai aturan."""
