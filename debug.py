import requests, re, json

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})

# 搜尋 data.gov.tw 實價登錄桃園市
r1 = s.get("https://data.gov.tw/datasets/search?q=%E5%AF%A6%E5%83%B9%E7%99%BB%E9%8C%84%E6%A1%83%E5%9C%92&page=1&pageSize=10", timeout=30)
print(f"Search HTTP: {r1.status_code}, size: {len(r1.content)}")

# 找 dataset links
links = re.findall(r'href=["\'](/dataset/\d+)["\']', r1.text)
print("Dataset links:", links[:10])

# 試 dataset/77051（內政部當期批次資料）
for ds_id in ['77051', '25119', '34521']:
    r2 = s.get(f"https://data.gov.tw/dataset/{ds_id}", timeout=20)
    print(f"\ndataset/{ds_id}: HTTP {r2.status_code}")
    # 找下載連結
    dl = re.findall(r'https?://[^\s"\'<>]*(?:plvr|lvr)[^\s"\'<>]*', r2.text, re.I)
    print("  plvr/lvr links:", dl[:3])
    # 找 zip/csv 連結
    zips = re.findall(r'https?://[^\s"\'<>]*\.(?:zip|csv)[^\s"\'<>]*', r2.text, re.I)
    print("  zip/csv links:", zips[:3])

print("DONE")
