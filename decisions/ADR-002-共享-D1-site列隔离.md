# ADR-002 · 双站共库：一个 D1（yunmengge-db）+ site 列隔离
**日期**: 2026-07（迁移于 002-add-site-to-content-tables.sql）· **状态**: 生效
**决策**: 云梦阁/寻梦阁共用一个 D1 数据库，行级 `site` 列（xunmengge/yunmengge）隔离数据；Worker 按路由域判定 site 上下文。
**拒绝的方案**: ① 每站独立 D1（双份 schema 迁移成本 + 跨站共享功能（如 admin 总览）无路）② 应用层路由到多库（CF 无多 D1 绑定价值）
**证据**: `yunmengge-router/migrations/002-add-site-to-content-tables.sql` + wrangler.toml d1 绑定单库；活体 /api/health=200。
**代价（未来读者必读）**: 改共享默认行为（如 /api/hobbies 分页 limit）前必须枚举双站消费方；删列=跨站事故。