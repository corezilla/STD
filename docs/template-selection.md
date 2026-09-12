# 模板选择规则

选定交付物后，从[通用 AI 编写指南](ai-authoring-guide.md)进入对应专项；
[精确映射](ai-authoring-guides.json)为每个 Template ID 指定一个主专项，相近模板可以共用。
本文件决定模板适用性，指南解释如何写作；项目采用版本、裁剪与批准规则不因指南更新而变化。

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
| 系统中的一个 subsystem/module/component/implementation-unit | 默认 `design.definition`，硬件/FPGA 见下行专项模板；填写对应 `design_level` | 继承固定的上级约束与设计自由度，解释本单元问题/能力、结构、流程、失败及实现验证；系统背景只作必要摘要和引用 |
| 跨多个 Owner 的行为与恢复闭环 | `design.system-mechanism` | 参与方责任、状态/协议、正常与失败流程；参与单元的实现由各自定义文档负责 |
| 板卡/硬件或 FPGA 单元设计 | `design.hardware` / `design.fpga` | 在专项模板 §1.1 承接固定上级约束与自由度，解释本地落实，并在 §12 区分本地与系统组合验证 |
| 数据字段规格 | `design.data-dictionary` | 保存字段范围的详细 authority，引用所属系统/单元及契约 |

`design.system` 的写作 profile 为 `software-system`、`integrated-system`、`hardware-fpga`。
完整的 profile × 章节适用矩阵、条件触发规则和裁剪记录格式以
[`architecture-design.md` §B.2](../templates/design/architecture-design.md) 为准。这些写作 profile
不改变项目 lock 的 `project_profile` 枚举。子系统/模块不是从系统模板随意删出一个较短版本。

如果一个名为“子系统”的对象本身是独立交付的完整系统，可采用 `design.system`，但必须在
§1.2 说明独立系统边界、消费方和上级关系；`cross-level` 需说明下钻目的和深度，不得复制下级
规格成为第二份 authority。模板生成器只产生草稿，profile 和裁剪决定仍由作者填写及 Reviewer 核验。

条件成立的章节必需；条件不成立时记录理由和 `management.tailoring` 中的决定与批准证据。
省略/合并章节时使用 `template_conformance=tailored`，`tailoring_ref` 指向该裁剪文档的
Document ID，并保留信息项到承载位置的映射。不得只写 N/A 或跳过难以完成的设计。

只有确实需要独立描述跨组件机制、单一实现单元、硬件、FPGA 或数据字典时，才选择相应专项
模板。一个文档可以引用其他领域设计，但每项责任只能有一个 authority。
硬件、FPGA 单元使用专项模板即可完成约束承接，不必再创建 `design.definition` 文档重复同一设计。

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

系统模板 §3.4 先维护机制清单和文档映射，允许预定 ID/文件名后逐份写作。
Planned 路径不是已存在链接或实现输入，成文后才绑定真实版本；详细规则见[映射规范 §5](interface-data-mapping-standard.md#5-先登记机制再逐份编写)。


- `design.system` 保存系统全景、子系统分解、全局策略和约束分配，并自包含地解释端到端原理、
  关键阶段、系统级约束和代表失败；机制目录是导航，不是正文的替代品。
- `design.system-mechanism` 每份细化一个跨子系统机制，唯一维护其详细状态转换、参与方协议、
  完整正常/失败步骤及恢复规则；公共字段与操作必须已完整定义，已有机器契约保持唯一来源。
  系统 §10 统一呈现或精确关联；没有机器源时先用受控设计明确共同定义，不伪造引用。
- `design.definition` 接收系统/父单元及机制的固定输入，记录继承约束、允许自行选择的范围、
  本单元落实与验证；不能重新决定或静默放宽系统政策。

如果一个行为由两个或更多子系统共同完成，并且有独立状态、协议、恢复或验证闭环，应建立
机制文档；如果行为完全属于一个责任单元，则留在该单元的分层设计文档中。
这里按运行职责与协议边界判断，不按工程 Owner 的人数判断；同一 Owner 可以负责多个参与方。
机制模板为 16 个主章，§4 数据结构、§5 接口分开，既有信息保留，不复制完整产品系统的全部专业章节；条件信息项见机制模板附录 A。
开篇用途图、协作/时序/数据/状态/异常/测试六幅关系图与两幅有副作用过程/条件依赖图见
[机制图形样板](../templates/diagrams/mechanism/README.md)，按表达需要选择，不设置图片数量 Gate。
逐能力写作、图例复用和下游承接方法见[系统机制 AI 编写指南](ai-guides/system-mechanism.md)，
不需要先通读完整系统专项。只读与[有副作用完整案例](examples/mechanism-side-effect-example.md)
是不同教学范围，不能将只读重采样规则套用于写操作；职责图放 §3，§1 先说明使用场景与结果。

拆出机制后，用同一 Process/Step/Constraint ID 和固定文档版本关联三层。系统可以保留
概括性流程图和关键阶段，但不复制详细状态机/协议；机制文档细化同一系统行为，不能改成
另一种结果。评审既检查系统正文单独可读，也检查其摘要与详细机制一致。已有完整流程正文
在其他适用文档中时引用其唯一位置，不为模板再创建相同的机制文档。

系统约束分配在系统模板 §3.2 汇总，机制模板 §3.1、通用单元模板 §1.1，以及硬件/FPGA 专项
模板 §1.1 分别记录承接与落实；专项模板 §12 把 Constraint ID 接到本地与系统组合验收。
预算和技术推导保留在原章节。各单元提交的结果须按同一适用条件组合校核，冲突由原决定责任方
依已有流程裁决；这是设计信息承接，不新增审批层级或工具。遇到机制未定的问题，先做章节
预设计，必要时复用 `evaluation.technical-analysis`，选定后回写正文，不以另建文档代替决定。

运行时统筹者、权威状态、参与方确认、部分失败与清理，是系统/机制共同方案的一部分，不能
用工程 Owner 或下级各自实现代替。逐能力查到完整公共契约；已有局部定义先核对整合，旧定义
冲突先裁决修订。只有内部算法、私有布局等不改变共同保证的选择才可独立下放，不新增审批流程。
