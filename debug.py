import requests, zipfile, io, csv

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})

# 試 /opendata/ 路徑
urls = [
    "https://plvr.land.moi.gov.tw/opendata/lvr_landAcsv.zip",
    "https://plvr.land.moi.gov.tw/Download?type=zip&fileName=lvr_landcsv.zip",
]

for url in urls:
    print(f"\n=== {url} ===")
    try:
        r = s.get(url, timeout=60)
        print(f"HTTP: {r.status_code}, size: {len(r.content)}")
        if r.content[:4] == b'PK\x03\x04':
            print("✅ ZIP!")
            z = zipfile.ZipFile(io.BytesIO(r.content))
            print("files:", z.namelist()[:5])
            # 找桃園市買賣檔案
            for name in z.namelist():
                if 'H_' in name.upper() and '_A' in name.upper():
                    print(f"Reading {name}...")
                    with z.open(name) as f:
                        rows = list(csv.reader(f.read().decode('utf-8-sig', errors='replace').splitlines()))
                    print(f"  rows: {len(rows)}")
                    longtan = [row for row in rows if row and '龍潭' in row[0]]
                    print(f"  龍潭: {len(longtan)} 筆")
                    if longtan:
                        print(f"  sample: {longtan[0][:4]}")
                    break
        else:
            print("Content:", r.content[:300])
    except Exception as e:
        print(f"ERROR: {e}")

print("DONE")
