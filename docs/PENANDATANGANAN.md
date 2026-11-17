# Tanda tangan aplikasi (signing) Corvus Academy

Android hanya mau memperbarui aplikasi bila APK baru ditandatangani dengan
kunci yang sama dengan APK lama. Karena itu kunci harus dibuat **sekali**,
disimpan aman, lalu dipakai terus oleh setiap build.

Workflow `build.yml` sudah siap membaca kunci dari GitHub Secrets. Tinggal
membuat kunci dan mengisi tiga secret.

## Ringkasan

1. Buat keystore (`.jks`) di komputer Anda.
2. Cadangkan keystore dan kata sandinya di dua tempat berbeda.
3. Ubah keystore menjadi teks base64.
4. Isi tiga secret di repo `efendiyhy/corvus-apk`.
5. Rilis versi baru, lalu cek sidik jari kuncinya.

## 1. Buat keystore

Perlu JDK (perintah `keytool`). Cek dengan `keytool -help`.

Jalankan sebagai **satu baris** (berlaku di Windows PowerShell, Linux, dan macOS):

```
keytool -genkeypair -v -keystore corvus-release.jks -alias corvus -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=Corvus Academy, O=EK-Instrumentation, C=ID"
```

Perintah akan meminta kata sandi keystore dan kata sandi kunci. Pakai
**kata sandi yang sama** untuk keduanya, panjang dan acak (workflow memakai
satu kata sandi untuk dua keperluan itu). Masa berlaku 10.000 hari sekitar
27 tahun, cukup untuk Play Store.

Catat tiga hal ini:

| Data | Isi |
|------|-----|
| Nama file | `corvus-release.jks` |
| Alias | `corvus` |
| Kata sandi | yang Anda ketik tadi |

## 2. Simpan dengan aman

Kehilangan keystore atau kata sandinya berarti aplikasi tidak bisa lagi
diperbarui. Pengguna harus menghapus aplikasi lama dan memasang ulang.

- Simpan `corvus-release.jks` di minimal dua tempat terpisah, misalnya
  password manager dan flash disk.
- Simpan kata sandi di password manager, terpisah dari file keystore.
- **Jangan pernah** meng-commit `.jks` atau kata sandi ke repo. Repo ini
  publik.

## 3. Ubah keystore menjadi base64

GitHub Secrets hanya menyimpan teks, jadi file diubah dulu.

Linux atau macOS:

```bash
base64 -w0 corvus-release.jks > corvus-release.b64   # macOS: base64 -i corvus-release.jks
```

Windows PowerShell:

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("corvus-release.jks")) | Set-Content corvus-release.b64
```

Isi file `corvus-release.b64` adalah satu baris panjang. Hapus file ini
setelah dipakai.

## 4. Isi GitHub Secrets

Buka https://github.com/efendiyhy/corvus-apk/settings/secrets/actions lalu
pilih **New repository secret**. Buat tiga secret berikut, nama harus persis:

| Nama secret | Isi |
|-------------|-----|
| `ANDROID_KEYSTORE_BASE64` | seluruh isi `corvus-release.b64` |
| `ANDROID_KEYSTORE_PASSWORD` | kata sandi keystore |
| `ANDROID_KEY_ALIAS` | `corvus` |

Atau dengan GitHub CLI:

```bash
gh secret set ANDROID_KEYSTORE_BASE64   -R efendiyhy/corvus-apk < corvus-release.b64
gh secret set ANDROID_KEYSTORE_PASSWORD -R efendiyhy/corvus-apk
gh secret set ANDROID_KEY_ALIAS         -R efendiyhy/corvus-apk --body corvus
```

## 5. Rilis dan verifikasi

1. Naikkan angka di file `VERSION` (misalnya `1.1.2`) dan tambahkan catatan
   di `CHANGELOG.md`.
2. Push ke `main`. Workflow berjalan dan membuat rilis.
3. Di log langkah "Siapkan kunci penanda tangan" harus muncul
   `Memakai kunci tetap dari GitHub Secrets.` Bila muncul peringatan kuning,
   berarti secret belum terbaca.
4. Unduh APK hasil rilis, lalu cek sidik jarinya:

```bash
apksigner verify --print-certs corvus-academy.apk
```

Catat nilai `SHA-256 digest` sertifikat. Pada rilis berikutnya nilainya harus
**sama persis**. Bila berbeda, kunci yang dipakai bukan kunci tetap.

## Catatan penting

- **Satu kali hapus aplikasi.** APK lama (v1.1.1 dan sebelumnya) ditandatangani
  kunci sekali pakai. Pengguna perlu menghapusnya sekali, lalu memasang rilis
  pertama yang memakai kunci tetap. Setelah itu semua pembaruan berjalan
  mulus.
- **Play Store.** Bila nanti mengunggah ke Play Store, aktifkan Play App
  Signing. Keystore ini menjadi *upload key*, dan Google menyimpan kunci
  penanda tangan utama. Itu menjaga aplikasi tetap aman bila keystore hilang.
- **Ganti kata sandi.** `keytool -storepasswd -keystore corvus-release.jks`
  lalu perbarui secret `ANDROID_KEYSTORE_PASSWORD`. Ubah kata sandi kunci
  dengan `-keypasswd` agar tetap sama dengan kata sandi keystore.

## Masalah umum

| Gejala | Penyebab | Perbaikan |
|--------|----------|-----------|
| Peringatan "Secrets ... belum diisi" | Nama secret salah atau kosong | Cek tiga nama secret, huruf besar semua |
| `Keystore was tampered with` | Kata sandi salah | Perbarui `ANDROID_KEYSTORE_PASSWORD` |
| `Cannot recover key` | Kata sandi kunci berbeda dari kata sandi keystore | Samakan dengan `-keypasswd` |
| Android menolak memperbarui: "paket bertentangan" | Kunci berbeda dari APK terpasang | Hapus aplikasi lama sekali, pasang ulang |
