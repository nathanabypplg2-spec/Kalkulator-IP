# SPEC.md — Kalkulator Subnet & VLSM

## Tujuan

Aplikasi web untuk membantu guru dan siswa TKJ memeriksa perhitungan subnet IPv4 dan alokasi VLSM. Hasil utama ditampilkan sebagai alamat yang dapat dibaca tanpa harus memeriksa kode.

## Aturan Validasi

- IPv4 harus terdiri dari tepat empat oktet desimal, masing-masing 0–255, tanpa nol di depan (kecuali oktet `0`) dan tanpa spasi.
- Prefix subnet adalah bilangan bulat 0–32. Input yang tidak valid melempar `ValueError` pada fungsi perhitungan.
- Kebutuhan VLSM harus berupa daftar tidak kosong berisi bilangan bulat positif.
- CIDR VLSM harus berupa alamat jaringan kanonis dan prefix valid. Jika alokasi melebihi blok induk, input ditolak.
- Endpoint mengembalikan HTTP 400 untuk kesalahan input, dengan penjelasan pada field `detail`.

## Kontrak Fungsi

### `hitung_subnet(ip: str, prefix: int) -> dict`

Menghasilkan kunci `mask`, `network`, `broadcast`, `first_host`, `last_host`, dan `usable_hosts`. Network dihitung dengan operasi bitwise AND antara bilangan IP dan subnet mask. Jumlah host untuk prefix 0–30 adalah `2^(32-prefix)-2`. Untuk `/31`, aturan point-to-point RFC 3021 dipakai: dua alamat host dan `broadcast = None`. Untuk `/32`, satu alamat host; `broadcast = None` dan first/last host sama dengan IP masukan.

### `alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]`

Mengurutkan kebutuhan dari terbesar, lalu mengalokasikan berurutan mulai dari network. Setiap blok menggunakan ukuran pangkat dua terkecil yang menampung `kebutuhan + 2`, dengan ukuran minimum `/30`. Setiap item hasil memuat `kebutuhan`, `network_cidr`, serta semua kunci hasil `hitung_subnet`. Melempar `ValueError` untuk CIDR bukan network kanonis, daftar kosong/kebutuhan kurang dari satu, atau kapasitas tidak cukup.

## Kontrak API

- `GET /api/subnet?ip=<IPv4>&prefix=<0..32>` mengembalikan objek hasil subnet.
- `POST /api/vlsm` menerima JSON `{"network":"192.168.1.0/24","kebutuhan_host":[100,50]}` dan mengembalikan daftar alokasi.
- `GET /` menyajikan `index.html`.
- Kesalahan input menghasilkan HTTP 400 dengan JSON berisi `detail`.

## Halaman Web

Satu halaman responsif dengan mode/tab Subnet dan VLSM. Mode Subnet menerima IP dan prefix, lalu menampilkan mask, network, broadcast, rentang host, dan jumlah host. Mode VLSM menerima CIDR dan daftar kebutuhan host yang dapat ditambah/dihapus, lalu menampilkan tabel hasil. Kedua mode menampilkan pesan kesalahan yang jelas.

## Tabel Test Case

| Kasus | Input | Hasil yang diharapkan | Status |
|---|---|---|---|
| Subnet dasar | `172.16.5.130/25` | Network `.128`, broadcast `.255`, host `.129–.254`, 126 host | Pasti |
| Blok `/30` | `10.0.0.0/30` | Host `.1–.2`, broadcast `.3`, 2 host | Pasti |
| Point-to-point `/31` | `192.168.1.0/31` | Dua host `.0–.1`, broadcast null | Keputusan ditetapkan: RFC 3021 |
| Host tunggal `/32` | `192.168.1.5/32` | First/last `.5`, 1 host, broadcast null | Keputusan ditetapkan |
| Oktet di luar rentang | `256.1.1.1/24` | Ditolak | Pasti |
| Nol di depan | `192.168.01.1/24` | Ditolak | Pasti |
| IPv4 kurang oktet / teks / kosong | `192.168.1`, `abc`, `` | Ditolak | Pasti |
| IP mengandung spasi | ` 1.1.1.1/24` | Ditolak | Pasti |
| Prefix di atas rentang | `1.1.1.1/33` | Ditolak | Pasti |
| Prefix di bawah rentang | `1.1.1.1/-1` | Ditolak | Pasti |
| VLSM cukup | `192.168.1.0/24`, `[100,50,20,2]` | `.0/25`, `.128/26`, `.192/27`, `.224/30` | Pasti |
| VLSM tak cukup | `192.168.1.0/24`, `[200,100]` | Ditolak | Pasti |
| CIDR bukan network kanonis | `192.168.1.5/24`, `[10]` | Ditolak | Pasti |
| Daftar/kebutuhan tidak valid | `[]`, `[0]` | Ditolak | Pasti |
| API subnet valid / invalid | GET `/api/subnet` | 200 dengan hasil / 400 dengan `detail` | Pasti |
| API VLSM valid / invalid | POST `/api/vlsm` | 200 / 400 dengan `detail` | Pasti |
| Halaman utama | GET `/` | 200 dan HTML | Pasti |

## Di Luar Cakupan

IPv6, routing, reservasi alamat khusus, autentikasi, penyimpanan data, dan validasi topologi jaringan tidak termasuk.
