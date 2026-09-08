# STD 项目仓库目录规范

## 1. 规则

本规范适用于软件、硬件、固件、FPGA 和混合系统项目。目录结构是推荐默认值；已有项目可保留
合理结构，并在 tailoring manifest 中记录实际路径、Owner 和 authority。

- 按 artifact 类型与 authority 组织，不按迁移批次或作者组织。
- 项目级、系统级和跨 Owner 文档放在根 `docs/`；领域专属设计可以随 Owner 共置。
- 规范、实现、测试程序、运行证据、沟通记录和对外材料分开保存。
- 每个 artifact 只有一个 canonical path；索引可以引用，不复制权威正文。
- 目录树中的 `#` 注释就是该目录的职责说明，不要求为每个目录另建 README。
- 只创建实际需要的目录，不要求预建空目录。

## 2. 混合软硬件项目默认结构

```text
<project>/                        # 项目仓库根，容纳全局治理、各Owner工程域和交付物
├── .github/                       # GitHub PR、Issue、CODEOWNERS、CI和协作配置
├── docs/                          # 项目级、系统级和跨工程域权威文档
│   ├── 00_management/             # 项目、开发、配置、风险、质量和安全管理计划
│   ├── 10_requirements/           # Stakeholder Needs、ConOps、需求规格和追踪
│   ├── 15_evaluation/             # 可行性、技术选型、容量性能、竞品和trade-off证据
│   ├── 20_system_design/          # 系统边界、架构、分解和跨子系统设计
│   │   ├── mechanisms/            # 跨两个以上Owner的端到端机制
│   │   └── features/              # 可独立验收的系统级功能设计
│   ├── 25_product_definition/     # 产品形态、解决方案、SKU和路线图
│   │   ├── solutions/             # 面向场景的完整产品或部署方案
│   │   ├── skus/                  # 可交付配置、选型、容量和适用边界
│   │   └── roadmap/               # 产品阶段、里程碑和演进计划
│   ├── 30_subsystem_design/       # 未采用Owner共置时的子系统设计
│   ├── 40_module_design/          # 未采用Owner共置时的模块设计
│   ├── 50_implementation_design/  # 文件、类、RTL单元等实现级设计
│   ├── 60_interfaces/             # ICD、接口目录、边界说明和契约索引
│   ├── 70_verification/           # V&V和正式测试文档，不存测试源码
│   │   ├── plans/                 # 验证策略、范围、资源和排期
│   │   ├── specifications/        # Case、输入、Oracle和覆盖要求
│   │   ├── procedures/            # 测试环境、步骤和操作方法
│   │   ├── reports/               # 执行结果、偏差、结论和证据索引
│   │   └── acceptance/            # 客户或项目验收计划与结论
│   ├── 80_operations/             # 安装、用户、运维、维护、Bring-up和发布资料
│   ├── 90_decisions/              # ADR和已批准的重要技术决策
│   ├── 91_reviews/                # 正式评审包、发现、决定和关闭记录
│   ├── 98_migration/              # 迁移盘点、路径映射和阶段性记录
│   ├── 99_reference/              # 外部参考、历史材料和非权威快照
│   └── assets/                    # 供正式文档引用的图表和小型附件
├── notes/                         # 过程性会议、客户、合作方和内部沟通记录
│   ├── meetings/                  # 项目例会、专题会和评审准备会记录
│   ├── customers/                 # 按客户分组的沟通、需求线索和行动项
│   ├── partners/                  # 按合作方分组的沟通、依赖和行动项
│   ├── internal/                  # 内部讨论、工作记录和临时共识
│   └── attachments/               # 与沟通记录绑定的小附件
├── materials/                     # 对外表达和交付材料，不是工程规格authority
│   ├── investors/                 # 投资人Deck和经批准的数据室材料
│   ├── products/                  # 系统、产品、板卡单页和Datasheet
│   ├── marketing/                 # 宣传册、活动、网站和媒体材料
│   ├── sales/                     # Solution Brief和销售竞品卡
│   ├── customers/                 # 面向特定客户的已批准交付件
│   ├── partners/                  # 面向特定合作方的已批准交付件
│   ├── assets/                    # Logo、渲染图和公共视觉素材
│   └── published/                 # 实际对外发出的不可变版本快照
├── interfaces/                    # 多工程域消费的机器可读契约authority
│   ├── docs/                      # 接口导航、边界和人工可读说明
│   ├── abi/                       # 二进制布局、调用约定和版本基线
│   ├── idl/                       # Proto、Thrift或自定义IDL源定义
│   ├── schemas/                   # JSON、YAML、配置和数据Schema
│   ├── error-codes/               # 跨组件错误码注册和语义
│   ├── compatibility/             # 兼容矩阵、弃用和升级规则
│   ├── vectors/                   # 小型冻结契约向量和Golden样例
│   └── codegen/                   # 从契约生成代码或文档的工具
├── software/                      # 软件域产品、服务、库及其Owner文档
│   ├── docs/                      # 跨软件组件的总体设计、约束和公共说明
│   │   ├── 10_requirements/       # 从系统需求分配到软件域的需求和追踪
│   │   ├── 20_architecture/       # 软件域总体架构、分层、进程和部署视图
│   │   │   └── mechanisms/        # 跨多个软件组件的调度、恢复、数据流等机制
│   │   ├── 30_subsystem_design/   # 软件子系统划分、责任、依赖和组合关系
│   │   ├── 60_interfaces/         # 软件接口目录及对顶层机器契约的引用
│   │   ├── 70_verification/       # 软件域测试策略、规格、报告和质量Gate
│   │   ├── 80_operations/         # 软件域构建、安装、部署、运行和维护说明
│   │   └── 91_reviews/            # 软件架构、集成、质量和发布评审记录
│   └── <component>/               # 一个可独立维护的软件组件、服务或应用
│       ├── docs/                  # 该组件专属需求、设计、接口消费和评审
│       │   ├── requirements/      # 分配给该组件的功能和质量需求
│       │   ├── architecture/      # 组件边界、依赖、状态、线程和数据流
│       │   ├── modules/           # 组件内部包、模块、类和关键算法设计
│       │   ├── interfaces/        # 组件提供/消费接口及公共契约引用
│       │   ├── verification/      # 组件测试设计、覆盖、结果和已知限制
│       │   ├── operations/        # 组件配置、部署、诊断、升级和恢复说明
│       │   └── reviews/           # 组件需求、设计、实现和发布评审记录
│       ├── src/                   # 该组件的产品实现源码
│       ├── include/               # 该组件对外公开头文件或SDK接口，按需启用
│       ├── tests/                 # 该组件内部单元、组件和局部契约测试
│       ├── configs/               # 该组件默认配置、示例和Schema
│       ├── deploy/                # 该组件独立部署定义，适用于服务类组件
│       └── tools/                 # 该组件专用构建、生成、调试和分析工具
├── firmware/                      # FPGA、MCU、设备固件和RTL工程域
│   ├── docs/                      # 跨固件产品的总体设计、工具链和公共约束
│   │   ├── 10_requirements/       # 从系统需求分配到固件域的需求和追踪
│   │   ├── 20_architecture/       # 固件域总体架构、产品分解和公共技术基线
│   │   │   └── mechanisms/        # 跨固件产品的启动、升级、恢复和遥测机制
│   │   ├── 30_product_design/     # 多个固件产品的职责、依赖和集成关系
│   │   ├── 60_interfaces/         # 固件公共总线、寄存器、协议和接口索引
│   │   ├── 70_verification/       # 固件域仿真、形式验证、实现和板测策略
│   │   ├── 80_operations/         # 工具链、构建、烧录、升级、回滚和维护
│   │   └── 91_reviews/            # 固件架构、CDC/RDC、时序和发布评审
│   └── <product>/                 # 一个可独立构建、烧录或发布的固件产品
│       ├── docs/                  # 固件产品的需求、架构、模块和验证文档
│       │   ├── requirements/      # 功能、性能、资源、时序和安全需求
│       │   ├── architecture/      # 顶层架构、时钟复位、数据流和资源分解
│       │   ├── modules/           # RTL模块、驱动模块或固件组件设计
│       │   ├── interfaces/        # 寄存器、总线、协议和板级接口说明
│       │   ├── verification/      # 仿真、形式验证、实现和Bring-up资料
│       │   ├── operations/        # 构建、烧录、升级、诊断、恢复和维护说明
│       │   └── reviews/           # 需求、设计、CDC/RDC、时序和发布评审
│       ├── src/                   # 可综合或可编译的固件产品源码
│       │   ├── rtl/               # FPGA/ASIC HDL、package和顶层封装
│       │   └── embedded/          # MCU、管理核或软核上的嵌入式软件
│       ├── constraints/           # Pin、时钟、时序、区域和实现约束
│       ├── ip/                    # 自研/第三方IP封装、配置和版本manifest
│       ├── sim/                   # Testbench、仿真模型和仿真入口
│       ├── tests/                 # 固件单元、接口、回归和板上验证自动化
│       └── tools/                 # 综合、实现、烧录、寄存器和报告工具
├── hardware/                      # 板卡、机械、电气、BOM和制造工程域
│   ├── docs/                      # 系统硬件总体设计、公共约束和选型原则
│   │   ├── 10_requirements/       # 从系统需求分配到硬件域的需求和追踪
│   │   ├── 15_evaluation/         # 器件、平台、成本、供应链和技术trade-off
│   │   ├── 20_architecture/       # 整机、板卡、互连、供电和散热总体架构
│   │   ├── 30_platform_design/    # 多板卡、机箱、背板、线缆和部署形态设计
│   │   ├── 60_interfaces/         # 电气、机械、连接器、时钟和管理接口索引
│   │   ├── 70_verification/       # SI/PI、热、功耗、可靠性和合规验证策略
│   │   ├── 80_manufacturing/      # 全局制造、装配、检验、追溯和质量要求
│   │   ├── 85_compliance/         # 安规、EMC、环境、认证和法规资料
│   │   └── 91_reviews/            # 硬件架构、原理图、PCB和量产评审
│   ├── catalog/                   # 器件、平台、供应商、报价和来源注册表
│   ├── libraries/                 # 受控EDA符号、封装、3D模型和复用电路库
│   ├── boards/                    # 所有板、卡和硬件产品的Owner目录
│   │   └── <board>/               # 一个具体板卡型号或硬件修订族
│   │       ├── docs/              # 板卡需求、设计、BOM、制造和评审文档
│   │       │   ├── requirements/  # 板卡功能、性能、环境、成本和合规需求
│   │       │   ├── architecture/  # 器件分区、数据通路、时钟、复位和管理架构
│   │       │   ├── interfaces/    # 插槽、连接器、电气、机械和板间接口说明
│   │       │   ├── power-thermal/ # 电源树、功耗预算、散热和热设计文档
│   │       │   ├── components/    # 关键器件选型、替代料理由和生命周期分析
│   │       │   ├── verification/  # 板级验证设计、覆盖、结果和已知限制
│   │       │   ├── manufacturing/ # 装配、生产测试、检验和追溯文档
│   │       │   ├── compliance/    # 板卡适用的安规、EMC和环境合规文档
│   │       │   ├── operations/    # Bring-up、调试、升级、维修和现场支持资料
│   │       │   └── reviews/       # 需求、原理图、PCB、EVT/DVT/PVT和发布评审
│   │       ├── schematic/         # 原理图源文件、可审查导出和ERC结果
│   │       ├── pcb/               # PCB布局布线源、约束、DRC和制造输出定义
│   │       ├── mechanical/        # 结构、尺寸、机箱、散热和3D模型
│   │       ├── bom/               # 机器可读BOM、AVL、价格和替代料数据
│   │       ├── manufacturing/     # Gerber、坐标、装配和生产测试等交付数据
│   │       ├── verification/      # 板测脚本、小型输入、测量数据和结果索引
│   │       ├── images/            # 板卡照片、布局图和文档用渲染图
│   │       └── references/        # Datasheet、应用笔记和供应商参考资料
│   └── tools/                     # BOM、ERC/DRC、PCB检查和制造导出工具
├── tests/                         # 跨软件、固件、硬件的可执行验证
│   ├── static/                    # 文档、路径、源码、RTL和策略静态检查
│   │   ├── documents/             # 文档结构、metadata、链接和追踪检查
│   │   ├── source/                # 软件源码格式、依赖和禁止模式检查
│   │   ├── rtl/                   # HDL lint、CDC/RDC规则和约束静态检查
│   │   └── repository/            # 路径、命名、许可证和仓库策略检查
│   ├── unit/                      # 可在单一模块边界完成的自动化测试
│   │   ├── software/              # 软件函数、类和模块单元测试
│   │   ├── firmware/              # RTL模块、嵌入式函数和固件单元测试
│   │   └── models/                # 算法、容量、性能和参考模型单元测试
│   ├── contract/                  # ABI、IDL、Schema、寄存器和协议契约测试
│   │   ├── api/                   # HTTP、RPC、SDK和命令接口契约测试
│   │   ├── abi/                   # 二进制布局、符号和调用约定测试
│   │   ├── idl/                   # Proto、消息和代码生成一致性测试
│   │   ├── schemas/               # JSON、YAML、配置和artifact Schema测试
│   │   ├── registers/             # 寄存器地址、位域、复位值和访问语义测试
│   │   ├── protocols/             # 总线、队列、DMA、网络和时序协议测试
│   │   └── compatibility/         # 版本、升级、降级和向后兼容测试
│   ├── subsystem/                 # 单个软件、FPGA或板卡子系统闭环测试
│   │   ├── software/              # 单个软件子系统在隔离依赖下的闭环测试
│   │   ├── firmware/              # FPGA/MCU固件子系统仿真或板上测试
│   │   └── hardware/              # 单板、接口、电源或热子系统测试
│   ├── integration/               # 软件-固件、固件-板卡等跨域集成测试
│   │   ├── software-software/     # 服务、引擎、驱动和工具之间的集成测试
│   │   ├── software-firmware/     # Host软件、Driver、固件和寄存器联调
│   │   ├── firmware-hardware/     # 固件与板卡接口、时钟、复位和外设联调
│   │   └── hardware-system/       # 板卡、主机、机箱、网络和电源集成测试
│   ├── system/                    # 整机、真实拓扑和端到端场景测试
│   │   ├── functional/            # 完整系统功能和业务场景验证
│   │   ├── performance/           # 吞吐、时延、容量、带宽和功耗验证
│   │   ├── reliability/           # 稳定性、耐久性、压力和寿命测试
│   │   ├── recovery/              # 故障注入、重试、恢复和数据一致性测试
│   │   ├── security/              # 权限、隔离、输入安全和攻击面测试
│   │   └── interoperability/      # 不同平台、版本和第三方设备互操作测试
│   ├── acceptance/                # 项目、客户或生产验收自动化
│   │   ├── product/               # 产品规格与发布Gate验收测试
│   │   ├── customer/              # 合同、客户场景和现场验收测试
│   │   └── manufacturing/         # 生产、装配、出厂和批次验收测试
│   ├── fixtures/                  # 小型稳定输入、Golden向量和仿真fixture
│   │   ├── synthetic/             # 可由规则生成的合成输入和边界数据
│   │   ├── vectors/               # 冻结协议、数值和Golden契约向量
│   │   ├── configs/               # 测试专用、无secret的配置样例
│   │   ├── traces/                # 小型脱敏事件、总线和执行trace
│   │   └── models/                # 小型模型、行为模型和参考模型fixture
│   ├── environments/              # 测试环境定义、能力清单和准备检查
│   │   ├── local/                 # 开发机和本地快速测试环境
│   │   ├── simulation/            # 软件模拟器、RTL仿真器和虚拟设备环境
│   │   ├── hil/                   # Hardware-in-the-loop连接和控制定义
│   │   └── lab/                   # 实验室设备、拓扑和校准要求
│   ├── manifests/                 # Suite、Case、环境、数据和预期artifact清单
│   └── common/                    # 公共harness、driver、oracle和测试工具
│       ├── harness/               # 测试编排、生命周期和结果收集框架
│       ├── drivers/               # 仪器、模拟器、板卡和环境控制适配器
│       ├── oracles/               # 期望结果、参考实现和判定器
│       ├── schemas/               # 测试配置、结果和artifact Schema
│       └── tools/                 # fixture、报告、覆盖和诊断辅助工具
├── experiments/                   # 可复现实验manifest、runner和分析代码
├── models/                        # 模型或算法注册、分析和小型统计摘要
├── knowledge-base/                # 静态知识网站；文档、素材和站点构建配置
├── tools/                         # 构建、生成、检查、迁移和发布工具
├── third_party/                   # 第三方依赖manifest、许可证和受控patch
└── <local-data-root>/             # 不进入Git的本地数据根
    ├── models/                    # 模型权重、checkpoint和转换产物
    ├── datasets/                  # 大型数据集、语料和输入快照
    ├── runs/                      # 活动运行和已完成运行目录
    ├── evidence/                  # 被正式报告引用的不可变证据包
    ├── build/                     # 可从源码重建的编译、综合和打包输出
    ├── cache/                     # 可重新获取或计算的缓存
    └── tmp/                       # 无长期保留价值的临时文件
```

