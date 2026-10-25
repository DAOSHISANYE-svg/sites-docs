#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""backup-integrity-check.py — 备份 L2/L3 完整性验证（industry: 4-level confidence, 见 ADR-009）

L1 it ran      — 已覆盖（cron 日志 + 守卫 §13 新鲜度）
L2 plausible   — 文件存在 + 非空 + 头部可解析（CREATE TABLE 计数）
L3 intact      — sha256 记录入账（证明"测过的=保留的"）+ 与上次尺寸对比（膨胀/截断告警）
L4 restores    — 真恢复：需 D1 读写 scope（当前 token 受限）→ 升级触发条件（ADR-009）

运行：python backup-integrity-check.py            # 验最新 3 个 SQL + 入账
      python backup-integrity-check.py --archive  # 额外验 backups-archive/*.tar.gz 可列
ledger：E:/hermes/output/backup-integrity.jsonl（append-only）
"""
import os, re, json, time, hashlib, tarfile, subprocess, sys

D1DIR = r"E:/hermes/d1-backups"
ARC = r"E:/hermes/backups-archive"
LEDGER = r"E:/hermes/output/backup-integrity.jsonl"
NOW = time.time()

def sha256_file(p, chunk=1 << 20):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

def sql_check(p, tag, do_ledger):
    st = os.stat(p)
    name = os.path.basename(p)
    head = open(p, encoding="utf-8", errors="replace").read(200_000)
    creates = len(re.findall(r"CREATE TABLE", head))
    ok = st.st_size > 10_000 and creates >= 1
    rec = {
        "ts": NOW, "level": 3, "tag": tag, "file": name,
        "size": st.st_size, "create_tables": creates,
        "sha256": sha256_file(p), "ok": bool(ok),
    }
    # 与上次同 tag 尺寸对比（膨胀>30% 或截断>50% 告警；日更 SQL 相邻条目=前一日）
    prev = None
    if os.path.exists(LEDGER):
        for line in reversed(list(open(LEDGER, encoding="utf-8"))):
            try:
                o = json.loads(line)
                if o.get("tag") == tag and o.get("ok") and o.get("ts", 0) < NOW:
                    prev = o
                    break
            except Exception:
                pass
    if prev:
        ratio = rec["size"] / max(1, prev["size"])
        rec["size_ratio_vs_prev"] = round(ratio, 3)
        if ratio > 1.3 or ratio < 0.5:
            rec["anomaly"] = "size-drift"
    if do_ledger:
        with open(LEDGER, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"  [{'OK' if ok else 'FAIL'}] L3 {name} {rec['size']}B creates={creates} sha256={rec['sha256'][:16]}...")
    return ok

def archive_check(tag, do_ledger):
    oks = True
    if not os.path.isdir(ARC):
        print(f"  [SKIP] no {ARC}")
        return True
    for f in sorted(os.listdir(ARC)):
        if not f.endswith(".tar.gz"):
            continue
        p = os.path.join(ARC, f)
        try:
            names = tarfile.open(p, "r:gz").getnames()
            rec = {"ts": NOW, "level": 3, "tag": tag, "file": f, "entries": len(names),
                   "sha256": sha256_file(p), "ok": len(names) > 0}
            if do_ledger:
                with open(LEDGER, "a", encoding="utf-8") as ff:
                    ff.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(f"  [OK] L3 {f} {rec['entries']} entries sha256={rec['sha256'][:16]}...")
        except Exception as e:
            print(f"  [FAIL] L3 {f}: {e}")
            oks = False
    return oks

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ("--archive", "--quiet") else ""
    archive = "--archive" in sys.argv or mode == "--archive"
    ledger_write = "--quiet" not in sys.argv
    all_ok = True
    sqls = sorted([f for f in os.listdir(D1DIR) if f.endswith(".sql")], key=lambda x: os.stat(os.path.join(D1DIR, x)).st_mtime) if os.path.isdir(D1DIR) else []
    if not sqls:
        print("[FAIL] no .sql in " + D1DIR)
        sys.exit(1)
    for f in sqls[-3:]:
        all_ok &= sql_check(os.path.join(D1DIR, f), "d1-latest", ledger_write)
    if archive:
        all_ok &= archive_check("archive", ledger_write)
    print("[OK] backup integrity L2/L3 passed" if all_ok else "[FAIL] backup integrity issues")
    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()
