# 系统机制图形样板

这是一组可编辑 SVG 及其 PNG 展示，不是新模板类型、图形生成服务或产品设计。
用途图和原六幅关系图共用 **EX-OBS-01/v1 只读版本查询**：Target / Planned / NOT_RUN。
公共字段、操作、错误与命令唯一见 [AI 指南完整小例](../../../docs/ai-system-design-authoring-guide.md#88-完整小例两个单元的只读版本核对)。
新增两图引用 **EX-EXPORT-01/v1 暂存导出**，全部字段与 EX-R1～R8 规则唯一见
[有副作用完整案例](../../../docs/examples/mechanism-side-effect-example.md)，同为 Target / Planned / NOT_RUN。
九图分属两个不同案例，不能拼接为同一协议。数值是教学 Specified 值，不是实测指标。
所有案例为通用虚构内容，未采用保密 demo。

| 图形源 | 机制模板位置 | 表达的关系 |
|---|---|---|
| [usage-overview.svg](usage-overview.svg) | §1 | 使用场景 → 处理范围 → 输出结果 |
| [collaboration.svg](collaboration.svg) | §3 | 触发者、运行参与方、连接及 authority |
| [objects.svg](objects.svg) | §4 | 本地事实 → Sample → Report；复制、变换及寿命 |
| [sequence.svg](sequence.svg) | §6 | EX-OP1、顺序的两次 EX-OP2、响应与期限 |
| [state-lifecycle.svg](state-lifecycle.svg) | §8 | M 内存轮次、终止、迟到拒绝及槽位释放边界 |
| [failure-recovery.svg](failure-recovery.svg) | §9 | M 可返回部分结果 vs M 退出后的未知结果 |
| [test-path.svg](test-path.svg) | §15 | 测试控制、被测链路、独立 Oracle 和清理 |
| [effect-flow.svg](effect-flow.svg) | §6、§9 | 有副作用操作的正常与响应丢失全路径 |
| [cleanup-dependencies.svg](cleanup-dependencies.svg) | §6、§8、§9 | 停止、取证、互斥收口与释放的条件依赖 |

## 选择与复用

一个问题选择一种关系图，不要求九图齐全；已有清楚短表即可解释的状态不要再机械画图。
组成图强调分工，时序图强调先后；数据箭头不冒充时间顺序，状态箭头不等于函数调用。
图后须用正文解释输入、处理、结果、理由及边界，图不能替代公共契约。

1. 将所需 SVG 复制到项目资产目录，替换文件名、`title`/`desc`、示例 ID、真实对象、
   适用基线/配置/拓扑、Owner 与视图/实现/验证状态。不能只替换标题保留教学参数。
2. 每个节点为独立 `<g id="…">`，连线为带 ID 的 `<path>`；增删节点同时修改端点、
   标签、阅读顺序与图注。SVG 不自动布线，长名称用 `tspan` 换行，不能挤进旧框。
3. 统一编辑顶部 `<style>`。白底，灰蓝模块，正文 25 px、辅助字 21 px，标题 34 px；
   浅层面板与较深重点面板有区别，不用模块图标。颜色不表示实现状态；混合 Current/Target
   时另加明确文字及边框样式。图例要和具体图同步，不套用一份含义不符的图例。
4. 蓝实线在交互图表示请求，在对象图表示数据变换，在状态图表示转换；每图图例说明含义。
   灰虚线在交互图是响应，在状态图是终止分支；紫虚线只用于测试控制/判据联系，不是产品通路。
   跨图复用颜色允许表达不同视角，但同一图内不可混淆。无箭头的分组不应被推断为调用关系。
5. 用本地浏览器渲染，检查所有中文、框线和箭头；在约 900 px 正文宽度复查可读性。
   不能靠无限缩字容纳大量参与方；按阶段/故障域拆图，并保留跨图对象 ID。
6. 修改 SVG 后重新导出 PNG，同步图注/正文与跨图语义，核对正常、部分失败、退出、迟到和
   清理。有副作用时再核对 UNKNOWN/FENCED/FINALIZED/RELEASED 的独立含义及选定分支依赖；
   不把“不能重执行”误画成“不能安全收口”。图中真实测试夹具尚未实现/验证，
   教学逻辑模型不是实际停止/隔离证据，若项目用替身则标 simulated，不冒称真实设备覆盖。

## 来源、导出与一致性

SVG 是唯一绘图维护源；不包含脚本、远程图片/字体或嵌入位图。Markdown 使用
[PNG 展示目录](../../../docs/assets/system-mechanism-authoring/README.md)中的兼容导出，
并链接回 SVG，不能独立编辑 PNG。画布 1440 × 840，浏览器 deviceScaleFactor=1，
页面无外部网络依赖；中文使用本地 PingFang SC 或等效中文字体，跨平台字形可能不同。
生成项目实例时 `STD_TEMPLATE_EXAMPLE_BEGIN/END` 内教学图文会移除，项目作者需自行填写真实图文。
文档控制、裁剪与版本规则仍使用现有 STD，不为画图新增审批或发布流程。
