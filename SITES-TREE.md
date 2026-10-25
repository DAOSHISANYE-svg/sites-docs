# SITES-TREE.md · 双站项目树图 v2（页级/端点级/数据表级 · 数据驱动 2026-10-25）

> 生成=活体仓 + 活体 curl 实测。配套：`SITES-INDEX.md`（依赖/密钥/部署）· 各仓 `AGENTS.md`/`DEPLOY.md`。
> ⚠️ 同名异项：`master-test` 两站不同物（xmg=B8 P0 sm 克隆；ymg=主人综合测评）。跨站 grep 勿混。

## 1. 拓扑总树
```
DAOSHISANYE-svg/
├── simishuwu        = 寻梦阁 → CF Pages `xunmengge` → 33333344.xyz（成人内容域，内容零改动红线）
├── yunmengge        = 云梦阁 → CF Pages `yunmengge`   → 2244444.xyz（常规站；本地目录 yunmengge-pages）
└── yunmengge-router = 共享后端 → CF Worker Service `yunmengge-router`
    routes: api.33333344.xyz/* + 33333344.xyz/api/* + 2244444.xyz/api/*
    绑定: D1 `yunmengge-db`(共库, site 列 xunmengge/yunmengge 隔离) · KV `yunmengge-cache`(可选守卫式) · DO `RATE_LIMITER`
    secrets: ADMIN_PASSWORD_HASH / JWT_SECRET / PII_KEY / PII_ENCRYPT [槽位, 值不落文档]
部署顺序: D1(+迁移)+KV+secrets → router → 双 Pages → 自定义域
```

## 2. 寻梦阁 pages 全量（50 目录 + articles/43）
xmg: 共 50 目录 = 测试 6 + 结果 12（general 结果已计入）+ 其他 25

### 2.1 测试/结果页（本地实读全页对照）
<!-- GEN:BEGIN §2-->
| /pages/admin/ | 《管理面板 - 寻梦阁》 |  |
| /pages/adult-tests/ | 《成人测试 - 寻梦阁》 |  |
| /pages/api/ | 《API文档 - 寻梦阁》 |  |
| /pages/articles/ | 《三爷文章 - 寻梦阁》 |  |
| /pages/assets/ | （无 index.html） |  |
| /pages/bitch-result/ | 《女奴属性测试结果 - 寻梦阁》 | ⚠️ H1=slave 残留（B8#5） |
| /pages/bitch-test/ | 《女奴属性测试 - 寻梦阁》 |  |
| /pages/diagnostic/ | 《详细诊断 - 寻梦阁》 |  |
| /pages/exposure-task/ | 《每日露出任务 - 寻梦阁》 |  |
| /pages/feedback/ | 《意见反馈 - 寻梦阁》 |  |
| /pages/general-attachment/ | 《依恋风格测试 - 寻梦阁》 |  |
| /pages/general-attachment-result/ | 《你的依恋类型测试结果 - 寻梦阁》 |  |
| /pages/general-bigfive/ | 《大五人格测试 - 寻梦阁》 |  |
| /pages/general-bigfive-result/ | 《你的大五人格测试结果 - 寻梦阁》 | ⚠️ H3'情商画像'=emotion 残留（B8#4） |
| /pages/general-emotion/ | 《情绪情商测试 - 寻梦阁》 |  |
| /pages/general-emotion-result/ | 《情绪情商测试结果 - 寻梦阁》 |  |
| /pages/general-meaning/ | 《人生意义感测试 - 寻梦阁》 |  |
| /pages/general-meaning-result/ | 《人生意义感测试结果 - 寻梦阁》 |  |
| /pages/general-peoplepleaser/ | 《讨好型人格测试 - 寻梦阁》 |  |
| /pages/general-peoplepleaser-result/ | 《讨好型人格测试结果 - 寻梦阁》 |  |
| /pages/general-stress/ | 《压力与韧性测试 - 寻梦阁》 |  |
| /pages/general-stress-result/ | 《压力与韧性测试结果 - 寻梦阁》 |  |
| /pages/general-trauma/ | 《童年创伤测试 - 寻梦阁》 |  |
| /pages/general-trauma-result/ | 《童年创伤测试结果 - 寻梦阁》 |  |
| /pages/green-result/ | 《绿奴属性测试结果 - 寻梦阁》 |  |
| /pages/green-test/ | 《绿奴属性测试 - 寻梦阁》 |  |
| /pages/hobbies-list/ | 《兴趣标签 - 寻梦阁》 |  |
| /pages/jars/ | 《性癖瓶子 · 互动填涂 \| 寻梦阁》 |  |
| /pages/leaderboard/ | 《排行榜 - 寻梦阁》 |  |
| /pages/login/ | 《登录 - 寻梦阁》 |  |
| /pages/master-test/ | 《SM属性测试 - 你的真实欲望 - 寻梦阁》 | **B8#1 P0 = sm-test 完整克隆** |
| /pages/members/ | 《圈友展示 - 寻梦阁》 |  |
| /pages/memory-result/ | 《回忆测试结果 - 寻梦阁》 | ⚠️ test/result title 名实错位（B8 P1 类） |
| /pages/memory-test/ | 《强奸回忆体验 - 寻梦阁》 |  |
| /pages/my/ | 《我的 - 寻梦阁》 |  |
| /pages/privacy/ | 《隐私政策 - 寻梦阁》 |  |
| /pages/privacy-en/ | 《Privacy Policy - 寻梦阁》 |  |
| /pages/psych-tests/ | 《通用心理测试 - 寻梦阁》 |  |
| /pages/qa-dashboard/ | 《寻梦阁 QA 仪表盘》 |  |
| /pages/quiz/ | 《属性测试 - 寻梦阁》 |  |
| /pages/quiz-female/ | 《女奴属性测试 - 寻梦阁》 |  |
| /pages/register/ | 《加入圈友 - 寻梦阁》 |  |
| /pages/slave-result/ | 《女奴接受度测试结果 - 寻梦阁》 |  |
| /pages/slave-test/ | 《女奴接受度测试 - 寻梦阁》 |  |
| /pages/sm-result/ | 《SM属性测试结果 - 寻梦阁》 |  |
| /pages/sm-test/ | 《SM属性测试 - 你的真实欲望 - 寻梦阁》 |  |
| /pages/submissions/ | 《圈友投稿 - 寻梦阁》 |  |
| /pages/terms/ | 《用户协议 - 寻梦阁》 |  |
| /pages/test/ | 《全部测试 - 寻梦阁》 |  |
| /pages/wall/ | 《打招呼墙 - 向全体圈友打招呼 \| 寻梦阁》 |  |
<!-- GEN:END §2-->
## 3. 云梦阁 pages 全量（32 目录 + 根级活页 leaderboard.html/article.html/blog.html；文章=单文件非目录）
ymg: 共 32 目录 = 测试 6 + 结果 12（general 结果已计入）+ 其他 7

