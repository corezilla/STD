# 模板选择规则

## 1. 先判断交付物，而不是先判断项目名称

| 要回答的问题 | 模板 |
|---|---|
| 项目为什么做、如何组织和控制 | `management.project-plan` |
| 哪些模板适用、哪些裁剪 | `management.tailoring` |
| 软件、固件或 FPGA 如何开发 | `management.development-plan` |
| 系统工程活动如何组织和闭环 | `management.semp` |
| 配置、风险、质量、安全和信息安全如何管理 | 对应的 `management.*-plan` |
| Stakeholder 真正需要什么 | `requirements.stakeholder-needs` |
| 产品在真实环境中如何被使用 | `requirements.conops` |
| 产品必须满足什么 | `requirements.specification` |
| Need、Requirement、Design、Implementation 和 Test 如何闭环 | `requirements.traceability` |
| 某项技术、平台或竞品应如何基于证据分析 | `evaluation.technical-analysis` |
| 整体架构、上下文和关键策略 | `design.system` |
| 一个机制如何跨多个子系统端到端工作 | `design.system-mechanism` |
| 子系统、模块或组件如何实现职责 | `design.definition` |
| 板卡/硬件如何满足电气、机械、热和制造约束 | `design.hardware` |
| FPGA/RTL 如何实现数据面与控制面 | `design.fpga` |
| 数据对象、字段、单位和编码如何定义 | `design.data-dictionary` |
| 面向场景的完整解决方案是什么 | `product.solution-definition` |
| 可交付 SKU 的配置、能力和边界是什么 | `product.sku-specification` |
| 产品阶段、里程碑和演进次序是什么 | `product.roadmap` |
| 如何制造、装配和检验硬件 | `hardware.manufacturing` |
| BOM、正式料号、替代料和供应风险如何管理 | `hardware.bom` |
| 两侧如何连接并共同演进 | `interfaces.control` |
| API、Schema、事件和错误语义 | `contracts.specification` |
| 如何证明需求满足 | `assurance.vv-plan` |
| 某个测试层级如何组织 | `assurance.test-plan` |
| 某组测试如何执行和判定 | `assurance.test-specification` |
| 单次可复现测试如何逐步执行 | `assurance.test-procedure` |
| 测试实际发生了什么 | `assurance.test-report` |
| 如何进行正式验收 | `assurance.acceptance-plan` / `assurance.acceptance-report` |
| FPGA 综合、实现和时序是否收敛 | `assurance.fpga-implementation-report` |
| 某个基线能否进入下一阶段 | `review.packet` |
| 原理图和 PCB 是否可发布 | `review.schematic-pcb` |
| 为什么选择某项方案 | `decisions.adr` |
| 如何发布、部署、运行、恢复和退役 | `operations.release` |
| 发布中准确包含什么 | `operations.version-description` |
| 用户如何使用产品 | `operations.user-manual` |
| 如何安装和部署 | `operations.installation-deployment` |
| 运维人员如何持续运行系统 | `operations.operations-manual` |
| 如何维护和排障 | `operations.maintenance` |
| 新板卡/系统如何首次上电联调 | `operations.bring-up` |

## 2. 分层设计

`design.definition` 通过 metadata 的 `design_level` 支持：

```text
system → subsystem → module → component → implementation-unit
```

系统级必须使用 `design.system`；下级默认使用 `design.definition`，再叠加 software、hardware、
firmware 或 FPGA profile。一个文档可以引用其他领域设计，但每项责任只能有一个 authority。

## 3. 当前项目映射

- Slinky：system、subsystem、module、implementation-unit、interface、test、review。
- Piko/LLMTier：service/subsystem design、contract、schema、error、fixture、recovery、review。
- HIFM：system/subsystem/module、hardware、FPGA、interface、simulation、budget、V&V、SKU gate。

## 4. 测试文档的边界

- `vv-plan`：整个产品如何证明需求满足。
- `test-plan`：某一测试层级的范围、资源、策略、入口和出口。
- `test-specification`：测试 case、输入、oracle 和覆盖设计。
- `test-procedure`：可由执行者逐步操作的程序。
- `test-report`：一次或一组实际执行结果。
- `acceptance-*`：客户/产品 authority 的正式验收决定。

这些文档可以按 tailoring 合并，但 metadata 和章节映射必须保留。

## 5. 系统设计与机制设计的边界

- `design.system` 保存系统全景、子系统分解、全局策略和机制目录。
- `design.system-mechanism` 每份只描述一个跨子系统机制的完整端到端设计。
- `design.definition` 描述某个子系统或模块如何履行自己在机制中的责任。

如果一个行为由两个或更多子系统共同完成，并且有独立状态、协议、恢复或验证闭环，应建立
机制文档；如果行为完全属于一个 owner，则留在该 owner 的分层设计文档中。
