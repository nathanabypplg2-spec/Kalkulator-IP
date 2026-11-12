# PROMPT-INTEGRATE

Demo Vibe Engineering: Kalkulator Subnet & VLSM

## Babak 1: Vibe coding (±20 menit)

Tool: ANTIGRAVITY

```text
Bikinin kalkulator subnet berbasis web. Input IP dan prefix, tampilkan
network address, broadcast address, range host, dan jumlah host.
```

## Tahap 0: Scaffold proyek (tanpa CI)

Tool: ANTIGRAVITY

```text
Di folder ini: inisialisasi git dengan branch main, jalankan `uv init
--python 3.12`, tambahkan dependency `fastapi[standard]` serta dev
dependency pytest, pytest-cov, httpx dengan `uv add`. Buat `.gitignore`
untuk Python (.venv, __pycache__, .pytest_cache, .coverage, htmlcov,
.env). JANGAN membuat folder .github atau workflow CI. Commit dengan
pesan "chore: scaffold awal tanpa CI", lalu buat repo GitHub publik
bernama "subnet-calculator-sqa" dan push branch main ke sana dengan `gh`.
```

## Tahap 1: Memahami masalah

Tool: GEMINI

```text
[P] Persona: Bertindaklah sebagai guru senior TKJ yang mengajar
subnetting dan penguji perangkat lunak.

[K] Konteks: Kita akan membuat kalkulator subnet dan VLSM berbasis web
untuk guru SMK TKJ. Input: alamat IPv4 dan prefix. Output: network
address, broadcast address, range host, dan jumlah host, plus mode VLSM.
Kebenaran hasilnya harus bisa dinilai guru tanpa membaca kode.

[T] Tugas: Bantu saya mendaftar kasus uji dan kasus tepi (edge case)
yang harus ditangani, baik untuk perhitungan subnet maupun VLSM. Untuk
tiap kasus, tandai apakah jawabannya pasti (bisa dijadikan test) atau
perlu keputusan manusia (misalnya aturan /31 dan /32). JANGAN menulis
kode apa pun.

[F] Format: Tabel dengan kolom: kasus, input, hasil yang diharapkan,
dan status (pasti / perlu keputusan).
```

## Tahap 2: Spesifikasi (SPEC.md)

Tool: GEMINI, MANUSIA

```text
[P] Persona: Bertindaklah sebagai Solutions Architect dan penulis
spesifikasi teknis yang teliti.

[K] Konteks: Lanjutkan dari daftar kasus uji pada percakapan ini.
Aplikasi: Kalkulator Subnet & VLSM berbasis web, dengan backend
Python 3.12 + FastAPI dan satu halaman HTML. Logika perhitungan berada
di `main.py`; test berada di `test_main.py` (pytest).

[T] Tugas: Tulis dokumen SPEC.md (JANGAN menulis kode aplikasi) yang
memuat keputusan berikut:

1. `hitung_subnet(ip: str, prefix: int) -> dict` dengan kunci:
   mask, network, broadcast, first_host, last_host, usable_hosts.
   - IP valid: tepat 4 oktet, tiap oktet 0-255, tanpa angka nol di
     depan (192.168.01.1 ditolak), tanpa spasi.
   - Prefix valid: bilangan bulat 0-32.
   - Input tidak valid: raise ValueError.
   - Jumlah host: 2^(32-prefix) - 2 untuk prefix 0-30.
   - /31: aturan point-to-point RFC 3021, 2 host, broadcast = None.
   - /32: 1 host, broadcast = None, first_host = last_host = IP itu.
   - network = IP AND subnet mask (hitung secara bitwise).
2. `alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) ->
   list[dict]`
   - Urutkan kebutuhan dari yang terbesar, alokasikan berurutan mulai
     dari alamat network.
   - Ukuran blok: pangkat 2 terkecil yang >= kebutuhan + 2 (minimal /30).
   - Tiap hasil memuat: kebutuhan, network_cidr, dan semua kunci
     hitung_subnet.
   - Raise ValueError bila: network_cidr bukan alamat jaringan yang
     valid, daftar kebutuhan kosong atau berisi nilai < 1, atau blok
     tidak cukup menampung seluruh kebutuhan.
3. Endpoint: GET /api/subnet?ip=&prefix=, POST /api/vlsm (body JSON:
   network, kebutuhan_host), dan GET / untuk halaman index.html.
   Kesalahan input menghasilkan HTTP 400 dengan field "detail".
4. Halaman web: satu halaman dengan dua mode (Subnet dan VLSM),
   menampilkan hasil dan pesan error yang jelas.
5. Tabel test case lengkap, memakai tabel dasar berikut:
   - 172.16.5.130/25 -> network 172.16.5.128, broadcast 172.16.5.255,
     126 host
   - 10.0.0.0/30 -> host .1 sampai .2, broadcast .3, 2 host
   - 192.168.1.0/31 -> point-to-point, 2 host
   - 192.168.1.5/32 -> 1 host
   - 256.1.1.1/24, 192.168.01.1/24, 192.168.1, abc, kosong, prefix 33,
     prefix -1 -> ditolak
   - VLSM 192.168.1.0/24 untuk 100, 50, 20, 2 host -> /25 (.0),
     /26 (.128), /27 (.192), /30 (.224)
   - VLSM 192.168.1.0/24 untuk 200 dan 100 host -> ditolak (tidak muat)

[F] Format: Markdown yang siap saya simpan sebagai SPEC.md, dengan
bagian: Tujuan, Aturan Validasi, Kontrak Fungsi, Kontrak API, Halaman
Web, Tabel Test Case, Di Luar Cakupan.
```

