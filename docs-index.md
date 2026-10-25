# docs-index.md · 双站文档系统总索引
> 本文件随文档仓 `DAOSHISANYE-svg/sites-docs`（https://github.com/DAOSHISANYE-svg/sites-docs）版本化。（indexed-or-it-doesn't-exist）
> 生成 2026-10-25 · 规则：每个文档恰好一个家（one home per fact）；新增文档必须入本索引。

## 入口层（活体，其他 AI 第一跳）
| 文档 | 回答的唯一问题 | 位置 |
|---|---|---|
| llms.txt | 这个站有什么/怎么调/红线在哪 | 双仓根（活体 /llms.txt） |
| CLAUDE.md | Claude 系工具读哪 | 三仓根（指针） |
| AGENTS.md | 在此仓动手的纪律 | 三仓根 |

## 地图层（workspace，跨站）
| 文档 | 唯一问题 | 位置 |
|---|---|---|
| SITES-INDEX.md | 资源拓扑/依赖顺序/密钥槽/已知 P0 | workspace/ |
| SITES-TREE.md | 双站有哪些页/端点/表（页级结构） | workspace/（regen-docs 可再生） |
| sites.manifest.yaml | 机器可读资源清单（守卫断言源） | workspace/ |
| docs-index.md | 每个文档的家在哪 | workspace/ |
| decisions/ADR-00X | 为什么这样设计（6 条，见下） | workspace/decisions/ |
| B8 报告（19 项定夺） | 哪些内容项等主人定夺 | C:/Users/junji/.hermes/output/xmg-b8-content-qa-report.md |

## 执行层（各仓）
| 文档 | 唯一问题 |
|---|---|
| DEPLOY.md ×3 | 新账号如何复刻部署本件 |
| api-manifest.json（router） | /api 契约（58 exact+7 prefix，权威） |
| migrations/SCHEMA.md（router） | D1 表结构权威 |

## 守卫层（机器）
| 资产 | 职责 |
|---|---|
| sites-drift-guard.py + cron 02852915324d | 机器断言：文档声明 vs 活体现实（全量见脚本输出）（仓名/同步/发布面/活体/CF 项目） |
| 双仓 Pages deploy.yml 三道门（ci-xss-gate + frontend-deps-check 前置门, nav-smoke 后置门）/ router CI smoke→promote | 部署=带自验证（防"push≠上线"与"路由抖动环"回归） |

## ADR 列表（append-only，supersede 不改史）
- 001 零 build CF Pages · 002 共享 D1 site 列 · 003 结果键 5 套并存（待定夺）· 004 内容零改动红线 · 005 Karing 代理+90s 窗口 · 006 告警走文件+exit0 · 007 GitHub API 走 Karing CONNECT 隧道（本机 github 段直连全阻）

## 明确不做（防双家漂移）
- agent.json（/.well-known）= sites.manifest.yaml 的活体副本 → 违反 one home，不做；活体 agent 入口=llms.txt
- SITES-TREE 手工副本进仓 → 违反单一真源；树只在 workspace（regen 再生）