编号只用于稳定排序，不表示生命周期必须线性执行。纯软件或纯硬件项目应通过 profile 裁剪不适用目录。

`knowledge-base/` 默认指面向人阅读的静态知识网站，不暗示问答、RAG、向量库或外部索引服务。
静态站点只需保留实际使用的内容、素材、站点配置和构建入口；不强制建立独立 `tests/`
目录。最低验证是站点可构建、内部链接有效、被引用的图片和附件存在，且页面路径不重复。
`webui/` 或 `apps/<app>/` 用于产品 Web UI，不应再用含糊的顶层 `web/` 同时表示知识库。

项目采用记录使用单值 `project_profile`（`mixed-system`、`software`、`hardware-fpga` 或
`documentation-only`）和数组 `enabled_domains`。目录存在不自动表示该 domain 已启用；以通过
`schemas/std-lock.schema.json` 校验的 `docs/std.lock.json` 为准。

## 3. Owner共置

大型项目可采用：

```text
software/<component>/docs/          # 软件组件专属需求、设计和评审
firmware/<product>/docs/            # 固件产品专属需求、架构和实现报告
hardware/boards/<board>/docs/       # 板卡专属设计、BOM、制造和验证文档
```

根 `docs/` 保留系统入口和跨 Owner 机制，不复制下级正文。小项目也可以使用根
`docs/30_*`、`40_*`、`50_*`；同一文档类型只能选择一个 canonical 位置。

