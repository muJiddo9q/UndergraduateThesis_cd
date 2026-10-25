import sys, csv, collections
src, dst = sys.argv[1], sys.argv[2]
rng = lambda a, b: set(range(a, b + 1))
T = {
 "T1 원조·대일구매": {3,5,46,56,57,60,61,62,63,75,77,85,87,89,92,93,96,101,102,103,104,105,106,107,108,109,110,111,113,114,117,118,125,132,153,155,156} | rng(168,173) | {176} | rng(178,185),
 "T2 특수 보도·분석": rng(11,15) | {23,30,43,47,48,58,122,126,137,139,177},
 "T3 일본 부흥=참조 모델": {2,4,7,16,19,20,24,25,28,40,44,45} | rng(49,52) | {54,71,72,74,80,83,86,94,99,100,142,143,147,148},
 "T4 조달 현지화 요구": {36,37,38,39,133,152,166},
 "T5 대일 경계·한일관계": {1,8,17,29,33,42,67,68,97,158,160,191},
}
genre = {"00101":"기사","00102":"사설","00115":"논단·기고","00116":"좌담","00106":"해설","00108":"기획연재","00111":"칼럼"}
rows = list(csv.DictReader(open(src, encoding="utf-8"), delimiter="\t"))
cnt, gcnt, ycnt = collections.Counter(), collections.Counter(), collections.Counter()
with open(dst, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["번호","날짜","신문","면","장르(추정)","분류","검색어","제목(원문)","제목(독음)","요약(독음, 일부)","원문 링크"])
    for i, r in enumerate(rows, 1):
        tag = next((k for k, v in T.items() if i in v), "X 주변·무관")
        g = genre.get(r["genre"], r["genre"])
        cnt[tag] += 1
        if not tag.startswith("X"):
            gcnt[g] += 1; ycnt[(r["date"][:4], r["office"][:2])] += 1
        w.writerow([f"{i:03d}", r["date"], r["office"], r["page"], g, tag, r["keywords"], r["title"], r["translatedTitle"], r["summary"][:150], r["url"]])
print("분류별:", dict(cnt))
print("관련 기사 장르별:", dict(gcnt))
print("관련 기사 연도·신문별:", dict(sorted(ycnt.items())))
print("관련 합계:", sum(v for k, v in cnt.items() if not k.startswith("X")))
