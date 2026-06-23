import requests, zipfile, io, csv, sys

season = "114S4"
url = "https://plvr.land.moi.gov.tw/DownloadSeason?season=" + season + "&type=zip&fileName=H_lvr_land_A.zip"
print("URL:", url)
sys.stdout.flush()

r = requests.get(url, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
print("HTTP:", r.status_code, "Size:", len(r.content))
sys.stdout.flush()

if r.status_code == 200:
    try:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        print("ZIP files:", z.namelist())
        for n in z.namelist():
            if n.upper().endswith("_A.CSV"):
                print("Reading:", n)
                with z.open(n) as f:
                    raw = f.read().decode("utf-8-sig", errors="replace")
                rows = list(csv.reader(raw.splitlines()))
                print("Total rows:", len(rows))
                print("Row 0:", rows[0][:4] if rows else "empty")
                print("Row 1:", rows[1][:4] if len(rows)>1 else "na")
                print("Row 2:", rows[2][:4] if len(rows)>2 else "na")
                longtan = [row for row in rows if row and "龍潭" in row[0]]
                print("龍潭 rows:", len(longtan))
                if longtan:
                    print("Sample:", longtan[0][:4])
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("First 300 bytes:", r.content[:300])
else:
    print("HTTP Error:", r.content[:300])
print("DONE")
