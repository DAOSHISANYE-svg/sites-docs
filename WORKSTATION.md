# WORKSTATION.md · 把一台机器变成双站工程化工作站的 onboarding

> 配套：docs-index.md（文档体系）· decisions/ADR-007（GitHub API 隧道）· tools/workstation-check.py（9 项自检）

## 工作站 = 什么
能**读文档层 + 跑守卫 + 推三仓 + 调 GitHub API（隧道）**的机器。最小集=本仓 + Karing 服务 + GitHub token；完整工作站（含每日巡检 cron/输出账本）= 本机 E:/hermes 资产。

## Onboarding（任意新机 10 分钟）
1. **克隆四仓**（git 需经 Karing `http://127.0.0.1:3066` 代理；Karing=Windows 服务 karingService，无则先装）：
   ```
   <ws>\> git clone -c http.proxy=http://127.0.0.1:3066 https://github.com/DAOSHISANYE-svg/{sites-docs,simishuwu,yunmengge,yunmengge-router}
   布局: <ws>\sites-docs 为文档层仓(本仓), 三源仓同级; 本仓 tools/ 脚本按 <ws> 根布局运行
   ```
2. **GitHub token**：GCM 自动（曾推过 github）或 `~/.git-credentials` 一行 `https://<user>:<token>@github.com`。
3. **就绪自检（一条命令）**：
   ```
   python <ws>\sites-docs\tools\workstation-check.py
   ```
   全绿=READY；FAIL 项自带修复指引（Karing 未跑/token 缺/再生漂移/活体异常）。

## 日常操作速查
| 动作 | 命令 |
|---|---|
| 树图数据节再生 | `python tools/regen-docs.py`（--check=只测漂移） |
| 漂移守卫（33 断言） | `python <hermes>/scripts/sites-drift-guard.py`（Hermes 工作站; cron 每日 9/21） |
| GitHub API（建仓/查 CI/查仓） | `python tools/karing-github-api.py GET /repos/DAOSHISANYE-svg/<仓>` |
| 推仓 | `git -c http.proxy=http://127.0.0.1:3066 -c https.proxy=http://127.0.0.1:3066 push` |
| 判活 | 三视角：直连 curl / Karing / CF dashboard；**代理 000 ≠ 宕机**（ADR-005） |
| 部署后验证 | CF 边缘缓存 60-90s 窗口，带 `?v=ts` 复检（ADR-005） |

## 红线（动手前必读 AGENTS.md + ADR-004/006）
- 内容零改动（双站既有文案/题面=报告制）· 密钥只走槽位 [SECRET-*] · 发布面零垃圾（_dev-archive 不入库不发布）
- 告警型脚本：检出=告警写文件+exit0（ADR-006）· 本机 GitHub API 一律走 Karing CONNECT 隧道，勿试直连/gh 浏览器流（ADR-007）

## 资产台账 · 本机（workstation #1）
| 项 | 值（2026-10-25 实测） |
|---|---|
| 主机 | DESKTOP-VKKOMGP · Windows · 用户 junji（=公司工作站 #1） |
| 数据根 | `E:/hermes`（HERMES_HOME：75 顶层目录，分组全树见 MACHINE-TREE.md）；E 盘已用 ≈50.8G |
| 网络服务 | Karing `karingService.exe`（:3066，计划任务 **Karing Autorun** 自启，双进程）；LLM 网关 **:8430** 在跑 |
| 自动化 | `hermes cron` 61 任务（含 sites-drift-guard-cron 02852915324d 每日 9/21 巡检） |
| 安全防线 | `E:/hermes/llm-key-gateway/` 只读核心 7 文件（目录共 61 件，10-24 主人令，改动=六步流程+_sha_drift）；密钥 `config/keys/.cf_token` + GitHub GCM token 仅槽位引用 |
| 备份纪律 | `backups/` 7 天滚动；`scattered-bak` 安全网 2026-11-08 期满且无事故→归档压缩删（排程） |
| 真机 | adb `RCUUO4DNN9XRO5PQS`（IP 不在 192.168.2.x 时白屏，走 adb） |
维护规则：改动只走仓+gate；本机故障≠站点故障（双站在 CF，本机只影响工程链，非发布链）。

### 软件层（本机安装，2026-10-25 实测版本）
| 软件 | 版本 | 位置/用途 |
|---|---|---|
| Karing | karingService.exe | `C:/Program Files/Karing/`，:3066 git/CONNECT 隧道服务（自启） |
| GitHub CLI | gh 2.102.0 | 系统 PATH |
| Node.js | v26.7.0（PATH）/ 26.12.1（tools） | `E:/hermes/tools/node-*` |
| npm | 12.0.2 | `E:/hermes/tools/npm-*` |
| Python | 3.14.9（PATH）/ 3.14.7（tools） | `E:/hermes/tools/python-*`；uv 运行器 0.12.3/0.13.5 |
| git | 2.53.0 | 系统 PATH |
| ffmpeg | 8.1.1（PATH）/ 9.0.1（tools） | `E:/hermes/tools/ffmpeg-*` |
| ripgrep | 15.2.0 | `E:/hermes/tools/ripgrep-*` |
| agent-browser | 0.26.0 | `E:/hermes/tools/`（无头浏览器/走查） |
| chromium | 1208 | `E:/hermes/tools/chromium-1208/` |
| cua-driver | 0.21.0 | `E:/hermes/tools/`（桌面视觉） |
| Hermes 本体 | — | `E:/hermes/`（73 顶层目录，含 venv `installs/`、cron、skills、tools） |
| LLM 网关 | :8430 | `E:/hermes/llm-key-gateway/`（只读防线，10-24 主人令） |
| adb | platform-tools | 真机 RCUO4DNN9XRO5PQS 调试 |
版本规则：`E:/hermes/tools/` 为本地工具箱（多版本并存，PATH 取其一）；脚本统一走 uv 的 cpython-3.11 运行器（见 workstation-check 的 PY 变量），避免系统 3.14 与脚本语法漂移。

## 变更治理门禁（Change Gate Protocol）

**规则**：对以下文件的任意编辑，**必须**先创 `change` 类型 gate record，编辑后再写入 `result`/`evidence`。

| 受保护文件 | 路径 |
|---|---|
| 布局契约 | `workspace.layout.yaml` |
| 机器树 | `MACHINE-TREE.md` |
| 事故手册 | `RUNBOOK.md` |
| 文档索引 | `docs-index.md` |
| 保留期审计 | `tools/retention-audit.py` |
| 工作站检查 | `tools/workstation-check.py` |

**Gate record 模板**（type=change）：
```json
{
  "ts": "<ISO8601>",
  "writer": "<agent 名>",
  "type": "change",
  "subject": "编辑 workspace.layout.yaml 保留期策略",
  "affected_dirs": ["backups", "output"],
  "reason": "backups 53 子目录在 GC 外，需标记 gap",
  "evidence": "git diff --stat HEAD~1..HEAD workspace.layout.yaml",
  "result": "success"
}
```

**断言位置**：`retention-audit.py --check` 自动检测 `change_gates_total` 并验证每条含 `subject/affected_dirs/reason/evidence`；缺失任何字段则 `change_gate_valid: false`（报告，不 FAIL）。
