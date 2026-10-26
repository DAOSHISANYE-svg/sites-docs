# ADR-009 · 备份恢复演练的分级置信模型 + llms.txt v2 对齐 + AGENTS.md 自查命令

日期：2026-10-25　状态：accepted（部分 blocked-on-scope）

## 背景
全网搜索（backup restore drill / postmortem / llms.txt v2 / AGENTS.md）发现三条工程纪律，对照双站规模取舍：
1. **备份 4 级置信**（L1 跑了 → L2 合理 → L3 完好 → L4 可真恢复）。多数团队停在 L1（只信 exit 0）就自认 L4。D1 双站共库，`d1-backups/*.sql` 每日 03:00 落盘，但**从未验证过能否真恢复**。
2. **llms.txt v2**（2026-08 修订）：强要求 = H1 + 一句 blockquote 摘要；可发现性 = HTML 页带 `Link: </llms.txt>; rel="describedby"` 头（`_headers` 注入）。
3. **AGENTS.md**（Linux Foundation AAIF 标准）：最高杠杆 = 写一条"agent 自查自身改动的命令"，让 agent 能自我验证。

## 决策

| 项 | 决定 | 理由 |
|---|---|---|
| 备份 L2/L3 廉价完整性 | ✅ 落地 `tools/backup-integrity-check.py`（非空 + 头部可解析 + CREATE TABLE/行数计数 + sha256 记录 + 与上次尺寸对比告警），挂守卫 §14 + cron 每日 | L2/L3 便宜，应每跑都做；纯静态，不需 DB 连接 |
| 备份 L4 真恢复演练 | ⏸ blocked-on-scope | 需 D1 读写 token 建 scratch 库并 `sqlite3 < backup.sql` + 行数对生产。当前 token 无 D1 写 scope（ADR-008 已记 scope 受限）。升级触发=拿到 D1 读写 scope |
| llms.txt blockquote 摘要 | ✅ 两站已补 | v2 唯一强要求 |
| `_headers` 加 `Link: describedby` | ⏸ vendor-blocked（已撤行） | 实测 CF Pages _headers 不投递 Link 响应头（3+min 全路径 0 命中，同块 X-Frame-Options 生效）；替代方案=/llms.txt 直达+AGENTS.md 指路（已做）。升级触发=CF 放开或改走 _middleware.js 注头（成本高，暂不做） |
| AGENTS.md 自查命令 | ✅ 三仓各补 1 块 | 让 agent 改完能一条命令自验 |

## 升级触发（何时重开）
- **D1 备份 L4**：拿到带 D1 `edit` scope 的 token → 写 `backup-restore-drill.py`（scratch sqlite + 行数对账 + RTO 计时），入 cron 季度 + ADR 记 RTO 基线。
- **llms.txt**：站点若改多子路径 → 按 v2「最具体路径文件生效」拆 `/docs/llms.txt`。
- **AGENTS.md**：若某仓指令 >100 行 → 拆嵌套 AGENTS.md（closest-file-wins）。

## 影响
- 新增 `tools/backup-integrity-check.py`（sites-docs）+ cron 每日 + 守卫 §14 断言"备份完整性台账 ≤30h"。
- `d1-backups/` 保留 7 天滚动（与 backup log 一致）；integrity 台账 append-only 到 `output/backup-integrity.jsonl`。

## 补充（2026-10-26 24:0x · L4 破局）
- **L4 原定义 "真恢复需 D1 写 scope = blocked-on-scope" 已破**，拆为三级：
  - **L4-local（已闭环）**：`tools/d1-restore-drill.py` 把最新备份 SQL 灌入全新 SQLite :memory:，断言全语句可执行 + 25 表 + 行数抽检。cron `c48818593733` 每日 04:30。
  - **L4-prod-read（已闭环）**：`--prod-check` 模式用 `config/keys/.env` 的 `CLOUDFLARE_API_TOKEN`（cfut_，实证 D1 读权限）做 备份↔生产 D1 表结构+行数只读对照，首跑 **25/25 表 + 行数全一致**。cron `928ec17f944a`（wrapper `d1-restore-drill-prod.py`）每日 04:35。
  - **L4-prod-write（保留为不可逆末手段）**：把备份写回生产 D1。不自动化；触发=主人一句授权 + RUNBOOK "D1 恢复（末手段）"节执行；执行前必做 L4-local+L4-prod-read 双绿。
- 密钥事实：`CLOUDFLARE_API_TOKEN`（.env L39，wrangler deploy 用）具备 D1:read（200 列出 xunmengge-db/mysite-db）+ Pages:read；写 D1 权限未授（本 ADR 不假设，末手段执行时实探 401 即回退申请）。
