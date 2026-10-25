import sys, json, time, urllib.request, urllib.parse
API = "https://newslibrary.naver.com/api/search/article/json"
HDR = {"User-Agent": "Mozilla/5.0", "Referer": "https://newslibrary.naver.com/search/searchByKeyword.naver"}
def count(kw, s, e, office=""):
    q = {"keyword": kw, "startDate": s, "endDate": e, "startIndex": 1, "endIndex": 1}
    if office: q["officeId"] = office
    url = API + "?" + urllib.parse.urlencode(q)
    for _ in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HDR), timeout=30) as r:
                d = json.loads(r.read().decode("utf-8"))
            return int(d["result"].get("articleCount") or 0)
        except Exception as ex:
            time.sleep(1)
    return -1
kws = sys.argv[2].split("|")
years = list(range(1950, 1956))
offices = [("00020","동아"),("00032","경향")]
out = open(sys.argv[1], "w", encoding="utf-8")
out.write("keyword\toffice\t" + "\t".join(map(str, years)) + "\ttotal\n")
for kw in kws:
    for oid, oname in offices:
        row = []
        for y in years:
            s = "1950-06-25" if y == 1950 else f"{y}-01-01"
            row.append(count(kw, s, f"{y}-12-31", oid)); time.sleep(0.25)
        out.write(f"{kw}\t{oname}\t" + "\t".join(map(str,row)) + f"\t{sum(x for x in row if x>0)}\n"); out.flush()
out.close()
