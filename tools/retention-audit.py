#!/usr/bin/env python
# retention-audit.py · 本地工作区保留期审计（机读契约核）
# 用法: python retention-audit.py            # JSON 报告
#       python retention-audit.py --check    # 断言模式: 全绿 rc=0 / 有漂移 rc=1
# 断言面: ① 布局漂移(layout.yaml 条目 vs 实际顶层目录) ② 盘量预算(E 盘 free>=20G) ③ 保留期缺口清单(报告, 不 FAIL)
import json, os, sys, re, time, subprocess

ROOT = r"E:/hermes"
LAYOUT = r"E:/hermes/workspace-repos/workspace/workspace.layout.yaml"

def parse_layout(text):
    entries = []
    for line in text.splitlines():
        m = re.match(r"\s*- \{dir: ([^,]+), layer: ([^,]+), mb: ([^,]+), files: (\d+), retention: '([^']*)', gap: (true|false)\}", line)
        if m:
            entries.append({"dir": m.group(1), "layer": m.group(2), "mb": float(m.group(3)),
                            "files": int(m.group(4)), "retention": m.group(5), "gap": m.group(6) == "true"})
    return entries

def main(check_mode):
    text = open(LAYOUT, encoding="utf-8").read()
    entries = parse_layout(text)
    assert entries, "layout.yaml 解析 0 条=格式破坏"
    dirs_in_yaml = {e["dir"] for e in entries}
    actual = set()
    for d in os.listdir(ROOT):
        if os.path.isdir(os.path.join(ROOT, d)):
            actual.add(d)
    missing = sorted(actual - dirs_in_yaml)          # 新目录未入契约=漂移
    stale = sorted(dirs_in_yaml - actual)             # 契约有盘上无=陈旧
    # 盘量预算
    r = subprocess.run("powershell -NoProfile -Command \"(Get-PSDrive E).Free/1GB\"",
                       shell=True, capture_output=True, text=True, timeout=30)
    try:
        free_gb = float(r.stdout.strip().splitlines()[-1])
    except Exception:
        free_gb = -1
    # 保留期缺口（报告，不 FAIL）
    retention_gaps = [e["dir"] for e in entries if e["gap"]]

    # change gate 完整性验证
    _change_entries = []
    try:
        with open(r"E:/hermes/output/gate-checks.jsonl", encoding="utf-8") as _gf:
            for _line in _gf:
                if not _line.strip():
                    continue
                try:
                    _o = json.loads(_line)
                except Exception:
                    continue
                if _o.get("type") == "change":
                    _change_entries.append(_o)
    except Exception:
        pass
    change_gate_valid = all(
        bool(e.get("subject") and e.get("affected_dirs") and e.get("reason") and e.get("evidence"))
        for e in _change_entries
    )

    report = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "layout_entries": len(entries),
        "actual_top_dirs": len(actual),
        "drift_new_uncontracted": missing,
        "drift_stale_contract": stale,
        "disk_free_gb": round(free_gb, 1),
        "disk_budget_gb": 20,
        "disk_ok": free_gb >= 20,
        "retention_gaps": retention_gaps,
        "change_gates_total": len(_change_entries),
        "change_gate_valid": change_gate_valid,
    }

    if not check_mode:
        print(json.dumps(report, ensure_ascii=False, indent=1))
        return 0
    fails = []
    if missing:
        fails.append(f"布局漂移: {len(missing)} 个新目录未入契约 {missing[:6]}")
    if stale:
        fails.append(f"契约陈旧: {stale[:6]} 已删")
    if not report["disk_ok"]:
        fails.append(f"E 盘 free {report['disk_free_gb']}G < 20G 预算")
    print(json.dumps(report, ensure_ascii=False, indent=1))
    if fails:
        print("[DRIFT] " + " | ".join(fails))
        return 1
    print("[OK] 布局/盘量断言全绿（保留期缺口仅报告, 不 FAIL; change gate " + str(report["change_gates_total"]) + " 条）")
    return 0

if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))
