# ADR-007 · GitHub API 出口 = Karing CONNECT 隧道（本机 github 段直连全阻）
**日期**: 2026-10-25 · **状态**: 生效（新增）
**实测**: baidu.com=200（国内通）；github.com/api.github.com/CF=000（GFW 段）；Karing :3066 = git 专用透传（`curl -x` 通用 HTTP 走它=000），但其 **CONNECT 隧道**（`CONNECT api.github.com:443`+`Host` 头）可建 TLS 隧道 → 其上直发 GitHub REST API 全通（/rate_limit 200，token core 配额 4999/5000）。
**决策**: 本机一切 GitHub API 调用（建仓/读仓/CI 查询）一律走 `karing-github-api.py`（原始 socket→CONNECT→ssl 包装→REST），不再试 curl 直连/`gh auth login`（授权流也到不了 GitHub）。git 操作仍走 `git -c http(s).proxy=http://127.0.0.1:3066`。
**拒绝的方案**: ① 找本机代理端口（10 候选全无）② gh 浏览器授权（20.205.243.166:443 超时=同 000 根因）③ token 直喂 gh（gho_ 缺 read:org scope）
**工具**: `E:/hermes/hermes-tools/karing-github-api.py`（`kapi.py get /user/repos` / `kapi.py post /user/repos '{...}'`）
