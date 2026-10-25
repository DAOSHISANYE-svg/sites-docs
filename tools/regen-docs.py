#!/usr/bin/env python
"""regen-docs.py · SITES-TREE.md 数据节再生器 v2（三块 GEN: xmg表/ymg表/端点表）
用法: python regen-docs.py            # 再生并覆写
      python regen-docs.py --check    # 只比不写, 漂移 exit 1
规则: 数据节在 <!-- GEN:BEGIN §N-->/<!-- GEN:END §N--> 之间; 人工节永不覆盖。
"""
import os, re, sys, json
WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def T(repo, *rel):
    f = os.path.join(WS, repo, *rel)
    if not os.path.isfile(f): return ""
    m = re.search(r"<title>([^<]+)", open(f, encoding="utf-8").read())
    return m.group(1).strip() if m else ""
def table(repo, tags):
    rows = []
    for x in sorted(os.listdir(os.path.join(WS, repo, "pages"))):
        p = os.path.join(WS, repo, "pages", x)
        if not os.path.isdir(p): continue
        t = T(repo, "pages", x, "index.html")
        tt = t.replace('|', '\|') if t else ''
        tg = tags.get(x, '').replace('|', '\|')
        rows.append(f"| /pages/{x}/ | {('《'+tt+'》') if tt else '（无 index.html）'} | {tg} |")
    return "\n".join(rows)
def endpoints():
    man = json.load(open(os.path.join(WS, "yunmengge-router", "api-manifest.json"), encoding="utf-8"))
    d1 = sorted(set(re.findall(r"CREATE TABLE(?: IF NOT EXISTS)? ([a-z_]+)",
        "\n".join(open(os.path.join(WS,"yunmengge-router","migrations",f),encoding="utf-8").read()
                   for f in os.listdir(os.path.join(WS,"yunmengge-router","migrations")) if f.endswith(".sql")))))
    return (f"api-manifest: exact {len(man.get('exact',[]))} + prefix {len(man.get('prefix',[]))}（router 仓, 改路由须 --gen-manifest 重发）\n"
            f"D1 增量表（migrations SQL 实测）: {' '.join(d1)}")
X_TAGS = {"master-test":"**B8#1 P0 = sm-test 完整克隆**","bitch-result":"⚠️ H1=slave 残留（B8#5）",
          "memory-result":"⚠️ test/result title 名实错位（B8 P1 类）","general-bigfive-result":"⚠️ H3'情商画像'=emotion 残留（B8#4）"}
Y_TAGS = {"master-test":"主人综合测评（区别于 xmg 同名 P0 页）","memory-test":"**跨站命名残留：title 写'寻梦阁'**（报告制）",
          "bitch-test":"test/result 命名错位"}
def blocks():
    return {"§2": table("simishuwu", X_TAGS), "§3": table("yunmengge-pages", Y_TAGS), "§4": endpoints()}
def ensure(s, key, data, anchor, head):
    if f"<!-- GEN:BEGIN {key}-->" in s:
        return re.sub(rf"(<!-- GEN:BEGIN {key}-->).*?(<!-- GEN:END {key}-->)",
                      f"\g<1>\n{data}\n\g<2>", s, flags=re.S), True
    a = s.find(anchor)
    if a < 0: s += "\n" + head + f"\n<!-- GEN:BEGIN {key}-->\n{data}\n<!-- GEN:END {key}-->\n"
    else:
        a = s.find("\n", a) + 1
        s = s[:a] + f"{head}\n<!-- GEN:BEGIN {key}-->\n{data}\n<!-- GEN:END {key}-->\n" + s[a:]
    return s, False
def main():
    check = "--check" in sys.argv
    cur = open(os.path.join(WS, "SITES-TREE.md"), encoding="utf-8").read()
    B = blocks()
    # §2: xmg 表（若旧 §2 块含 api/D1 尾巴=旧版, 先清除尾巴再重写）
    m = re.search(r"<!-- GEN:BEGIN §2-->(.*?)<!-- GEN:END §2-->", cur, re.S)
    if m:
        body = m.group(1)
        cut = body.find("api-manifest:")
        if cut > 0:  # 旧版混入端点行 → 拆出
            cur = cur.replace(body, body[:cut].strip())
    cur, _ = ensure(cur, "§2", B["§2"], "### 2.1", "### 2.1 测试/结果页（全页对照 · 再生数据节）")
    cur, _ = ensure(cur, "§3", B["§3"], "### 3.1", "### 3.1 测试/结果页（全页对照 · 再生数据节）")
    cur, _ = ensure(cur, "§4", B["§4"], "## 4. 共享后端", "### 4.0 端点/D1 计数（再生数据节）")
    if not check:
        open(os.path.join(WS, "SITES-TREE.md"), "w", encoding="utf-8").write(cur)
        print("SITES-TREE.md 三块数据节已再生")
    else:
        drift = cur != open(os.path.join(WS, "SITES-TREE.md"), encoding="utf-8").read()
        print(f"[CHECK] SITES-TREE 数据节: {'DRIFT' if drift else 'STABLE'}")
        sys.exit(1 if drift else 0)
if __name__ == "__main__":
    main()
