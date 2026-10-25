import sys, json, urllib.request, urllib.parse, re
HDR = {"User-Agent": "Mozilla/5.0", "Referer": "https://newslibrary.naver.com/viewer/index.naver"}
def find(o, key):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key and isinstance(v, str): return v
            r = find(v, key)
            if r: return r
    elif isinstance(o, list):
        for v in o:
            r = find(v, key)
            if r: return r
    return None
out = open(sys.argv[1], "w", encoding="utf-8")
for aid in sys.argv[2:]:
    url = "https://newslibrary.naver.com/api/article/detail/json?" + urllib.parse.urlencode({"articleId": aid})
    with urllib.request.urlopen(urllib.request.Request(url, headers=HDR), timeout=30) as r:
        d = json.loads(r.read().decode("utf-8"))
    t = find(d, "translatedContent") or find(d, "content") or ""
    t = re.sub(r"[\u3400-\u9fff\uf900-\ufaff]+<span class='translation'>[(]([^)]*)[)]</span>", lambda m: m.group(1), t)
    t = re.sub(r"<br\s*/?>", "\n", t); t = re.sub(r"<[^>]+>", "", t)
    out.write("== " + aid + " " + (find(d, "title") or "") + "\n" + t + "\n\n")
out.close()