## Tahap 3: Desain UI

Tool: STITCH

```text
[Persona] You are a UI designer for educational tools.

[Context] A web calculator for IPv4 subnetting and VLSM, used by
vocational high school networking teachers. Style: clean, minimalist,
light mode, Google-like (white background, soft gray text, blue accent,
rounded cards).

[Task] Design one responsive page with two tabs: "Subnet" and "VLSM".
Subnet tab: an IP address field, a prefix field (0-32), a "Calculate"
button, and a result card listing mask, network, broadcast, first host,
last host, usable hosts. VLSM tab: a network field (CIDR), a list of
host requirements the user can add or remove, and a result table.
Include three states: empty, success, and error (clear error message
under the field).

[Format] Desktop and mobile layouts. Export-ready HTML/CSS.
```

## Tahap 2b: Issue dan branch

Tool: ANTIGRAVITY

```text
Baca SPEC.md. Buat dokumen `issues/1-issue_subnet_calculator.md` berisi:
Deskripsi, Tugas, Kriteria Penerimaan (merujuk tabel test di SPEC.md),
dan Alur Kerja (issue -> branch -> test dulu -> implementasi -> commit ->
pull request -> CI -> merge). Lalu buat GitHub Issue dari dokumen itu
dengan `gh issue create --title "[Feature] Kalkulator Subnet" --body-file
issues/1-issue_subnet_calculator.md --label feature` (buat label jika
belum ada). Catat nomor issue-nya, lalu buat branch dari main dengan
nama `feature/issue-<nomor>-subnet-calculator`. Commit SPEC.md,
index.html, DESIGN.md, dan folder issues/ sebagai satu commit dengan
pesan "docs: spesifikasi dan desain UI".
```

## Tahap 4: Test dulu (fase merah)

Tool: ANTIGRAVITY

```text
Baca SPEC.md. Tulis test lebih dulu, JANGAN implementasi:

1. Buat `test_main.py` dengan pytest dan `pytest.mark.parametrize`,
   mencakup semua kasus subnet dan API di tabel test SPEC.md (kasus
   normal, /31, /32, input tidak valid, GET /api/subnet sukses dan
   mengembalikan 400 untuk input tidak valid, dan GET / mengembalikan
   200). Kasus VLSM belum dibuat sekarang.
2. Ganti isi `main.py` dengan kerangka saja: `app = FastAPI()` dan fungsi
   `hitung_subnet` yang hanya `raise NotImplementedError`.
3. Jalankan `uv run pytest` dan tunjukkan bahwa test GAGAL (merah).
4. JANGAN membuat folder .github atau workflow CI.
5. Commit dengan pesan "test: tulis test subnet lebih dulu".
```

## Tahap 5: Implementasi

Tool: ANTIGRAVITY

