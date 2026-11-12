# [Feature] Kalkulator Subnet

## Deskripsi

Buat aplikasi web pembelajaran untuk menghitung subnet IPv4 dan alokasi VLSM dengan hasil yang dapat diperiksa guru.

## Tugas

- Sediakan fungsi hitung subnet IPv4 dengan validasi input.
- Sediakan endpoint subnet dan halaman web.
- Siapkan pengujian untuk kasus normal dan batas sesuai `SPEC.md`.

## Kriteria Penerimaan

- `172.16.5.130/25` menghasilkan network `172.16.5.128`, broadcast `172.16.5.255`, dan 126 host.
- `/30`, `/31` (RFC 3021), dan `/32` mengikuti keputusan pada `SPEC.md`.
- Input IPv4/prefix tidak valid ditolak; API mengembalikan HTTP 400 dengan field `detail`.
- VLSM `192.168.1.0/24` untuk `[100,50,20,2]` menghasilkan `/25`, `/26`, `/27`, `/30` sesuai urutan dan alamat pada `SPEC.md`.
- Semua test yang tercantum di `SPEC.md` lulus.

## Alur Kerja

Issue -> branch -> test dulu -> implementasi -> commit -> pull request -> CI -> merge.
