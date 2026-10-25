# ADR-006 · no-agent 告警脚本退出码约定：检出异常=告警 append 文件 + exit 0
**日期**: 2026-09-30（V12.39 实战）· **状态**: 生效（所有新 cron 脚本）
**决策**: 告警型 no-agent cron 检出问题时：结果写 `<name>-alerts.jsonl`（或本地 output）+ `sys.exit(0)`；只有脚本自身崩溃才 exit≠0。
**拒绝的方案**: exit 1 传"我有事报告"→ cron 记 last_status=error + 生成假 P0 卡，真告警被自己的正常产物淹没（incidents 污染实测）。
**证据**: sites-drift-guard.py 现行实现（FAIL→sites-drift-alerts.jsonl + [SILENT]/JSON + exit 0）；hermes cron SOP §问题11。