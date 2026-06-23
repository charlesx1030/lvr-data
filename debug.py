import requests, re, zipfile, io, csv

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})

# 取得下載頁面
r1 = s.get("https://plvr.land.moi.gov.tw/Download_ajax_active", timeout=30)
html = r1.text

# 找所有 DownloadSeason 或 download 的 JS 呼叫
js_calls = re.findall(r'javascript:[^"\'<>]+', html, re.I)
print("JS calls:", js_calls[:5])

# 找 href 和 onclick 帶下載的
hrefs = re.findall(r'href=["\']([^"\']+)["\']', html)
print("\nHrefs:", hrefs[:10])

# 找 onclick 
onclicks = re.findall(r'onclick=["\']([^"\']+)["\']', html)
print("\nOnclicks:", onclicks[:10])

# 找 fileDownload 呼叫（jquery.fileDownload 常見模式）
file_dl = re.findall(r'fileDownload\([^)]+\)', html)
print("\nfileDownload calls:", file_dl[:5])

# 找所有包含 .zip 或 .csv 或 DownloadSeason 的 URL
zip_urls = re.findall(r'["\']([^"\']*(?:zip|csv|DownloadSeason|DownloadOpenData|Download\?)[^"\']*)["\']', html, re.I)
print("\nZIP/CSV URLs:", zip_urls[:10])

# 印出 HTML 中第一個 table 的結構
print("\n=== First 2000 chars of HTML ===")
print(html[html.find('<table'):html.find('<table')+2000] if '<table' in html else html[:2000])

print("DONE")
