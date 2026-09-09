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
| 整个产品解决什么问题、有哪些功能/页面、整体数据如何流动和如何分解实现 | `design.system` |
| 一个行为如何跨多个组件端到端运行、失败和恢复 | `design.system-mechanism` |
| 一个子系统、模块或组件具体改哪些代码以及如何实现和测试 | `design.definition` |
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

按设计对象和责任范围选择模板，`design_level` 记录该对象在层级中的位置：

```text
system → subsystem → module → component → implementation-unit
```

| 设计对象/要交付的决定 | 首选模板 | 内容深度与上层引用 |
|---|---|---|
| 完整软件系统、设备或软硬件一体系统 | `design.system`，通常 `design_level=system` | 自包含系统概览、关键分工、端到端流程、实现/部署及验证；字段和单元算法引用唯一详细规格 |
| 系统中的一个 subsystem/module/component/implementation-unit | `design.definition`，填写对应 `design_level` | 本单元的问题/能力、外部边界、内部结构与路径、流程/状态、失败、安全、实现与验收；系统背景只作必要摘要和引用 |
| 跨多个 Owner 的行为与恢复闭环 | `design.system-mechanism` | 参与方责任、状态/协议、正常与失败流程；参与单元的实现由各自定义文档负责 |
| 独立硬件/FPGA/数据字段规格 | 对应专项模板 | 保存该领域的详细 authority；系统文档解释其设计作用和约束 |

`design.system` 的写作 profile 为 `software-system`、`integrated-system`、`hardware-fpga`。
完整的 profile × 章节适用矩阵、条件触发规则和裁剪记录格式以
[`architecture-design.md` §1.4](../templates/design/architecture-design.md) 为准。这些写作 profile
不改变项目 lock 的 `project_profile` 枚举。子系统/模块不是从系统模板随意删出一个较短版本。

如果一个名为“子系统”的对象本身是独立交付的完整系统，可采用 `design.system`，但必须在
§1.2 说明独立系统边界、消费方和上级关系；`cross-level` 需说明下钻目的和深度，不得复制下级
规格成为第二份 authority。模板生成器只产生草稿，profile 和裁剪决定仍由作者填写及 Reviewer 核验。

条件成立的章节必需；条件不成立时记录理由和 `management.tailoring` 中的决定与批准证据。
省略/合并章节时使用 `template_conformance=tailored`，`tailoring_ref` 指向该裁剪文档的
Document ID，并保留信息项到承载位置的映射。不得只写 N/A 或跳过难以完成的设计。

只有确实需要独立描述跨组件机制、单一实现单元、硬件、FPGA 或数据字典时，才选择相应专项
模板。一个文档可以引用其他领域设计，但每项责任只能有一个 authority。

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

这些文档可以按已批准的 tailoring 合并，但 metadata 和章节映射必须保留。

## 5. 系统设计与机制设计的边界

- `design.system` 保存系统全景、子系统分解、全局策略和机制目录。
- `design.system-mechanism` 每份只描述一个跨子系统机制的完整端到端设计。
- `design.definition` 描述某个子系统或模块如何履行自己在机制中的责任。

如果一个行为由两个或更多子系统共同完成，并且有独立状态、协议、恢复或验证闭环，应建立
机制文档；如果行为完全属于一个 owner，则留在该 owner 的分层设计文档中。
