#!/usr/bin/env python
"""workstation-check.py · 本机是否=双站工程化工作站的 9 项就绪自检
用法: python workstation-check.py    # 全绿=可直接开工; FAIL 项附修复指引
判定口径: 工作站=能读文档层 + 能跑守卫 + 能推送三仓 + 能调 GitHub API(隧道) 的机器。
"""
import json, os, re, socket, subprocess, sys, time
WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
res = []
def check(name, ok, fix=""):
    res.append({"item": name, "ok": bool(ok), "fix": fix if not ok else ""})

# 1. 文档层仓（sites-docs 布局: 本目录即 git 仓且有 origin）
r = subprocess.run(["git", "-C", WS, "ls-remote", "--heads", "origin", "main"],
                   capture_output=True, text=True, errors="replace", timeout=60,
                   env={**os.environ, "http_proxy": "http://127.0.0.1:3066", "https_proxy": "http://127.0.0.1:3066"})
check("1 文档层 sites-docs（远程 main 可达, 经 Karing）", bool(r.stdout.strip()), "git 需走 -c http(s).proxy=http://127.0.0.1:3066; Karing 服务未跑则先启 karingService")

# 2. 三仓在位
need = {"simishuwu": "AGENTS.md", "yunmengge-pages": "DEPLOY.md", "yunmengge-router": "api-manifest.json"}
for d, f in need.items():
    check(f"2 源仓 {d}（含 {f}）", os.path.isfile(os.path.join(WS, d, f)))

# 3. 核心文档件
for f in ["SITES-INDEX.md", "SITES-TREE.md", "sites.manifest.yaml", "docs-index.md", "decisions"]:
    check(f"3 文档件 {f}", os.path.exists(os.path.join(WS, f)))

# 4. Karing CONNECT 隧道活（127.0.0.1:3066）
try:
    socket.create_connection(("127.0.0.1", 3066), timeout=5).close()
    ok = True
except Exception:
    ok = False
check("4 Karing :3066 可达", ok, "启动 Karing（karingService / C:/Program Files/Karing/karingService.exe）")

# 5. GitHub token（.git-credentials）
tok = None
for cand in (os.path.expanduser("~/.git-credentials"),):
    try:
        for l in open(cand, encoding="utf-8", errors="replace"):
            m = re.match(r"https?://[^:]+:(\S+)@github\.com", l.strip())
            if m: tok = m.group(1)
    except OSError:
        pass
check("5 GitHub token（~/.git-credentials）", bool(tok), "git 曾推送 github 则 GCM 会自动写入; 否则手工配")

# 6. 守卫脚本可跑（本地副本, 允许缺失=非本 Hermes 机）
guard = os.path.join(os.path.dirname(os.path.dirname(WS)), "scripts", "sites-drift-guard.py")
check("6 漂移守卫（本机 Hermes 资产, 缺=只读工作站）", os.path.isfile(guard), "非 Hermes 主工作站可忽略")

# 7. 再生器 STABLE
r = subprocess.run([PY, os.path.join(WS, "tools", "regen-docs.py"), "--check"],
                   capture_output=True, text=True, errors="replace", timeout=180)
check("7 SITES-TREE 数据节 STABLE（regen --check）", r.returncode == 0, (r.stdout or r.stderr).strip()[:80])

# 8. GitHub API 隧道实测（GET /user）
r = subprocess.run([PY, os.path.join(WS, "tools", "karing-github-api.py"), "GET", "/user"],
                   capture_output=True, text=True, errors="replace", timeout=60)
check("8 GitHub API 隧道（karing-github-api GET /user=200）", "200" in (r.stdout or "")[:40], "Karing CONNECT 隧道未通: 看 item 4")

# 9. 活体双站（直连, 非代理）
for u, tag in [("https://33333344.xyz/api/health", "寻梦阁 API"), ("https://2244444.xyz/", "云梦阁首页")]:
    code = subprocess.run(["curl", "-s", "-o", "NUL", "-w", "%{http_code}", "--max-time", "20", u],
                          capture_output=True, text=True, errors="replace").stdout.strip()
    check(f"9 活体 {tag}（{code}）", code == "200", "双站宕机或本机到 CF 出网异常; 判活三视角勿单点定论")

# 10. 本地盘量预算（E 盘 free >= 20G, 防盘满=全 cron 死）
r = subprocess.run("powershell -NoProfile -Command \"(Get-PSDrive E).Free/1GB\"",
                   shell=True, capture_output=True, text=True, errors="replace", timeout=30)
try:
    free_gb = float(r.stdout.strip().splitlines()[-1])
except Exception:
    free_gb = -1
check(f"10 E 盘余量预算（free {free_gb:.0f}G >= 20G）", free_gb >= 20, "E 盘将满: 按 workspace.layout.yaml 保留期缺口清理(backups/output/cache)")

# 11. 布局契约 + 保留期审计（workspace.layout.yaml 无漂移）
r = subprocess.run([PY, os.path.join(WS, "tools", "retention-audit.py"), "--check"],
                   capture_output=True, text=True, errors="replace", timeout=120)
check("11 本地布局契约（retention-audit --check, 新目录须入 workspace.layout.yaml）", r.returncode == 0, (r.stdout or r.stderr).strip()[-120:])

bad = [x for x in res if not x["ok"]]
print(json.dumps({"workstation": "READY" if not bad else "DEGRADED",
                 "pass": len(res) - len(bad), "total": len(res),
                 "failed": [x["item"] for x in bad],
                 "fixes": [{"item": x["item"], "fix": x["fix"]} for x in bad]}, ensure_ascii=False, indent=1))
sys.exit(0 if not bad else 1)
