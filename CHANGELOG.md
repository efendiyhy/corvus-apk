# Catatan Perubahan

Format mengikuti [Keep a Changelog](https://keepachangelog.com/id-ID/1.1.0/) dan penomoran [Semantic Versioning](https://semver.org/lang/id/).
Isi bagian versi terbaru di bawah ini dipakai otomatis sebagai keterangan rilis.

## [1.2.0] - 2026-11-17

### Diubah
- Aplikasi kini ditandatangani dengan kunci tetap. Pembaruan berikutnya dapat dipasang langsung di atas versi ini tanpa menghapus aplikasi.
- Pengguna versi 1.1.1 atau lebih lama perlu menghapus aplikasi lama sekali, lalu memasang versi ini.

## [1.1.1] - 2026-11-18

### Diperbaiki
- Tombol Kembali Android (termasuk gestur geser dari tepi kiri) tidak lagi menutup aplikasi. Kini naik satu level ke menu sebelumnya, menutup dialog yang terbuka lebih dulu, dan dari menu utama meminta tekan dua kali untuk keluar.

### Diubah
- Menambahkan plugin native `@capacitor/app` untuk menangani tombol Kembali.

## [1.1.0] - 2026-11-17

### Ditambahkan
- Layar pembuka dengan logo dan nama aplikasi: **Corvus Academy by EK Instrumentation**.
- Pemberitahuan pembaruan di dalam aplikasi: banner "Versi baru tersedia" dengan tombol Perbarui.
- Akun massal, grup sekolah, kartu ujian, dan sertifikat nilai PDF tersedia melalui situs yang dibungkus aplikasi.

### Diperbaiki
- Tombol Kembali di Whiteboard dan halaman Kunci kini kembali ke menu utama, tidak lagi menutup aplikasi.

### Catatan pemasangan
- Versi sebelum 1.1.0 menggunakan kunci tanda tangan yang berbeda. Hapus aplikasi lama sekali, lalu pasang versi ini. Pembaruan berikutnya dapat dipasang langsung di atasnya.

## [1.0.4] - 2026-11-17
### Ditambahkan
- Tautan unduhan APK dan pemberitahuan versi dasar.

## [1.0.2] - 2026-11-17
### Ditambahkan
- Rilis APK pertama: pembungkus native situs Corvus Academy, tema ungu, ikon dan splash baru.
