import requests, re

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})

# 解析 data.gov.tw 資料集頁面
r1 = s.get("https://data.gov.tw/dataset/26820", timeout=30)
html = r1.text

# 找下載連結
download_links = re.findall(r'https?://[^\s"\'<>]*(?:download|csv|zip)[^\s"\'<>]*', html, re.I)
print("Download links from dataset/26820:")
for l in download_links[:10]:
    print(" ", l)

# 找 data.gov.tw/dataset 相關 API
api_links = re.findall(r'https?://[^\s"\'<>]*data\.gov\.tw[^\s"\'<>]*', html, re.I)
print("\ndata.gov.tw links:")
for l in set(api_links[:10]):
    print(" ", l)

# 試試 CKAN API (data.gov.tw 用 CKAN)
r2 = s.get("https://data.gov.tw/api/3/action/package_show?id=26820", timeout=15)
print(f"\nCKAN API: {r2.status_code}")
if r2.status_code == 200:
    import json
    data = r2.json()
    if data.get('success'):
        resources = data['result'].get('resources', [])
        print(f"Resources: {len(resources)}")
        for res in resources:
            print(f"  {res.get('name','?')} -> {res.get('url','?')[:100]}")

print("DONE")