```text
Implementasikan `hitung_subnet` dan endpoint di `main.py` sesuai
SPEC.md, hubungkan `index.html` ke endpoint API (tampilkan hasil dan
pesan error dari field `detail`), lalu jalankan `uv run pytest` sampai
SEMUA test lulus.

Aturan:
- DILARANG mengubah `test_main.py` agar test lulus. Bila menurut Anda
  sebuah test salah, berhenti dan jelaskan alasannya kepada saya.
- Hitung network address dengan operasi bitwise AND antara IP dan
  subnet mask.
- Setelah selesai, jalankan server (`uv run fastapi dev main.py`) dan
  pastikan halaman tampil dan terhubung ke API.
- Commit dengan pesan "feat: implementasi hitung_subnet dan API".
```

## Tahap 6: Review dan verifikasi

Tool: ANTIGRAVITY, MANUSIA

```text
Jelaskan fungsi `hitung_subnet` baris per baris untuk guru TKJ: tunjukkan
bagian yang menghitung subnet mask, bagian operasi AND yang menghasilkan
network address, dan bagian yang menghitung broadcast. Hubungkan
dengan teori subnetting (AND dengan subnet mask). Sebutkan juga bila
ada asumsi atau keputusan yang tidak ada di SPEC.md. Jangan mengubah
kode.
```

## Tahap 7: Git, CI, dan Pull Request

Tool: ANTIGRAVITY

```text
Buat file `.github/workflows/ci.yml` dengan isi PERSIS seperti berikut:

name: SQA Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Run Unit Tests
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v7

      - name: Install uv
        uses: astral-sh/setup-uv@v10.3.3
        with:
          enable-cache: true

      - name: Install Dependencies
        run: uv sync --dev

      - name: Run Tests with Coverage
        run: uv run pytest test_main.py -v --cov=main --cov-report=term-missing

Lalu: commit dengan pesan "ci: tambah pipeline setelah test ada", push branch ini, buka Pull Request ke main (deskripsi memuat "Closes #<nomor issue>"), pantau CI dengan `gh pr checks --watch` sampai hijau, lalu merge Pull Request tersebut. Jangan mengubah test agar CI hijau.
```

## Tahap 8: Fitur VLSM

Tool: ANTIGRAVITY

```text
Kerjakan fitur VLSM sesuai SPEC.md dengan alur lengkap yang sama:
1. Buat `issues/2-issue_vlsm.md` dari SPEC.md, buat GitHub Issue-nya
   (label feature), lalu buat branch `feature/issue-<nomor>-vlsm` dari
   main terbaru.
2. Tulis test VLSM LEBIH DULU di `test_main.py` (tambahkan ke file yang
   ada), buat kerangka `alokasi_vlsm` dan endpoint POST /api/vlsm yang
   belum diimplementasikan, jalankan pytest dan tunjukkan test merah,
   lalu commit.
3. Implementasikan sampai semua test lulus (DILARANG mengubah test
   agar lulus), hubungkan tab VLSM di index.html, lalu commit.
4. Push, buka Pull Request ke main ("Closes #<nomor>"), pantau CI sampai
   hijau, lalu merge.
```

## Tahap 9: Docker (membungkus aplikasi menjadi container)

Tool: ANTIGRAVITY, DOCKER

