import requests, re

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
r1 = s.get("https://plvr.land.moi.gov.tw/DownloadOpenData", timeout=30)

# 找所有 JS 裡的 URL
js_urls = re.findall(r'["\'](/[^"\']*(?:download|Download|csv|zip)[^"\']*)["\']', r1.text, re.I)
print("JS URLs:", js_urls[:10])

# 找 onclick handlers
onclick = re.findall(r'onclick=["\']([^"\']*)["\']', r1.text, re.I)
print("\nOnclick:", onclick[:5])

# 找所有 JS 函數呼叫帶 download 的
js_funcs = re.findall(r'[\w\.]+\([^)]*[Dd]ownload[^)]*\)', r1.text)
print("\nJS funcs:", js_funcs[:5])

# 載入每個 .js 檔案
js_files = re.findall(r'src=["\']([^"\']*\.js[^"\']*)["\']', r1.text, re.I)
print("\nJS files:", js_files)

for js_file in js_files[:3]:
    url = f"https://plvr.land.moi.gov.tw{js_file}" if js_file.startswith('/') else js_file
    r2 = s.get(url, timeout=15)
    if r2.status_code == 200:
        # 找 download 相關
        dl = re.findall(r'["\']([^"\']*[Dd]ownload[^"\']*)["\']', r2.text)
        print(f"\nIn {js_file}: {dl[:3]}")

print("DONE")
