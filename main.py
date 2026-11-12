import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse

app = FastAPI(title="Kalkulator Subnet & VLSM")
FULL = 0xFFFFFFFF


def _parse_ip(ip) -> int:
    if not isinstance(ip, str):
        raise ValueError("IP harus berupa teks")
    parts = ip.split(".")
    if len(parts) != 4:
        raise ValueError("IP harus terdiri dari 4 oktet")
    val = 0
    for p in parts:
        if not (p.isascii() and p.isdigit()) or len(p) > 3:
            raise ValueError(f"Oktet '{p}' tidak valid")
        if len(p) > 1 and p[0] == "0":
            raise ValueError(f"Oktet '{p}' tidak boleh diawali angka nol")
        if int(p) > 255:
            raise ValueError(f"Oktet '{p}' melebihi 255")
        val = (val << 8) | int(p)
    return val


def _ip(n: int) -> str:
    return ".".join(str((n >> s) & 255) for s in (24, 16, 8, 0))


def _bin(n: int) -> str:
    return ".".join(format((n >> s) & 255, "08b") for s in (24, 16, 8, 0))


def _kelas(n: int) -> str:
    f = n >> 24
    return "A" if f < 128 else "B" if f < 192 else "C" if f < 224 else "D" if f < 240 else "E"


def hitung_subnet(ip: str, prefix: int) -> dict:
    ip_int = _parse_ip(ip)
    if isinstance(prefix, bool) or not isinstance(prefix, int) or not 0 <= prefix <= 32:
        raise ValueError("Prefix harus bilangan bulat 0-32")
    mask = (FULL << (32 - prefix)) & FULL
    net = ip_int & mask  # operasi AND dengan subnet mask
    bcast = net | (~mask & FULL)
    if prefix == 32:
        first, last, hosts, b = ip_int, ip_int, 1, None
    elif prefix == 31:
        first, last, hosts, b = net, net + 1, 2, None
    else:
        first, last, hosts, b = net + 1, bcast - 1, 2 ** (32 - prefix) - 2, _ip(bcast)
    return {
        "mask": _ip(mask), "network": _ip(net), "broadcast": b,
        "first_host": _ip(first), "last_host": _ip(last), "usable_hosts": hosts,
        "prefix": prefix, "wildcard": _ip(~mask & FULL), "kelas": _kelas(ip_int),
        "ip_bin": _bin(ip_int), "mask_bin": _bin(mask), "network_bin": _bin(net),
        "broadcast_bin": _bin(bcast), "total_alamat": 2 ** (32 - prefix),
    }


def alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]:
    if not isinstance(network_cidr, str) or "/" not in network_cidr:
        raise ValueError("Network harus berformat CIDR, contoh 192.168.1.0/24")
    ip_s, _, p_s = network_cidr.partition("/")
    if not p_s.isdigit():
        raise ValueError("Prefix network tidak valid")
    prefix = int(p_s)
    base = hitung_subnet(ip_s, prefix)
    if base["network"] != ip_s:
        raise ValueError(f"{network_cidr} bukan alamat jaringan (seharusnya {base['network']}/{prefix})")
    if (not isinstance(kebutuhan_host, list) or not kebutuhan_host
            or any(isinstance(k, bool) or not isinstance(k, int) or k < 1 for k in kebutuhan_host)):
        raise ValueError("Kebutuhan host harus daftar bilangan bulat >= 1")
    start = _parse_ip(ip_s)
    end = start + 2 ** (32 - prefix)
    cursor, hasil = start, []
    for need in sorted(kebutuhan_host, reverse=True):
        size = 4
        while size < need + 2:
            size *= 2
        if cursor + size > end:
            raise ValueError("Blok jaringan tidak cukup menampung seluruh kebutuhan")
        p = 32 - (size.bit_length() - 1)
        hasil.append({"kebutuhan": need, "network_cidr": f"{_ip(cursor)}/{p}",
                      **hitung_subnet(_ip(cursor), p)})
        cursor += size
    return hasil


@app.get("/api/subnet")
def api_subnet(ip: str = "", prefix: str = ""):
    try:
        if not prefix.strip().lstrip("-").isdigit():
            raise ValueError("Prefix harus bilangan bulat 0-32")
        return hitung_subnet(ip, int(prefix))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/vlsm")
async def api_vlsm(request: Request):
    try:
        body = json.loads(await request.body())
        return alokasi_vlsm(body["network"], body["kebutuhan_host"])
    except (ValueError, KeyError, TypeError) as e:
        raise HTTPException(status_code=400, detail=str(e) or "Input tidak valid")


@app.get("/")
def index():
    return FileResponse(Path(__file__).parent / "index.html")