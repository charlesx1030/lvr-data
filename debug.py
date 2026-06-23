import requests, zipfile, io, sys

def try_url(url, extra_headers=None):
    h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    if extra_headers:
        h.update(extra_headers)
    r = requests.get(url, timeout=60, headers=h)
    print(f"  HTTP: {r.status_code}, size: {len(r.content)}")
    if r.content[:4] == b'PK\x03\x04':
        print("  ✅ ZIP!")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        print("  files:", z.namelist())
        return z
    else:
        print("  text:", r.content[:200])
    return None

print("=== Test 1: DownloadSeason with Referer ===")
try_url(
    "https://plvr.land.moi.gov.tw/DownloadSeason?season=114S4&type=zip&fileName=H_lvr_land_A.zip",
    {"Referer": "https://plvr.land.moi.gov.tw/DownloadOpenData"}
)

print("\n=== Test 2: 先訪問首頁取 cookie 再下載 ===")
s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
s.get("https://plvr.land.moi.gov.tw/DownloadOpenData", timeout=30)
print("cookies:", dict(s.cookies))
r2 = s.get(
    "https://plvr.land.moi.gov.tw/DownloadSeason?season=114S4&type=zip&fileName=H_lvr_land_A.zip",
    timeout=60
)
print(f"HTTP: {r2.status_code}, size: {len(r2.content)}")
if r2.content[:4] == b'PK\x03\x04':
    print("✅ ZIP!")
    z = zipfile.ZipFile(io.BytesIO(r2.content))
    print("files:", z.namelist())
else:
    print("text:", r2.content[:200])

print("\n=== Test 3: 直接下載本期 ===")
try_url("https://plvr.land.moi.gov.tw/Download?type=zip&fileName=H_lvr_land_A.zip")

print("DONE")
