#!/usr/bin/env python
"""regen-docs.py · 双站文档再生器（diagram-as-code 模式）
SITES-TREE.md §2/§3/§4 数据节 + sites.manifest.yaml 计数 = 活体仓再生产物。
用法:
  python regen-docs.py            # 再生并覆写两文件
  python regen-docs.py --check    # 只比不写, 有漂移 exit 1（供漂移守卫调用）
规则（docs-index.md）: 数据节在 <!-- GEN:BEGIN -->/<!-- GEN:END --> 之间, 人工节永不覆盖。
"""
import os, re, sys, json
WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def T(repo, *rel):
    f = os.path.join(WS, repo, *rel)
    if not os.path.isfile(f): return ""
    m = re.search(r"<title>([^<]+)", open(f, encoding="utf-8").read())
    return m.group(1).strip() if m else ""
def pages_table(repo, tags):
    d = os.path.join(WS, repo, "pages")
    rows = []
    for x in sorted(os.listdir(d)):
        p = os.path.join(d, x)
        if not os.path.isdir(p): continue
        t = T(repo, "pages", x, "index.html")
        tag = tags.get(x, "")
        rows.append(f"| /pages/{x}/ | {('《'+t+'》') if t else '（无 index.html）'} | {tag} |")
    return rows

def build_tree_data():
    xmg_tags = {
        "master-test": "**B8#1 P0 = sm-test 完整克隆**（title/H1/跳转/sid 全同；独立化 or 301→sm-test 待主人）",
        "bitch-result": "⚠️ H1=slave 残留（B8#5）",
        "memory-result": "⚠️ test/result title 名实错位（B8 P1 类）",
        "general-bigfive-result": "⚠️ H3'情商画像'=emotion 残留（B8#4）",
    }
    ymg_tags = {
        "master-test": "主人综合测评（区别于 xmg 同名 P0 页）",
        "memory-test": "**跨站命名残留：title 写'寻梦阁'**（报告制）",
        "bitch-test": "test/result 命名错位（结果页=女奴属性结果）",
    }
    xrows, yrows = pages_table("simishuwu", xmg_tags), pages_table("yunmengge-pages", ymg_tags)
    man = json.load(open(os.path.join(WS, "yunmengge-router", "api-manifest.json"), encoding="utf-8"))
    exact, pref = man.get("exact", []), man.get("prefix", [])
    d1 = sorted(set(re.findall(r"CREATE TABLE(?: IF NOT EXISTS)? ([a-z_]+)",
        "\n".join(open(os.path.join(WS, "yunmengge-router", "migrations", f), encoding="utf-8").read()
                   for f in os.listdir(os.path.join(WS, "yunmengge-router", "migrations"))
                   if f.endswith(".sql")))))
    return f"""| 路径 | title（本地实读） | 标注 |
|---|---|---|
{chr(10).join(xrows)}
""" + f"""| 路径 | title（本地实读） | 标注 |
|---|---|---|
{chr(10).join(yrows)}
""" + f"""api-manifest: exact {len(exact)} + prefix {len(pref)}（router 仓, 改路由须 --gen-manifest 重发）
D1 增量表（migrations SQL 实测）: {' '.join(d1)}
"""

def main():
    check = "--check" in sys.argv
    data = build_tree_data()
    tree = os.path.join(WS, "SITES-TREE.md")
    cur = open(tree, encoding="utf-8").read()
    m = re.search(r"<!-- GEN:BEGIN §2-->(.*?)<!-- GEN:END §2-->", cur, re.S)
    # 首跑: 若无 GEN 标记, 以当前 §2.1 表格作为基线注入标记
    if not m:
        m2 = re.search(r"### 2\.1 测试/结果页.*?\n(## 3\.)", cur, re.S)
        if m2:
            cur = cur.replace(m2.group(0)[:m2.end()-len(m2.group(1))],
                "### 2.1 测试/结果页（本地实读全页对照）\n<!-- GEN:BEGIN §2-->\n" + data + "<!-- GEN:END §2-->\n")
        open(tree, "w", encoding="utf-8").write(cur)
        print("标记已注入（首跑）; 数据节=全页对照表")
        return
    updated = re.sub(r"(<!-- GEN:BEGIN §2-->).*?(<!-- GEN:END §2-->)",
                    lambda mm: mm.group(1) + "\n" + data + mm.group(2), cur, flags=re.S)
    drift = updated != cur
    if not check:
        open(tree, "w", encoding="utf-8").write(updated)
        print("SITES-TREE.md 数据节已再生" + ("（漂移已更新）" if drift else "（无漂移）"))
    else:
        print("[CHECK] SITES-TREE 数据节:", "DRIFT" if drift else "STABLE")
        sys.exit(1 if drift else 0)

if __name__ == "__main__":
    main()