### 3.1 测试/结果页（全页对照 · 再生数据节）
<!-- GEN:BEGIN §3-->
| /pages/admin/ | （无 index.html） |  |
| /pages/bitch-result/ | 《女奴属性测试结果 - 云梦阁》 |  |
| /pages/bitch-test/ | 《高潮引导仪式 - 云梦阁》 | test/result 命名错位 |
| /pages/feedback/ | 《意见反馈 · 云梦阁》 |  |
| /pages/general-attachment/ | 《依恋风格测试 - 云梦阁》 |  |
| /pages/general-attachment-result/ | 《你的依恋类型测试结果 - 云梦阁》 |  |
| /pages/general-bigfive/ | 《大五人格测试 - 云梦阁》 |  |
| /pages/general-bigfive-result/ | 《你的大五人格测试结果 - 云梦阁》 |  |
| /pages/general-emotion/ | 《情绪情商测试 - 云梦阁》 |  |
| /pages/general-emotion-result/ | 《情绪情商测试结果 - 云梦阁》 |  |
| /pages/general-meaning/ | 《人生意义感测试 - 云梦阁》 |  |
| /pages/general-meaning-result/ | 《人生意义感测试结果 - 云梦阁》 |  |
| /pages/general-peoplepleaser/ | 《讨好型人格测试 - 云梦阁》 |  |
| /pages/general-peoplepleaser-result/ | 《讨好型人格测试结果 - 云梦阁》 |  |
| /pages/general-stress/ | 《压力与韧性测试 - 云梦阁》 |  |
| /pages/general-stress-result/ | 《压力与韧性测试结果 - 云梦阁》 |  |
| /pages/general-trauma/ | 《童年创伤测试 - 云梦阁》 |  |
| /pages/general-trauma-result/ | 《童年创伤测试结果 - 云梦阁》 |  |
| /pages/green-result/ | 《绿奴属性测试结果 - 云梦阁》 |  |
| /pages/green-test/ | 《绿奴属性测试 - 云梦阁》 |  |
| /pages/index/ | 《云梦阁 · 圈友广场》 |  |
| /pages/login/ | 《登录 - 云梦阁》 |  |
| /pages/master-test/ | 《主人综合测评 · 云梦阁》 | 主人综合测评（区别于 xmg 同名 P0 页） |
| /pages/members/ | 《圈友展示 - 云梦阁》 |  |
| /pages/memory-result/ | 《回忆测试结果 - 云梦阁》 |  |
| /pages/memory-test/ | 《强奸回忆体验 - 寻梦阁》 | **跨站命名残留：title 写'寻梦阁'**（报告制） |
| /pages/register/ | 《加入圈友 - 云梦阁》 |  |
| /pages/slave-result/ | 《奴隶属性测试结果 - 云梦阁》 |  |
| /pages/slave-test/ | 《女奴接受度测试 - 云梦阁》 |  |
| /pages/sm-result/ | 《SM属性测试结果 - 云梦阁》 |  |
| /pages/sm-test/ | 《SM属性测试 - 你的真实欲望 - 云梦阁》 |  |
| /pages/submissions/ | 《圈友投稿 - 云梦阁》 |  |
<!-- GEN:END §3-->
| 路径 | title | 标注 |
|---|---|---|
| /pages/master-test/ | 《主人综合测评 · 云梦阁》 | 正规功能（区别于 xmg P0 同名页） |
| /pages/memory-test/ | 《强奸回忆体验 - **寻梦阁**》 | **跨站命名残留：云梦阁仓页 title 写寻梦阁**（内容资产，报告制交主人，Hermes 不改） |
| /pages/bitch-test/ | 《高潮引导仪式 - 云梦阁》 | test/result 命名错位（结果页=女奴属性测试结果） |
| /pages/slave-test/ | 《女奴接受度测试 - 云梦阁》 | |
| /pages/sm-test/ / /pages/green-test/ / 7 general-*/ | 与 xmg 同系测评克隆 | 克隆同源实证 |
| 根级活页 | leaderboard.html（/leaderboard/ 200 指向根文件） | _redirects 186 规则（200=71/301=74） |

