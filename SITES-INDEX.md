# SITES-INDEX.md · 双站资产总清单（三件套 · 单一事实源）

> 生成：2026-10-25（A 段整理后实测）。任何 AI/队友动手前先读本文件 + 各仓 AGENTS.md + DEPLOY.md。
> 红线：秘钥只走槽位（[SECRET]），文档/日志不落真实值；内容零改动红线（寻梦阁）。

## 1. 三件套（全部有 git 源仓，"一键复刻"完备）
| 件 | 仓库 | CF 资源 | 域 | 形态 |
|---|---|---|---|---|
| 寻梦阁前端 | `DAOSHISANYE-svg/simishuwu` | Pages 项目 `xunmengge` | 33333344.xyz | 静态零 build + Pages Functions(2 端点) + sw.js/manifest |
| 云梦阁前端 | `DAOSHISANYE-svg/yunmengge`（本地目录 yunmengge-pages） | Pages 项目 `yunmengge` | 2244444.xyz | 静态零 build + _middleware.js |
| 共享后端 | `DAOSHISANYE-svg/yunmengge-router` | Worker Service `yunmengge-router` | api.33333344.xyz + 双域 /api/* | 单 index.js + nodejs_compat，两站共用 D1（site 列隔离） |

本地真源路径：`E:/hermes/workspace-repos/workspace/{simishuwu, yunmengge-pages, yunmengge-router}`。

## 2. 数据/绑定矩阵（复刻时全要建）
| 资源 | 生产值 | 新部署 |
|---|---|---|
| D1 `yunmengge-db` (65cdd645-a790-4e3f-9703-3167d34f9b18) | 双站共库，site 列隔离 | 新建库 + 全量 migrations 按序 apply（**CI 只自动跑 003+compliance 两条，其余手工**，权威=router `migrations/SCHEMA.md`） |
| KV `yunmengge-cache` (35a50ced…) | 热点缓存 | 新建；**可选**（worker 守卫式：env.KV 缺失自动跳过） |
| Durable Object `RATE_LIMITER` | 登录限流 | wrangler deploy 自动建（class 在源码内） |
| Secrets | ADMIN_PASSWORD_HASH / JWT_SECRET / PII_KEY / PII_ENCRYPT | `wrangler secret put` 槽位，**值不落文档** [SECRET] |
| vars DEPLOY_URL | https://yunmengge-pages.pages.dev | 改指新账号 ymg Pages URL |
| Worker routes | api.33333344.xyz/* + 33333344/api/* + 2244444/api/* | 域名替换槽 |

## 3. 依赖方向（部署顺序）
`D1+KV+secrets → yunmengge-router(Worker) → simishuwu(Pages) → yunmengge-pages(Pages) → 自定义域切换`
前端调 `/api/*`：**寻梦阁**本地 functions 服务 2 端点（/api/feedback、/api/admin/errors），其余 ~12 端点（auth/leaderboard/members/contact/bitch-progress/qa-reports…）全由共享 Worker 承载；**云梦阁无本地 API**（functions/ 仅 `_middleware.js` CSP 层，/api/* 100% 走 Worker）（端点真源=`router` 全 src/ 树 70 端点：`src/index.js` 路由壳 + `src/handlers/*` + `src/routes/*` 阶段迁移中；契约=`api-manifest.json`；勿只 grep index.js 下结论）。

## 4. 部署路径（勿臆测，实测）
- 前端双仓：`git push main` → GitHub Actions `deploy.yml`（wrangler-action，project-name=xunmengge/yunmengge，**无 build 步骤**，仓库文件直发）。
- 本地推送走 Karing 代理：`git -c http.proxy=http://127.0.0.1:3066 -c https.proxy=http://127.0.0.1:3066 push`。
- Worker：CI（route-parity+contract-gate+幂等迁移+wrangler deploy+smoke）；主理人亦可 `wrangler deploy` 直部。
- **验证铁律**：push ≠ 上线。CF 边缘缓存滞后 60-90s；活体判定=直连 `env -u HTTPS_PROXY curl` + 部署别名 + 自定义域三视角。

## 5. 健康签名（复刻验收基线）
- `GET https://33333344.xyz/api/health` = 200 + `{"status":"ok","version":"<动态 commit 短哈希>","service":"yunmengge-router-v7"}`（version 随 CI 构建变化，**勿用固定 1.4.9 做回退判定**；判定=200+status ok）
- xmg：`/` 200 + `/slave-test` 200 + `manifest.json` theme=#62775F + 51 页含 vh-fix.js
- ymg：`/` 200 + `/master-test` 301→/pages/master-test/
- 双站 KPI 表见 B8 报告（工作区 `C:/Users/junji/.hermes/output/xmg-b8-content-qa-report.md`，3.2KB）

## 6. 已知 P0/隐患（复刻时保留还是修复，决策权=主人）
1. xmg `master-test` = sm-test 完整克隆（title/H1/跳转全同）——B8 #1 待主人定夺（独立化 or 301）
2. xmg 结果键 5 套命名并存（green_test_v1/slave_test_v2/xmg_sm_test_v2_result/bitch_test_v1/memory_test_result）
3. 认证 session 走 URL 查询参数（/my?sid=），泄漏面 B8 #8
4. xmg 279 unique hex 未全收敛（B5 机械层 879→279 完成，剩余=策展项）
5. router 仓 AGENTS 记载 `xunmengge-db`(fd387c04…) 为孤儿库（无 route，不在生产路径）
6. 双站根级 `br.html/br2.html`（xmg）= 不可达孤儿克隆，B8 #7 待主人定夺

## 7. 工作纪律（所有 AI 通用）
- 改前 `git fetch` 核对 main；`node --check` 过再推；push 后 60-90s 活体三视角验证；gate 落盘（hermes-gate-logging SOP）。
- 寻梦阁=成人内容域：**内容零改动**红线（B8 报告制，Hermes 不擅改一字）；云梦阁/寻梦阁双站分离，交叉只允许出现在：router 共享层（site 列）、qa-dashboard 监控区、本文档。
- 秘钥槽位制：文档/代码/日志不写明文（token 只经环境变量/CF secret 传递）。