## 4. 边界说明

- `notes/` 记录沟通过程；产生正式需求或决定后提升到需求、ADR或Owner设计文档。
- 投资人PPT放 `materials/investors/`，板卡单页放 `materials/products/`。
- 完整竞品分析放 `docs/15_evaluation/competitive-analysis/`，销售竞品卡放
  `materials/sales/competitive-battlecards/`。
- `docs/70_verification/` 放计划和报告，`tests/` 放可执行测试，本地数据根放大型运行证据。
- 简单项目可把契约放 `docs/60_interfaces/contracts/`；需要codegen或多域消费时使用顶层
  `interfaces/`，根文档只保留索引。
- `docs/migration/std-YYYYMMDD/` 和 `docs/98_migration/` 都可作为迁移区，validator不按目录名禁止。

### 4.1 测试authority

- `software/<component>/tests/`和`firmware/<product>/tests/`是Owner内部单元、组件和局部契约测试的默认authority。
- 根`tests/`是跨Owner契约、集成、系统和验收测试的默认authority。小项目可在tailoring中选择全部集中，但不得在根目录和Owner目录维护两份同一测试。
- `tests/fixtures/`只保存小型、稳定、可提交的输入；大型数据、原始运行输出和证据包分别放本地数据根的`datasets/`、`runs/`和`evidence/`。

### 4.2 文档与工程数据

- `hardware/boards/<board>/docs/`保存人工评审的需求、方案、计划、结论和理由。
- 同板卡的`schematic/`、`pcb/`、`mechanical/`、`bom/`、`manufacturing/`和`verification/`保存EDA源文件、机器可读数据、交付输出、脚本和小型结果。
- 正式文档通过版本化路径或artifact ID引用工程数据，不把大型二进制产物嵌入Markdown。

### 4.3 默认落位与Owner共置

`templates/path-policy.json` 中的`default_paths`是项目级或领域级默认落位。具体软件组件、固件产品或板卡的文档，使用同文件的`domain_owned_path_patterns`选择Owner路径，并在生成时显式给出`--output`。占位符`<component>`、`<product>`和`<board>`不是真实目录名，不得直接生成到仓库中。

## 5. Profile

- `software`：见 [软件项目目录结构](software-project-layout.md)。
- `mixed-system`：使用本页完整骨架。
- `hardware-fpga`：保留docs、notes、materials、interfaces、hardware、firmware、tests、tools和数据区。
- `documentation-only`：保留docs、notes、materials和必要assets。
