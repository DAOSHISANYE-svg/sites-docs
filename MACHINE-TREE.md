# MACHINE-TREE.md · 本机工作树（workstation #1 = DESKTOP-VKKOMGP）
> 生成 2026-10-25 实测（dir 清点/netstat/schtasks/hostname）。用途：本机全量资产视图；WORKSTATION.md 台账=本篇摘选。
> 纪律：只注已实证用途；未实证=标"未注"；凭据只标槽位不落值。

## 1. 数据层 `E:/hermes`（HERMES_HOME，77 顶层目录）
### 1.1 核心运行面（高频）
- `cron/`(14) 定时任务注册+输出 · `cron-memory/`(13) 跨会话记忆
- `skills/`(88) 技能库 · `plugins/`(4) · `profiles/`(7) 多 profile
- `state/`(5) `state-snapshots/` `checkpoints/`(1) `locks/` 运行状态
- `logs/`(26) `output/`(4803 件, 交付物+gate 账本 gate-checks.jsonl) `sessions/`(41)
- `team/`(54) 团队资产 · `kanban/`(6) · `gates/`(2) · `checklists/`(4)
- `config/`(10) 配置 · **`config/keys/.cf_token`**（CF API token 槽位）
- `bot_relay/`(4) `bot-groups/`(312) 群发/卡片链 · `pending/`(1) `pending_messages/`(0)
### 1.2 工程面
- **`workspace-repos/workspace/`(1)** = 四仓（sites-docs 即此目录 git 仓 + simishuwu/yunmengge-pages/yunmengge-router）
- `workspace/`(2) · `sandboxes/`(1) · `runtime/`(3) · `hooks/`(2) · `lsp/`(4)
- `hermes-agent/`(147) 本体 · `hermes-tools/`(128) 团队工具（guard/门/脚本） · `scripts/`(154) 脚本双副本层
- `tools/`(15) 工具箱（node/python/git/ffmpeg/rg/uv/agent-browser/chromium/cua-driver，版本清单见 WORKSTATION.md 软件层）
- `bin/`(15) · `node/`(13) · `installs/`(1, venv) · `platforms/`(1) · `templates/`(5)
### 1.3 QA/审计面
- `qa-d-audit/`(70) `qa-screenshots/`(1) `screens/`(170) `visual-qa/`(1) `source-checks/`(2) `plugin-update-checks/`(2)
### 1.4 数据/备份面
- `backups/`(75, 7 天滚动) `backups-archive/`(0) `d1-backups/`(18) `snapshots/`(1)
- `memory/`(2) `memories/`(7) `memory-tencentdb-data/`(7) `vault/`(0)
### 1.5 缓存/临时面（可清）
- `cache/`(54) `scratch/`(138) `tmp/`(15) `__pycache__/` `bootstrap-cache/` `image_cache/`(0) `audio_cache/`(0) `pets/`(0) `proxy/`(0) `pairing/`(0) `profile/`(1) `references/`(1) `assets/`(6) `agents/`(6) `gateway/`(1) `gateway-service/`(5) `desktop/`(0) `desktop-plugins/`(4) `test-bot-workspace/`(1) `skill-bundles/`(1) `nachos/`(1)

## 2. C 盘用户层（`C:/Users/junji`）
- `.git-credentials`（GitHub GCM token 槽位，gho_ OAuth，~8h 时效自动刷新）
- `.workbuddy/`（WorkBuddy 插件市场；four-perspective-review 团队名册）
- `.config/` · `AppData/Roaming/uv/python/cpython-3.11-*`（**脚本统一 3.11 运行器**）
- `Program Files/Karing/`（karingService.exe + karing.exe）

## 3. 服务/端口面（2026-10-25 netstat 快照）
| 端口 | 判定 |
|---|---|
| 127.0.0.1:3066 | Karing git/CONNECT 隧道（自启 Karing Autorun） |
| 0.0.0.0:4066/4067/5040 + 49664-49670/49672/49673 | 本机多进程监听（Karing 系多端点+其他；未逐一归因=快照留痕） |
| 127.0.0.1:18488/3057/3065/3067/39099 | 未归因（快照） |
| 0.0.0.0:8430 | LLM key-rotation 网关（只读防线，六步流程） |
| 135/445 等 | Windows 系统端口（非资产） |

## 4. 自动化面
- Windows 计划任务：**Karing Autorun**（自启 Running）
- `hermes cron` 61 任务（含 sites-drift-guard-cron 02852915324d 每日 9/21）
- 每日 21:00 work-retro · 审计链 60min 断链红线

## 5. 外部资产绑定
- 真机 adb `RCUO4DNN9XRO5PQS`（IP 不在 192.168.2.x 时白屏）
- 双站 CF（33333344.xyz / 2244444.xyz）+ Worker + D1/KV（本机只工程，不托管）
- GitHub 4 仓（DAOSHISANYE-svg/{sites-docs,simishuwu,yunmengge,yunmengge-router}）

## 6. 与文档层关系
本机 = workstation #1；本树=全量；WORKSTATION.md 台账=摘选+规则；新增目录/服务/端口=更新本篇（regen 风格，勿散落三处）。
