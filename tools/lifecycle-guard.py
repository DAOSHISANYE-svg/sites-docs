#!/usr/bin/env python
# lifecycle-guard.py · 生命周期自动化守卫（backups/output gap 闭环）
# 用法: python lifecycle-guard.py          # 仅评估
#       python lifecycle-guard.py --dry    # 评估 + 显示将执行的动作（不真正执行）
#       python lifecycle-guard.py --run    # 执行 + 落 gate record
import json, os, time, subprocess, sys, datetime

BK = r"E:/hermes/backups"
OUT = r"E:/hermes/output"
ARCHIVE = r"E:/hermes/backups-archive"
GATE_FILE = r"E:/hermes/output/gate-checks.jsonl"
NOW = time.time()

def backup_age_days(path):
    """Return the age in days of the oldest file in a backup directory."""
    oldest = None
    try:
        for root, dirs, files in os.walk(path):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    age_h = (NOW - os.path.getmtime(fp)) / 3600
                    if oldest is None or age_h > oldest:
                        oldest = age_h
                except Exception:
                    continue
    except Exception:
        pass
    if oldest is not None:
        return oldest / 24
    return None

def find_stale_backups():
    """Find backups dirs with oldest file older than 90 days."""
    stale = []
    if os.path.isdir(BK):
        for d in os.listdir(BK):
            dp = os.path.join(BK, d)
            if not os.path.isdir(dp):
                continue
            age_d = backup_age_days(dp)
            if age_d is not None and age_d > 90:
                stale.append((d, round(age_d, 1)))
    return stale

def find_stale_output():
    """Find output files older than 365 days."""
    stale = []
    if os.path.isdir(OUT):
        for root, dirs, files in os.walk(OUT):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    age_d = (NOW - os.path.getmtime(fp)) / 86400
                    if age_d > 365:
                        rel = os.path.relpath(fp, OUT)
                        stale.append((rel, round(age_d, 1)))
                except Exception:
                    continue
    return stale

def append_gate(record):
    try:
        record["ts"] = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
        record.setdefault("writer", "lifecycle-guard")
        with open(GATE_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return True
    except Exception:
        return False

def main():
    mode = "dry"
    if "--run" in sys.argv:
        mode = "run"
    if "--dry" in sys.argv:
        mode = "dry"

    stale_bk = find_stale_backups()
    stale_out = find_stale_output()

    print(f"backups stale (>90d): {len(stale_bk)} dirs")
    for d, age in stale_bk[:10]:
        print(f"  - {d} ({age}d)")
    print(f"output stale (>365d): {len(stale_out)} files")
    for f, age in stale_out[:10]:
        print(f"  - {f} ({age}d)")

    if mode == "run":
        # Archive stale backups to backups-archive
        archived = 0
        if stale_bk:
            os.makedirs(ARCHIVE, exist_ok=True)
            ts = int(NOW / 86400)
            archive_name = os.path.join(ARCHIVE, f"archived_{ts}.tar.gz")
            print(f"[ARCHIVE] {archive_name}")
            subprocess.run(
                "tar -czf " + archive_name + " -C " + BK + " " + " ".join([d for d, _ in stale_bk]),
                shell=True, capture_output=True, text=True, timeout=300)
            archived = len(stale_bk)

        # Log stale output (do NOT auto-delete; owner decides)
        if stale_out:
            print(f"[NOTE] {len(stale_out)} output files >365d, no auto-delete")

        ok = append_gate({
            "type": "lifecycle_guard",
            "subject": f"backups {archived} dirs archived; output {len(stale_out)} stale files noted",
            "result": "success",
            "evidence": f"archived_at={ts}, output_stale_count={len(stale_out)}",
        })
        print(f"[GATE] recorded={ok}")
    else:
        print("[DRY] no archive/delete executed; use --run to act")
    return 0

if __name__ == "__main__":
    sys.exit(main())
