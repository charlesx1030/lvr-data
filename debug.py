import requests, re

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})

# 找 GitHub 上的實價登錄鏡像
tests = [
    # grimmerk 的 repo
    ("grimmerk README", "https://raw.githubusercontent.com/grimmerk/Taiwan-house-price-data/master/README.md"),
    # 5168 有 XHR API 嗎？先找他的 JS bundle
    ("5168 main page", "https://price.houseprice.tw/list/%E6%A1%83%E5%9C%92%E5%B8%82_city/%E9%BE%8D%E6%BD%AD%E5%8D%80_zip/%E9%87%91%E9%BE%8D%E8%B7%AF_kw/"),
    # 永慶有 API
    ("yungching api", "https://evertrust.yungching.com.tw/api/realprice?kw=%E9%87%91%E9%BE%8D%E8%B7%AF&zipcode=325&page=1"),
]

for name, url in tests:
    try:
        r = s.get(url, timeout=15)
        print(f"\n{name}: HTTP {r.status_code}, size {len(r.content)}")
        if r.status_code == 200 and len(r.content) < 10000:
            print(r.text[:500])
        elif r.status_code == 200:
            # 找 JS 的 XHR API endpoints
            api_calls = re.findall(r'fetch\(["\']([^"\']+)["\']', r.text)
            xhr_calls = re.findall(r'XMLHttpRequest[^;]*\.open\([^,]+,["\']([^"\']+)["\']', r.text)
            axios_calls = re.findall(r'axios\.(?:get|post)\(["\']([^"\']+)["\']', r.text)
            print(f"  fetch: {api_calls[:3]}")
            print(f"  xhr: {xhr_calls[:3]}")
            print(f"  axios: {axios_calls[:3]}")
    except Exception as e:
        print(f"\n{name}: {type(e).__name__}: {str(e)[:80]}")

# 5168 的 JS bundle 裡找 API
r5 = s.get("https://price.houseprice.tw/", timeout=15)
if r5.status_code == 200:
    # 找 _next/static/chunks/ 裡的 JS
    chunks = re.findall(r'/_next/static/chunks/[^\s"\'<>]+\.js', r5.text)
    print(f"\n5168 JS chunks: {chunks[:3]}")

print("DONE")
