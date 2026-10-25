import sys, json, time, re, urllib.request, urllib.parse
HDR = {"User-Agent": "Mozilla/5.0", "Referer": "https://newslibrary.naver.com/viewer/index.naver"}
HAN = r"[\u3400-\u9fff\uf900-\ufaff\u2e80-\u2fdf]+"
def clean(t, mode):
    if mode == "read":
        t = re.sub(HAN + r"<span class='translation'>[(]([^)]*)[)]</span>", lambda m: m.group(1), t)
    else:
        t = re.sub(r"<span class='translation'>[(]([^)]*)[)]</span>", lambda m: "(" + m.group(1) + ")", t)
    t = re.sub(r"<br\s*/?>", "\n", t); t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&quot;", '"')
    return re.sub(r"\n{3,}", "\n\n", t).strip()
out = open(sys.argv[1], "w", encoding="utf-8")
for aid in sys.argv[2:]:
    url = "https://newslibrary.naver.com/api/article/detail/json?" + urllib.parse.urlencode({"articleId": aid})
    with urllib.request.urlopen(urllib.request.Request(url, headers=HDR), timeout=30) as r:
        a = json.loads(r.read().decode("utf-8"))["result"]["article"]
    rec = {k: a.get(k) for k in ["articleId","officeId","officeName","pageNo","publishDate","articleGenre","personalName","editNo","printNo","publishType","title"]}
    rec["titleRead"] = clean(a.get("translatedTitle") or "", "read")
    rec["titleMixed"] = clean(a.get("translatedTitle") or "", "mixed")
    rec["read"] = clean(a.get("translatedContent") or a.get("content") or "", "read")
    rec["mixed"] = clean(a.get("translatedContent") or a.get("content") or "", "mixed")
    out.write(json.dumps(rec, ensure_ascii=False) + "\n"); time.sleep(0.3)
out.close()
