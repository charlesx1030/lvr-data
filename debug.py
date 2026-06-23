import requests, re

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})

# 測試各個備用來源
tests = [
    # 政府開放資料平台
    ("data.gov.tw API", "https://data.gov.tw/api/v2/rest/datastore/355000000A-000155-001?limit=1"),
    # 內政部資料開放平台
    ("moi open data", "https://data.moi.gov.tw/MoiOD/Data/DataDetail.aspx?oid=E2201829-B4ED-4ED6-B46D-EA0FC376368F"),
    # 5168 實價登錄（有公開 API）
    ("5168 api", "https://price.houseprice.tw/api/deals?zipcode=325&keyword=%E9%87%91%E9%BE%8D%E8%B7%AF&page=1"),
    # 直接 data.gov.tw 下載
    ("data.gov.tw download", "https://data.gov.tw/dataset/26820"),
]

for name, url in tests:
    try:
        r = s.get(url, timeout=15)
        print(f"{name}: HTTP {r.status_code}, size {len(r.content)}")
        if r.status_code == 200:
            print(f"  first 200: {r.content[:200]}")
    except Exception as e:
        print(f"{name}: ERROR {e}")

print("DONE")
