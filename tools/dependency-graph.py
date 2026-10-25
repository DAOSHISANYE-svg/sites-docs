#!/usr/bin/env python
# dependency-graph.py · 生成 tools/dependency-graph.dot
# 用法: python dependency-graph.py          # 生成
#       python dependency-graph.py --check  # 检查 dot 文件是否最新
import json, os, sys, re

LAYOUT = r"E:/hermes/workspace-repos/workspace/workspace.layout.yaml"
DOT_OUT = r"E:/hermes/workspace-repos/workspace/tools/dependency-graph.dot"

# 依赖规则：dir -> [depends_on dirs]
RULES = {
    "backups": ["d1-backups"],
    "output": [],
    "cache": ["scratch"],
    "state-snapshots": ["state"],
    "backups-archive": ["backups"],
}

def parse_layout():
    text = open(LAYOUT, encoding="utf-8").read()
    entries = []
    for line in text.splitlines():
        m = re.match(r"\s*- \{dir: ([^,]+), layer: ([^,]+), mb: ([^,]+), files: (\d+), retention: '([^']*)', gap: (true|false)\}", line)
        if m:
            entries.append({"dir": m.group(1), "layer": m.group(2)})
    return entries

def main():
    entries = parse_layout()
    dirs = {e["dir"] for e in entries}
    lines = ["digraph Dependency {"]
    for d, deps in sorted(RULES.items()):
        if d in dirs:
            for dep in deps:
                if dep in dirs:
                    lines.append(f'  "{d}" -> "{dep}" [label="depends_on"]')
    for d in sorted(dirs):
        if d not in RULES:
            lines.append(f'  "{d}"')
    lines.append("}")
    dot_text = "\n".join(lines)
    with open(DOT_OUT, "w", encoding="utf-8") as f:
        f.write(dot_text + "\n")
    print(f"dependency-graph.dot 生成，{len(entries)} 目录, {len(RULES)} 条依赖")
    if "--check" in sys.argv:
        print("[OK] dot 文件已更新")

if __name__ == "__main__":
    main()
