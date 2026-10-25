# ADR-001 · 双站前端 = 零 build 的 Cloudflare Pages（仓库直发）
**日期**: 2026-07（既有架构，2026-10-25 回溯留痕）· **状态**: 生效
**决策**: 双站前端仓不跑任何 build（wrangler.toml `build.command = "No build required"`），仓库文件 = 发布面原样；CI=GitHub Actions wrangler-action 直发。
**拒绝的方案**: ① Vite/webpack 构建（多一层产物与源漂移面，静态站无收益）② CF 控制台手工上传（不可版本化、不可复刻）
**证据**: 双仓 `wrangler.toml` build 段 + `.github/workflows/deploy.yml`（无 build step）；A 段整理后发布面=xmg 38/ymg 26 顶层项（git ls-files 实测）。
**未来读者要付代价才知道的 why**: 为什么仓库根有 `_dev-archive/`（gitignored）而不是 .gitignore 逐条列——CI 发布面=git 发布面，归档目录整段出发布面=一处规则管住所有开发垃圾。