## 4. 共享后端 yunmengge-router（/api/* 真源 · 70 端点全树）
### 4.0 端点/D1 计数（再生数据节）
<!-- GEN:BEGIN §4-->
api-manifest: exact 58 + prefix 7（router 仓, 改路由须 --gen-manifest 重发）
D1 增量表（migrations SQL 实测）: client_errors revoked_tokens users_new wall_messages
<!-- GEN:END §4-->
```
src/
├── index.js（路由壳，42/70 端点字面）
├── handlers/content.js, xunmengge.js（按站分文件）
├── routes/content.js（阶段0 单域迁移）
├── api-manifest.json（契约：exact 58 + prefix 7，08-17 生成；改路由/handler 须 `--gen-manifest` 重发并提交）
├── migrations/（002/003/004/compliance + SCHEMA.md；CI 只自动 003+compliance）
└── scripts/pre-deploy-check.mjs（契约闸门）
D1 表（SCHEMA.md 10 + 增量 3）:
│   users users_new wall_messages articles audit_logs comments feedbacks hobbies questions_suggest quiz_results submissions client_errors revoked_tokens
api-manifest exact 分组:
    /api/achievements（1）: /api/achievements
    /api/activity（1）: /api/activity/view
    /api/admin（21）: /api/admin/articles /api/admin/audit-logs /api/admin/dashboard /api/admin/export/users/csv /api/admin/feedback /api/admin/generate-code /api/admin/hobbies /api/admin/hobbies/batch /api/admin/hobbies/batch-delete /api/admin/login /api/admin/logout /api/admin/me …
    /api/articles（1）: /api/articles
    /api/auth（2）: /api/auth/login /api/auth/register
    /api/client-error（1）: /api/client-error
    /api/comments（1）: /api/comments
    /api/contact（1）: /api/contact
    /api/favorites（1）: /api/favorites
    /api/feedback（1）: /api/feedback
    /api/health（1）: /api/health
    /api/hobbies（1）: /api/hobbies
    /api/leaderboard（1）: /api/leaderboard
    /api/members（2）: /api/members /api/members/count
    /api/misc（5）: / /wall/like /wall/list /wall/post /wall/unlike
    /api/qa-reports（1）: /api/qa-reports
    /api/quiz（2）: /api/quiz/history /api/quiz/save
    /api/rank（1）: /api/rank/me
    /api/register（1）: /api/register
    /api/sm-result（1）: /api/sm-result
    /api/stats（1）: /api/stats
    /api/submissions（1）: /api/submissions
    /api/user（8）: /api/user/export /api/user/generate-code /api/user/login /api/user/logout /api/user/me /api/user/my-hobby /api/user/register /api/user/test-history
    /api/wall（1）: /api/wall/messages


```

## 5. 前端 fetch 端点归属（实测差集）
| 前端 | 本地 functions | 共享 Worker |
|---|---|---|
| 寻梦阁（12 端点面） | /api/feedback · /api/admin/errors（errors.js+feedback.js） | auth/register login · leaderboard · members/count · contact · bitch-progress · qa-reports · stats · register · admin/*（18 admin 端点） |
| 云梦阁（全 Worker） | 无（仅 _middleware.js CSP） | leaderboard · user/logout · … |

## 6. B8 状态映射（19 项 → 当前态）
- **已闭环**: #11 worktree（A 段清退）· #12 quiz-ux 注入（B1' 外链化）
- **待主人**: #1 master-test P0 · #2 结果键 5 套 · #3 sm 断点 · #4-7 残留/orphan · #8 session URL · #9 wall UGC · #10 键名 · #13-16 UI 措辞 · #17-19 策展
- **新发现（本轮树图生成）**: 云梦阁仓 memory-test title 跨站残留（xmg 名入 ymg 页）→ 入云梦阁侧 QA 清单（报告制）

## 7. 读图入口
本文件（页级结构）→ SITES-INDEX.md（依赖/密钥/顺序）→ 各仓 AGENTS.md（纪律）→ 各仓 DEPLOY.md（复刻 runbook）→ B8 报告（C:/Users/junji/.hermes/output/xmg-b8-content-qa-report.md，19 项定夺）
