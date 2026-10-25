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
| decisions/ADR-00X | 为什么这样设计（7 条，见下） | workspace/decisions/ |
| B8 报告（19 项定夺） | 哪些内容项等主人定夺 | C:/Users/junji/.hermes/output/xmg-b8-content-qa-report.md |

| WORKSTATION.md | 把一台机器变成双站工作站（onboarding 10 分钟） | workspace/（sites-docs 仓） |
| tools/workstation-check.py | 本机就绪 9 项自检（一条命令） | sites-docs 仓 |
| tools/karing-github-api.py | GitHub REST API（Karing CONNECT 隧道） | sites-docs 仓（ADR-007） |

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
| RUNBOOK.md | 事故手册（8 故障模式四段式 + 不可逆即报） | sites-docs 仓 |
| decisions/ADR-008 | 重工具链取舍（Terraform/Pyrra/OpenAPI/混沌，评估不引入+升级触发） | sites-docs 仓 |
| integrate.json | org 级 agent 入口（repos/docs/tools/slo/redlines map） | sites-docs 仓 |
| workspace.layout.yaml | E:/hermes 77 顶层目录布局契约(层/保留期/缺口, 机读) | sites-docs 仓 |
| tools/retention-audit.py | 布局漂移+盘量预算+保留期缺口+change gate 完整性断言(--check) | sites-docs 仓 tools/ |
| tools/lifecycle-guard.py | 生命周期守卫(backups 90 天归档/output 365 天标记, --dry/--run) | sites-docs 仓 tools/ |
| tools/dependency-graph.py | 目录依赖图谱(--check 再生 dependency-graph.dot) | sites-docs 仓 tools/ |
| E:/hermes/output/slo-ledger.jsonl | 文件式 SLO 台账(双日 guard 全绿记账, ADR-008) | 本机(不入仓) |
| decisions/ADR-009-备份恢复分级与agent入口对齐.md | 备份 4 级置信 L2/L3 落地·L4 blocked-on-scope；llms.txt v2 + AGENTS 自查命令 | sites-docs 仓 decisions/ |
| incidents/README.md | 事故/blameless postmortem 索引 + Open AIs 台账（ADR-009 起） | sites-docs 仓 incidents/ |
| tools/backup-integrity-check.py | D1 备份 L2/L3 静态完整性（非空+可解析+CREATE TABLE/行数+sha256+尺寸漂移告警）| sites-docs 仓 tools/ |
