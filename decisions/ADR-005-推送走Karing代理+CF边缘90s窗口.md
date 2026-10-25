# ADR-005 · 部署验证链：Karing :3066 代理 git push + CF 边缘缓存 60-90s 复检窗口
**日期**: 2026-10（多次事故沉淀）· **状态**: 生效
**决策**: ① git push 一律 `git -c http.proxy=http://127.0.0.1:3066 -c https.proxy=...`；② push 后不立即判活：CF 边缘缓存 max-age=300/构建 60-90s，带 ?v=ts cache-buster 复检 + 必要时 sleep 600；③ 判活三视角（直连 curl / Karing / pages.dev 预览域），代理 000 ≠ 宕机。
**证据**: csp-poll 边缘缓存假报（V12.31 沉淀）；B7 双按钮 3旧2新=缓存滞后非部署失败。
**未来读者**: 同 commit 页面新旧混杂时先怀疑缓存再怀疑部署；部署状态以 CF dashboard/构建日志为准。