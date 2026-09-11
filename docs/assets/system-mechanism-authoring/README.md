# 系统机制示例展示资产

九个 PNG 均由 [对应 SVG 源](../../../templates/diagrams/mechanism/README.md)本地渲染导出，
仅用于机制模板图文教学。只读版本查询定义唯一见 [AI 指南](../../ai-system-design-authoring-guide.md#88-完整小例两个单元的只读版本核对)，
暂存导出定义唯一见[完整案例](../../examples/mechanism-side-effect-example.md)。两者都是原创虚构内容，
不是同一协议，不来源于保密 demo，不是项目实现或运行测试证据。

| 展示图 | 对应源 |
|---|---|
| [用途概览](usage-overview.png) | `usage-overview.svg` |
| [协作](collaboration.png) | `collaboration.svg` |
| [数据对象](objects.png) | `objects.svg` |
| [正常时序](sequence.png) | `sequence.svg` |
| [状态/资源](state-lifecycle.png) | `state-lifecycle.svg` |
| [异常处置](failure-recovery.png) | `failure-recovery.svg` |
| [测试路径](test-path.png) | `test-path.svg` |
| [有副作用完整过程](effect-flow.png) | `effect-flow.svg` |
| [条件依赖](cleanup-dependencies.png) | `cleanup-dependencies.svg` |

导出：本地 Chromium，画布 1440 × 840、deviceScaleFactor=1，等待本地字体加载后截取 SVG。
PNG 不独立维护；改 SVG、重新渲染、目视复查后同步 `exports.json` 中的源/导出摘要。
摘要只检查源与这次导出记录绑定，不能自动证明图片布局或设计内容正确。字体差异可能改变 PNG
字节，更新时如实重新检查，不以沿用旧摘要掩盖漂移。
