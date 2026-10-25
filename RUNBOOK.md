# RUNBOOK.md · 双站事故手册（workstation #1）
> 原则：**不可逆操作即报**（delete / zone / token / DNS / 生产写 → 先落 gate 再动，或只报不动）；
> **本机故障 ≠ 站点故障**（双站在 CF，本机只影响工程链，不影响发布面，除非正在 CI 推送）。
> 每个故障模式 = 现象 / 定位 / 处置 / 升级 四段。全部 2026-10-25 实测可跑。

## 0. 快速定位
```
现象 → 先跑：E:/hermes/hermes-tools/sites-drift-guard.py   （39 断言，全绿 [SILENT]=无结构性故障）
       +  curl -s -o /dev/null -w "%{http_code}" https://33333344.xyz/  （双站活体）
```

## 1. 双站 404 / 5xx（站点可达性）
- **定位**：`env -u HTTPS_PROXY curl -s -o NUL -w "%{http_code}" https://33333344.xyz/<path>`（直连，非代理；代理 000 ≠ 宕机，见 ADR-005）
- **处置**：
  - 单页 404 → 多为 CF Pages 边缘缓存滞后：带 `?v=$(date +%s)` 复检 + 等 60-90s 再判（见 hermes-deliverable-contract §CF缓存滞后）
  - 全站 5xx → CF dashboard 看 Pages 构建日志；构建卡=CI 三道门挂（ci-xss-gate/frontend-deps-check/nav-smoke），本地 `git log --oneline -5` 找最近 push 的 commit 回滚
  - 回滚=不可逆生产写 → **先落 gate + 报告主人**，不擅自 revert
- **升级**：CF 构建持续红 / 回滚前 → 报告主人

## 2. Worker API `/api/*` 异常（router）
- **定位**：`curl -s https://33333344.xyz/api/health`（D1 在跑=200 间接证）；5xx 看 router `pre-deploy-check` CI
- **处置**：
  - 429 → Durable Object RATE_LIMITER 限流在跑，属正常；查是否触发阈值=业务侧
  - 5xx 持续 → CF dashboard 看 Worker 最近部署版本；异常部署=回滚版本（不可逆→报告主人）
- **升级**：Worker 版本回滚前 → 报告

## 3. D1 数据库故障
- **定位**：`/api/health` 200=健康；持续 5xx=看 D1 用量/迁移日志（CF dashboard）
- **处置**：D1 **每日 SQL 备份**在 `E:/hermes/d1-backups/`（最新 `mysite-db-YYYY-MM-DD.sql` + `xunmengge-db-*.sql`），故障恢复=重导入备份（**恢复生产 D1=不可逆，先报告主人**）
- **升级**：任何 D1 恢复 / 迁移 → 报告

## 4. Karing 服务挂（:3066，全 GitHub 通道）
- **定位**：`netstat -ano | grep 3066`；guard §12 `karing_3066_alive` 断言会兜底报 FAIL
- **处置**：`tasklist | grep karing`；无进程=启动 `C:/Program Files/Karing/karingService.exe`（自启任务 **Karing Autorun** 会在重启后自跑）
- **升级**：Karing 启动失败 / 端口被占 → 报告（本机网络基建，非站点）

## 5. GCM token 过期（GitHub push 403/401）
- **定位**：`git -c http.proxy=http://127.0.0.1:3066 push` 报 403/401 = token 面
- **处置**：`C:/Users/junji/.git-credentials` 的 `gho_` 是 OAuth（~8h 自动刷新）；长期失效=重新 GCM 配置 token（**token 变更=不可逆，报告主人**）
- **隧道 API**：`tools/karing-github-api.py`（Karing CONNECT 隧道，ADR-007），隧道瞬时拥塞=工具自带 2s×2 重试

## 6. CF token 权限受限
- **定位**：`E:/hermes/config/keys/.cf_token`（只读进内存）；无 D1/KV 读 scope=活体 `/api/health` 200 间接证 D1 在跑
- **处置**：权限不足=不强行 apply；**扩权=报告主人**
- **红线**：CF / GitHub / 网关秘钥只走槽位引用，文档/日志不落真实值（出现即 [REDACTED]）

## 7. 双站发布 / 部署
- **定位**：`git -C <repo> log --oneline origin/main -1`（远程 HEAD）+ `env -u HTTPS_PROXY curl` 活体
- **处置**：本地 push 成功≠部署成功≠线上生效（三层，见 deliverable-contract §六）；CF Pages 构建 60-90s 窗口（ADR-005）
- **升级**：任何「恢复/下线/回滚/zone/DNS」= 不可逆，**先报告主人**

## 8. 红线（不可触碰）
- **双站分离**：寻梦阁任何用户流/出口/跳转/键名归因，禁写云梦阁（内容资产红线，主人 10-24 双红线 #1）
- **内容零改动**：双站既有文案/题面/结果/成人内容 = 合理合规，Hermes 不改一字（红线 #2）；发现措辞缺口只入 B8 报告交主人定夺
- **网关只读防线**：`E:/hermes/llm-key-gateway/` 7 文件只读（10-24 主人令），改动=六步流程 + `_sha_drift.py --repin`
- **密钥不落盘**：所有 token/secret 走槽位，摘要/日志出现真实值即 [REDACTED]

## 9. 升级路径
Bot（Hermes）自决执行「可逆 + 授权内」→ 落 gate → 报主人结论+证据。
「不可逆 / 越权 / 生产写 / 密钥 / zone/DNS/回滚」→ 只报不动，等主人。
