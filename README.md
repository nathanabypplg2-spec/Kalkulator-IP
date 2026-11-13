# Kalkulator Subnet & VLSM

Aplikasi pembelajaran subnet IPv4 dan alokasi VLSM berbasis FastAPI.

## Menjalankan aplikasi

```powershell
uv sync --dev
uv run fastapi dev main.py
```

Buka `http://127.0.0.1:8000`.

## Menjalankan test

```powershell
uv run pytest
```

Spesifikasi kebutuhan dan perilaku aplikasi ada di [SPEC.md](SPEC.md).

## Docker

Bangun image dan jalankan container secara lokal:

```powershell
docker build -t subnet-calculator .
docker run -d --name subnet-app -p 8080:8000 subnet-calculator
```

Buka `http://127.0.0.1:8080/`. Angka pertama pada `-p 8080:8000` adalah port di komputer Anda dan bisa diganti, misalnya `-p 5000:8000` untuk membuka `http://127.0.0.1:5000/`. Angka kedua `8000` adalah port aplikasi di dalam container.

Jalankan smoke test terhadap container:

```powershell
uv run python scripts/smoke_test.py http://127.0.0.1:8080
```

Setelah selesai, hentikan dan hapus container dengan `docker rm -f subnet-app`.

## Deploy ke Vercel

Proyek FastAPI ini menggunakan `main.py` dengan objek `app`, yang dapat dideteksi Vercel. Hubungkan repository GitHub ini dari dashboard Vercel satu kali:

1. Masuk ke Vercel dan pilih **Add New → Project**.
2. Hubungkan akun GitHub jika diminta, lalu impor `nathanabypplg2-spec/Kalkulator-IP`.
3. Biarkan **Framework Preset** terdeteksi otomatis dan **Root Directory** tetap `./`.
4. Pilih **Deploy**. Setelah deploy selesai, Vercel memberikan URL publik.

Sesudah integrasi dibuat, setiap push ke branch `main` memulai deployment Vercel baru. Untuk deploy preview dari perubahan, buat branch lain dan push ke GitHub.

## Alur perubahan, rebuild Docker, dan push GitHub

Jalankan PowerShell dari folder proyek setelah mengedit dan menyimpan file. Ubah pesan commit sesuai pekerjaan Anda.

```powershell
# 1. Pastikan berada di folder proyek
cd "D:\Projects PKL\Tugas Sekolah\Kalkulator IP"

# 2. Bangun ulang image Docker (titik di akhir wajib: folder saat ini)
docker build -t subnet-calculator .

# 3. Ganti container lama dengan image terbaru
docker rm -f subnet-app
docker run -d --name subnet-app -p 8080:8000 subnet-calculator

# 4. Buka http://127.0.0.1:8080/ dan periksa perubahan

# 5. Commit dan kirim kode ke GitHub
git add .
git commit -m "Jelaskan perubahan di sini"
git push origin main
```

Perintah build Docker dan Git adalah dua hal terpisah: build memperbarui aplikasi yang berjalan di komputer lokal; `git push` mengirim kode ke GitHub dan, setelah Vercel terhubung ke repository, memicu deployment cloud. Jika `git commit` menampilkan `nothing to commit`, tidak ada perubahan kode tersimpan untuk dikirim. Jika container `subnet-app` belum ada dan `docker rm -f` melaporkan container tidak ditemukan, lanjutkan dengan perintah `docker run`.

# Kalkulator-IP
