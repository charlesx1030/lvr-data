import requests, zipfile, io, re, sys

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

print("Step1: 訪問首頁...")
r1 = s.get("https://plvr.land.moi.gov.tw/DownloadOpenData", timeout=30)
print(f"  HTTP: {r1.status_code}")

# 找所有 form 和 input
forms = re.findall(r'<form[^>]*>(.*?)</form>', r1.text, re.S | re.I)
print(f"  Forms: {len(forms)}")
for i, form in enumerate(forms[:3]):
    inputs = re.findall(r'<input[^>]*>', form, re.I)
    print(f"  Form {i}: {inputs[:5]}")
    
# 找所有 button
buttons = re.findall(r'<(?:button|input)[^>]*(?:submit|agree|download)[^>]*>', r1.text, re.I)
print(f"\nButtons/submits: {buttons[:5]}")

# 找 href with download
download_links = re.findall(r'href=["\']([^"\']*)["\'][^>]*>[^<]*(?:下載|download|agree)[^<]*<', r1.text, re.I)
print(f"\nDownload links: {download_links[:5]}")

# 輸出原始 HTML 的關鍵部分
print("\n=== HTML snippet (around 'agree' or '同意') ===")
idx = r1.text.find('同意')
if idx > 0:
    print(r1.text[max(0,idx-200):idx+500])
else:
    print("找不到 '同意'")
    # 看前 500 chars
    print("First 500:", r1.text[:500])

print("DONE")
