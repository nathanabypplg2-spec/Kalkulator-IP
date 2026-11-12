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
docker run -d --name subnet-app -p 8000:8000 subnet-calculator
```

Jalankan smoke test terhadap container:

```powershell
uv run python scripts/smoke_test.py http://127.0.0.1:8000
```

Setelah selesai, hentikan dan hapus container dengan `docker rm -f subnet-app`.

# Kalkulator-IP
