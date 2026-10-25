# Incidents 索引（blameless postmortem 台账）

> 规则：P0/P1 事故与重大误报自纠，48h 内落一页 postmortem（`incidents/YYYY-MM-DD-<slug>.md`）+ 本索引一行。
> 文化：blameless——归因到**允许它发生的系统**，不归咎个人；误报自纠（gate `redline_self_correction`）同样入册。

## Postmortem 五段式（模板）

```markdown
# <标题>（P0/P1，YYYY-MM-DD）
## 1. 影响面   — 哪些页面/用户流/服务受损，时长，波及数据
## 2. 时间线   — 从发现到闭环的关键节点（ISO 时间）
## 3. 根因     — 系统层面（机制缺口/工具静默失败/假设未验证），非"谁操作错了"
## 4. 处置     — 实际执行的动作 + 证据（commit/curl/gate seq）
## 5. 行动项   — open AIs 表（下表登记），每项带 owner + 期限，到期复核
```

## Open Action Items（未闭环即挂此表，季度复核）

| AI | 来源 | 描述 | owner | 期限 | 状态 |
|---|---|---|---|---|---|
| AI-001 | 2026-10-25 V1 自纠 | manifest host_map 缺 host 面声明 | Hermes | 2026-10-25 | ✅ 已闭环（router 55e7375） |
| AI-002 | 2026-10-25 V3 | Karing Autorun 仅 Logon 触发器 | Hermes | 2026-10-25 | ✅ 已闭环（Logon+Boot 双触发） |
| AI-003 | 2026-10-25 全盘扫描 | cron 脚本存在性无守卫（P3） | Hermes | 开放 | ⬜ Open（记待办） |
| AI-004 | 2026-10-25 ADR-009 | D1 备份 L4 恢复演练受 token scope 阻塞 | 主人 | 开放 | ⬜ Open（升级触发：获取 D1 读写 scope） |

## 已有事故（gate 溯源）

- 2026-10-25 复盘批：V1/V2 误报自纠（gate `redline_self_correction` seq 1792918459876 等）
- 2026-10-24 lifecycle-guard 虚假 success（gate seq 1792918545225）
- 事故全量账本：`E:/hermes/output/gate-checks.jsonl`（type=redline_self_correction / redline_violation 行）
