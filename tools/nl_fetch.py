import sys, json, time, re, urllib.request, urllib.parse, csv
API = "https://newslibrary.naver.com/api/search/article/json"
HDR = {"User-Agent": "Mozilla/5.0", "Referer": "https://newslibrary.naver.com/search/searchByKeyword.naver"}
def get(q):
    url = API + "?" + urllib.parse.urlencode(q)
    for _ in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HDR), timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))["result"]
        except Exception:
            time.sleep(1)
    return None
strip = lambda s: re.sub(r"<[^>]+>", "", s or "").replace("\t"," ").replace("\n"," ").strip()
out, kws = sys.argv[1], sys.argv[2].split("|")
seen = {}
for kw in kws:
    for oid in ["00020", "00032"]:
        start = 1
        while True:
            res = get({"keyword": kw, "startDate": "1950-06-25", "endDate": "1955-12-31", "officeId": oid, "startIndex": start, "endIndex": start+99})
            if not res: break
            arts = (res.get("articles") or {}).get("article") or []
            if isinstance(arts, dict): arts = [arts]
            for a in arts:
                aid = a["articleId"]
                if aid in seen: seen[aid]["kw"].add(kw); continue
                seen[aid] = {"kw": {kw}, "date": a.get("publishDate"), "office": a.get("officeName"), "page": a.get("pageNo"),
                             "genre": a.get("articleGenre"), "title": strip(a.get("title")), "ttitle": strip(a.get("translatedTitle")),
                             "summary": strip(a.get("translatedContentSummary"))[:220],
                             "url": f"https://newslibrary.naver.com/viewer/index.naver?articleId={aid}&editNo={a.get('editNo')}&printCount=1&publishDate={a.get('publishDate')}&officeId={a.get('officeId')}&pageNo={a.get('pageNo')}&printNo={a.get('printNo')}&publishType={a.get('publishType')}"}
            total = int(res.get("articleCount") or 0)
            start += 100
            time.sleep(0.3)
            if start > total or start > 600: break
with open(out, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["date","office","page","genre","keywords","title","translatedTitle","summary","url"])
    for aid, v in sorted(seen.items(), key=lambda x: x[1]["date"]):
        w.writerow([v["date"], v["office"], v["page"], v["genre"], ",".join(sorted(v["kw"])), v["title"], v["ttitle"], v["summary"], v["url"]])
print("articles:", len(seen))
