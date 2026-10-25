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