```text
Kemas aplikasi ini dengan Docker. Kerjakan berurutan:
1. Jalankan `docker version`. Bila bagian Server tidak muncul atau ada error
   koneksi, berhenti dan minta saya menyalakan Docker Desktop. Jangan
   mencoba memasang Docker sendiri.
2. Pastikan di `main` terbaru dan bersih (git switch main, git pull,
   git status), lalu buat branch `chore/docker`.
3. Buat `Dockerfile` di root dengan isi PERSIS seperti berikut:

    # Image dasar: Python 3.12 versi ramping
    FROM python:3.12-slim

    # Salin program uv dari image resminya (versi dikunci agar hasil build selalu sama)
    COPY --from=ghcr.io/astral-sh/uv:0.11.32 /uv /uvx /bin/

    WORKDIR /app
    ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

    # Pasang dependency dulu (lapisan ini di-cache selama uv.lock tidak berubah)
    COPY pyproject.toml uv.lock .python-version ./
    RUN uv sync --frozen --no-dev --no-install-project

    # Salin kode aplikasi
    COPY main.py index.html ./

    # Layanan hosting biasanya mengisi variabel PORT; di laptop dipakai 8000
    ENV PORT=8000
    EXPOSE 8000
    CMD ["sh", "-c", "/app/.venv/bin/uvicorn main:app --host 0.0.0.0 --port ${PORT}"]

4. Buat `.dockerignore` dengan isi PERSIS:

    .venv/
    .git/
    .github/
    __pycache__/
    .pytest_cache/
    .coverage
    htmlcov/
    .env

5. Buat `scripts/smoke_test.py` dengan isi PERSIS seperti di bawah
   (jangan diubah):

    """Smoke test (smoke test) untuk Kalkulator Subnet & VLSM yang sudah berjalan.

    Pemakaian:
        uv run python scripts/smoke_test.py <URL dasar>
    Contoh:
        uv run python scripts/smoke_test.py http://127.0.0.1:8000

    Keluar dengan kode 0 bila semua pemeriksaan lulus, 1 bila ada yang gagal.
    Kesalahan sementara (server belum siap atau cold start) dicoba ulang beberapa kali.
    """

    import http.client
    import json
    import os
    import sys
    import time
    import urllib.error
    import urllib.request

    PERCOBAAN = int(os.environ.get("SMOKE_PERCOBAAN", "6"))
    JEDA_DETIK = int(os.environ.get("SMOKE_JEDA", "15"))


    def minta(base, path, metode="GET", isi=None):
        url = base.rstrip("/") + path
        data = None
        header = {}
        if isi is not None:
            data = json.dumps(isi).encode("utf-8")
            header["Content-Type"] = "application/json"
        terakhir = (0, "")
        for percobaan in range(1, PERCOBAAN + 1):
            try:
                req = urllib.request.Request(url, data=data, headers=header, method=metode)
                with urllib.request.urlopen(req, timeout=30) as r:
                    return r.status, r.read().decode("utf-8", "replace")
            except urllib.error.HTTPError as e:
                terakhir = (e.code, e.read().decode("utf-8", "replace"))
                if e.code < 500:
                    return terakhir
            except (OSError, http.client.HTTPException) as e:
                # server belum siap: koneksi ditolak, terputus, atau habis waktu
                terakhir = (0, str(e))
            if percobaan < PERCOBAAN:
                time.sleep(JEDA_DETIK)
        return terakhir


    def cek_halaman(base):
        status, teks = minta(base, "/")
        assert status == 200, f"status {status}, seharusnya 200"
        assert "<html" in teks.lower(), "isi bukan halaman HTML"


    def cek_subnet(base):
        status, teks = minta(base, "/api/subnet?ip=172.16.5.130&prefix=25")
        assert status == 200, f"status {status}, seharusnya 200"
        hasil = json.loads(teks)
        assert hasil["network"] == "172.16.5.128", f"network {hasil['network']}"
        assert hasil["broadcast"] == "172.16.5.255", f"broadcast {hasil['broadcast']}"
        assert hasil["usable_hosts"] == 126, f"usable_hosts {hasil['usable_hosts']}"


    def cek_input_invalid(base):
        status, _ = minta(base, "/api/subnet?ip=256.1.1.1&prefix=24")
        assert status == 400, f"status {status}, seharusnya 400"


    def cek_vlsm(base):
        isi = {"network": "192.168.1.0/24", "kebutuhan_host": [100, 50, 20, 2]}
        status, teks = minta(base, "/api/vlsm", "POST", isi)
        assert status == 200, f"status {status}, seharusnya 200"
        hasil = [b["network_cidr"] for b in json.loads(teks)]
        harapan = ["192.168.1.0/25", "192.168.1.128/26", "192.168.1.192/27", "192.168.1.224/30"]
        assert hasil == harapan, f"hasil {hasil}"


    PEMERIKSAAN = [
        ("Halaman utama (GET /)", cek_halaman),
        ("Subnet 172.16.5.130/25", cek_subnet),
        ("Input tidak valid ditolak (400)", cek_input_invalid),
        ("VLSM 100, 50, 20, 2 host", cek_vlsm),
    ]


    def main():
        if len(sys.argv) != 2:
            print(__doc__)
            return 2
        base = sys.argv[1]
        gagal = 0
        for nama, fungsi in PEMERIKSAAN:
            try:
                fungsi(base)
                print(f"[LULUS] {nama}")
            except Exception as e:  # noqa: BLE001
                gagal += 1
                print(f"[GAGAL] {nama}: {e}")
        print(f"Ringkasan: {len(PEMERIKSAAN) - gagal} lulus, {gagal} gagal")
        return 1 if gagal else 0


    if __name__ == "__main__":
        sys.exit(main())

6. Build dan jalankan: `docker build -t subnet-calculator .`, lalu
   `docker run -d --name subnet-app -p 8000:8000 subnet-calculator`
   (bila port 8000 masih dipakai server lama, hentikan dulu memakai
   PID-nya), `docker ps`, lalu smoke test
   `uv run python scripts/smoke_test.py http://127.0.0.1:8000`
   (semua harus lulus). Setelah itu `docker rm -f subnet-app`.
