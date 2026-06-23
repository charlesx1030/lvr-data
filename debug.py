import requests, zipfile, io, csv, sys

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

print("Step1: 訪問首頁...")
r1 = s.get("https://plvr.land.moi.gov.tw/DownloadOpenData", timeout=30)
print(f"  HTTP: {r1.status_code}, cookies: {dict(s.cookies)}")

# 找 CSRF token 或 agree 按鈕
import re
tokens = re.findall(r'name=["\']([^"\']*token[^"\']*)["\'] value=["\']([^"\']*)["\'] ', r1.text, re.I)
print("  tokens:", tokens[:3])

print("\nStep2: POST 同意授權...")
# 嘗試 POST agree
r2 = s.post("https://plvr.land.moi.gov.tw/DownloadOpenData", 
    data={"agree": "Y"},
    timeout=30)
print(f"  HTTP: {r2.status_code}, size: {len(r2.content)}")

print("\nStep3: 下載資料...")
r3 = s.get(
    "https://plvr.land.moi.gov.tw/DownloadSeason?season=114S4&type=zip&fileName=H_lvr_land_A.zip",
    timeout=60
)
print(f"  HTTP: {r3.status_code}, size: {len(r3.content)}")
if r3.content[:4] == b'PK\\x03\\x04':
    print("  ✅ ZIP!")
else:
    print("  Content:", r3.content[:300])

print("DONE")
