import requests, re

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
r1 = s.get("https://plvr.land.moi.gov.tw/DownloadOpenData", timeout=30)

# 讀 qt.js 找 loadAjaxUrl 和下載邏輯
r_qt = s.get("https://plvr.land.moi.gov.tw/js/qt/qt.js", timeout=15)
print("qt.js size:", len(r_qt.text))

# 找 loadAjaxUrl 定義
idx = r_qt.text.find('loadAjaxUrl')
if idx >= 0:
    print("loadAjaxUrl found at:", idx)
    print(r_qt.text[idx:idx+500])

# 找 download 相關函數
dl_funcs = re.findall(r'function\s+\w*[Dd]ownload\w*[^{]*{[^}]*}', r_qt.text, re.S)
print("\nDownload funcs:", dl_funcs[:2])

# 讀 qt-ajax.js
r_qa = s.get("https://plvr.land.moi.gov.tw/js/qt/qt-ajax.js", timeout=15)
print("\nqt-ajax.js size:", len(r_qa.text))
idx2 = r_qa.text.find('Download_ajax')
if idx2 >= 0:
    print("Download_ajax found:")
    print(r_qa.text[max(0,idx2-100):idx2+500])

# 直接試 AJAX endpoints
for endpoint in ['Download_ajax_active', 'DownloadHistory_ajax_list', 'Download_ajax_list']:
    r2 = s.get(f"https://plvr.land.moi.gov.tw/{endpoint}", timeout=15)
    print(f"\n{endpoint}: {r2.status_code}, size: {len(r2.content)}")
    if r2.status_code == 200:
        print(r2.text[:300])

print("DONE")
