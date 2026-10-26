#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""D1 恢复演练 (L4-local) — ADR-009 L4 的本地等价证明:
把最新 D1 备份 SQL 灌入全新 SQLite :memory:, 断言「可还原」:
- 全部语句执行 rc=0 (SQL 语法/完整性可恢复)
- 表数 >= 期望基线 (13: SCHEMA 10 + 增量 3, 见 SITES-TREE GEN)
- INSERT 行数 > 0 (数据非空)
- 抽检 1 列可读 (数据内容可用)
生产 D1 零接触 (只读本地 SQL 文件)。生产 L4-prod (写 D1) 仍 blocked-on-scope。
ledger: E:/hermes/output/restore-drill.jsonl (append-only, backup-integrity §14 同族)
cron: 每日 04:30 no-agent。
"""
import json, os, re, sqlite3, sys, time

BACKUP_DIR = r"E:/hermes/d1-backups"
LEDGER = r"E:/hermes/output/restore-drill.jsonl"
MIN_TABLES = 10   # 保守基线 (13 全量, 10=硬下限防 schema 缩减)

def pick_latest():
    fs = [f for f in os.listdir(BACKUP_DIR) if f.endswith(".sql") and not f.endswith(".tmp")]
    if not fs:
        sys.exit("FAIL: no backup SQL in " + BACKUP_DIR)
    return os.path.join(BACKUP_DIR, sorted(fs)[-1])

def drill():
    f = pick_latest()
    sql = open(f, encoding="utf-8").read()
    con = sqlite3.connect(":memory:")
    t0 = time.time()
    try:
        con.executescript(sql)
    except Exception as e:
        print(f"FAIL: executescript error: {e}")
        return {"ok": False, "file": f, "error": str(e)[:200]}
    rows = con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall()
    tables = [r[0] for r in rows]
    total_rows = 0
    sample = None
    for t in tables[:3]:
        n = con.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
        total_rows += n
        if sample is None and n > 0:
            sample = {"table": t, "rows": n, "first_id": con.execute(f'SELECT rowid FROM "{t}" LIMIT 1').fetchone()[0]}
    ok = len(tables) >= MIN_TABLES and total_rows > 0
    result = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime()),
        "ok": ok, "file": os.path.basename(f), "size_kb": os.path.getsize(f)//1024,
        "tables": len(tables), "table_list": tables, "total_rows_sampled": total_rows,
        "sample": sample, "exec_ms": int((time.time()-t0)*1000),
        "scope": "L4-local (restore-ability proof, production D1 untouched)",
    }
    print(("OK  " if ok else "FAIL") + f" {result['file']} {result['size_kb']}KB tables={result['tables']} rows(sampled3)={total_rows} {result['exec_ms']}ms")
    if not ok:
        print(f"  detail: {tables}")
    with open(LEDGER, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(result, ensure_ascii=False) + "\n")
    return result


def prod_check():
    """L4-prod-read: 备份 vs 生产 D1 表结构+行数对照 (只读, 零写风险).
    token=E:/hermes/config/keys/.env CLOUDFLARE_API_TOKEN (cfut_, D1:read 实证).
    真正的写回恢复(L4-prod-write)=不可逆最后手段, 见 RUNBOOK D1 节 + 主人授权触发."""
    import urllib.request
    env = open(r"E:/hermes/config/keys/.env", encoding="utf-8").read()
    tok = re.search(r"^CLOUDFLARE_API_TOKEN\s*=\s*(\S+)", env, re.M).group(1).strip('"')
    acc = "071c36c227211679dd1537626856116f"
    def api(path, body=None, method="GET"):
        last = None
        for attempt in range(3):
            try:
                req = urllib.request.Request(f"https://api.cloudflare.com/client/v4/accounts/{acc}{path}",
                                             headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"},
                                             data=json.dumps(body).encode() if body else None, method=method)
                return json.loads(urllib.request.urlopen(req, timeout=30).read())
            except Exception as e:
                last = e
                time.sleep(2)
        raise last
    uuid = [d["uuid"] for d in api("/d1/database")["result"] if d["name"] == "xunmengge-db"][0]
    def d1q(sql):
        return api(f"/d1/database/{uuid}/query", {"sql": sql}, "POST")["result"][0]["results"]
    prod = [x["name"] for x in d1q("SELECT name FROM sqlite_master WHERE type='table'") if not x["name"].startswith(("sqlite_", "_cf_"))]
    f = pick_latest()
    con = sqlite3.connect(":memory:"); con.executescript(open(f, encoding="utf-8").read())
    bk = [x[0] for x in con.execute("SELECT name FROM sqlite_master WHERE type='table'") if not x[0].startswith(("sqlite_", "_cf_"))]
    missing = [t for t in prod if t not in bk]
    diffs = []
    same = 0
    for t in prod:
        pr = d1q(f'SELECT COUNT(*) AS n FROM "{t}"')[0]["n"]
        bb = con.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
        if pr == bb: same += 1
        else: diffs.append((t, pr, bb))
    ok = not missing
    result = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime()), "ok": ok,
              "scope": "L4-prod-read (read-only diff, no production write)",
              "file": os.path.basename(f), "tables_prod": len(prod), "tables_backup": len(bk),
              "rows_match": same, "rows_diff": diffs[:10], "backup_only_tables_missing": missing}
    print(("OK  " if ok else "FAIL") + f" prod {len(prod)} tables, rows match {same}/{len(prod)}" + (f", diff={diffs[:3]}" if diffs else ""))
    with open(LEDGER, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(result, ensure_ascii=False) + "\n")
    return result

if __name__ == "__main__":
    if "--prod-check" in sys.argv:
        r = prod_check()
    else:
        r = drill()
    sys.exit(0 if r.get("ok") else 1)