7. Ganti isi `.github/workflows/ci.yml` dengan isi PERSIS berikut
   (job baru `docker` berjalan setelah job `test` hijau):

    name: SQA Pipeline

    on:
      push:
        branches: [main]
      pull_request:
        branches: [main]

    jobs:
      test:
        name: Run Unit Tests
        runs-on: ubuntu-latest

        steps:
          - name: Checkout Code
            uses: actions/checkout@v7

          - name: Install uv
            uses: astral-sh/setup-uv@v10.3.3
            with:
              enable-cache: true

          - name: Install Dependencies
            run: uv sync --dev

          - name: Run Tests with Coverage
            run: uv run pytest test_main.py -v --cov=main --cov-report=term-missing

      docker:
        name: Build and Smoke Test Container
        runs-on: ubuntu-latest
        needs: test

        steps:
          - name: Checkout Code
            uses: actions/checkout@v7

          - name: Build Image
            run: docker build -t subnet-calculator .

          - name: Run Container
            run: docker run -d --name subnet-app -p 8000:8000 subnet-calculator

          - name: Smoke Test Container
            env:
              SMOKE_PERCOBAAN: "10"
              SMOKE_JEDA: "3"
            run: python3 scripts/smoke_test.py http://127.0.0.1:8000

          - name: Show Container Logs on Failure
            if: failure()
            run: docker logs subnet-app

8. Tambahkan bagian `## Docker` ke README.md: perintah build, perintah
   run, dan cara menjalankan smoke test ke container lokal.
9. Pastikan pytest masih hijau, commit "build: kemas aplikasi dengan
   Docker dan smoke test container", push, buka Pull Request ke main
   (tanpa "Closes"), pantau CI sampai KEDUA job hijau, lalu merge.
   Jangan mengubah test maupun skrip smoke test.
```

## Tahap 10: Deploy ke Vercel dan smoke test

Tool: MANUSIA, VERCEL, ANTIGRAVITY

### 10a. Periksa kesiapan

Tool: ANTIGRAVITY

```text
Siapkan deploy ke Vercel. Pastikan di `main` terbaru dan bersih, lalu periksa
dan laporkan satu per satu:
- `main.py` ada di root dan memuat variabel `app`.
- `.python-version` berisi 3.12, dan `uv.lock` sudah di-commit.
- `index.html` dan `scripts/smoke_test.py` ada di `main`.
- Tidak ada rahasia (token, kunci, .env) di repo.
- Run CI terakhir di main hijau untuk job `test` dan `docker`
  (`gh run list --branch main --limit 1`).

Lalu berhenti dan tunggu saya. Saya akan mengimpor repo di Vercel dan memberi
Anda URL produksi. JANGAN membuat akun atau login ke Vercel.
```

### 10c. Smoke test di URL produksi

Tool: ANTIGRAVITY

```text
Berikut URL produksi: <URL>. Jalankan
`uv run python scripts/smoke_test.py <URL>` dan tunggu sampai selesai.

- Bila ada [GAGAL]: analisis akar masalah dulu dan tunjukkan analisisnya.
  Bila perlu log, minta saya menempelkan Build Logs atau Runtime Logs dari
  dashboard Vercel. Perbaiki KODE APLIKASI saja, jangan ubah test maupun
  skrip smoke test, lewat branch dan Pull Request baru. Setelah merge Vercel
  men-deploy ulang; jalankan smoke test lagi.
- Bila semua [LULUS]: tambahkan bagian `## Deploy` di README.md (URL dan cara
  smoke test) lewat branch `docs/url-produksi` dan Pull Request kecil, tunggu CI
  hijau, lalu merge.
- Tunjukkan keluaran smoke test dan URL produksi di akhir.
```