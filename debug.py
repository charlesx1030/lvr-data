import requests, re

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})

# 測試其他能從 GitHub Actions 連的來源
tests = [
    # 5168 有 JSON API 嗎？
    ("5168 json", "https://price.houseprice.tw/api/v1/deals?zipcode=325&road=%E9%87%91%E9%BE%8D%E8%B7%AF"),
    # 樂屋網 API
    ("rakuya api", "https://realtyprice.rakuya.com.tw/api/realprice?zipcode=325&keyword=%E9%87%91%E9%BE%8D%E8%B7%AF&page=1"),
    # TWDATA g0v 有沒有鏡像
    ("twdata", "https://raw.githubusercontent.com/g0v/twdata/master/README.md"),
    # Huggingface datasets（有人上傳了實價登錄嗎）
    ("huggingface", "https://datasets-server.huggingface.co/search?dataset=lvr&config=default&split=train&query=%E9%BE%8D%E6%BD%AD"),
    # 5168 實際的資料 endpoint（從頁面分析）
    ("5168 deals", "https://price.houseprice.tw/api/deals?city=%E6%A1%83%E5%9C%92%E5%B8%82&zip=325&road=%E9%87%91%E9%BE%8D%E8%B7%AF&page=1&pageSize=20"),
]

for name, url in tests:
    try:
        r = s.get(url, timeout=15)
        print(f"\n{name}: HTTP {r.status_code}, size {len(r.content)}")
        if r.status_code == 200:
            ct = r.headers.get('content-type','')
            print(f"  Content-Type: {ct}")
            if 'json' in ct:
                print(f"  JSON preview: {r.text[:300]}")
            else:
                print(f"  Text preview: {r.content[:200]}")
    except Exception as e:
        print(f"\n{name}: ERROR {type(e).__name__}: {str(e)[:100]}")

print("DONE")
