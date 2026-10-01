# 测试规范

## 1. 作用与范围

本规范是 STD 测试体系的入口规范，统一说明测试分层、每层职责、测试模板族和跨层通用的测试约定。
它是测试目录结构（[repository-layout.md](repository-layout.md)）、Case/工件命名
（[software-object-identifiers.md](software-object-identifiers.md)）和测试模板族
（`templates/tests/`）的共同前提，也是人和 AI Agent 进入测试体系的入口。任何测试方案、用例、计划、
报告都先对齐本规范，再落到具体模板。

## 2. 测试分层总览

测试按「被测对象层级」分四层，与设计分层一一对应，从内到外逐层扩大被测边界：

```
UT → MT → IT → ST
单元  模块  子系统  系统
```

| 层 | 前缀 | 对应设计层级 |
|---|---|---|
| 单元测试 | `UT` | `design.implementation`（ISD） |
| 模块测试 | `MT` | 软件模块（`design.definition`） |
| 子系统测试 | `IT` | 软件子系统（`design.subsystem`） |
| 系统测试 | `ST` | 软件系统（`design.software-system`） |

- **顺序固定**：先内后外。下层 PASS 不关闭上层目标；上层不重复测下层已覆盖的单点逻辑。
- 软件系统可直接包含直属模块（无子系统层）；无子系统时，`IT`（子系统层）不适用，层级退化为
  `UT → MT → ST`。

## 3. 每层职责

| 层 | 前缀 | 被测对象 | 视角 | 主要手段 | 测什么（分母） | 不测什么（边界） | 对应设计 | 模板族 |
|---|---|---|---|---|---|---|---|---|
| 单元测试 | `UT` | 单个函数/类/方法 | 白盒 | 直接调用、冻结向量、替身注入 | 单点内部逻辑、错误路径、边界输入 | 模块组装、跨函数协作 | `design.implementation`（ISD） | `tests.unit-*` |
| 模块测试 | `MT` | 单个模块 | 灰盒 | 公开入口 + 边界替身 | 模块整体行为（内部单元真实、边界替身）、公开接口契约 | 跨模块协议、边界外真实依赖 | `design.definition` | `tests.module-*` |
| 子系统测试 | `IT` | 单个子系统 | 灰盒 | 跨模块流程、子系统 harness | 跨模块流程、子系统对外接口、承接的系统约束与机制要求 | 跨子系统协作、系统业务 | `design.subsystem` | `tests.subsystem-*` |
| 系统测试 | `ST` | 整个系统 | 黑盒 | 端到端流程、真实/预生产环境 | 端到端流程、系统对外接口、系统约束预算、机制端到端保证 | 内部协作、单点实现 | `design.software-system` | `tests.system-*` |

### 视角递进

```
白盒 ───────── 灰盒 ───────── 黑盒
  UT          MT   IT          ST
```

随层级升高，对单点实现的可见性下降、对系统整体行为的关注上升。

## 4. 分层原则

1. **下层不关闭上层**：`UT` PASS 不推导 `MT` PASS，逐层递推；每层只证明自己边界内的保证。
2. **边界不重叠**：每层测「自己对象层级的行为」，不重复测下层已覆盖的单点逻辑，也不越界测
   上层的系统保证。单点实现归 `UT`/`MT`，跨模块流程与子系统接口归 `IT`，系统业务归 `ST`。
3. **分母对照设计**：每层的分母来源是该层对应设计文档声明的验证项（VRC）；每个 VRC 至少一条
   Case，验证项是设计声明的必测点。

## 5. 测试模板族

测试按「层 × 工件」生成文档。工件五类，各司其职、状态分层：

| 工件 | 作用 | 持有状态 |
|---|---|---|
| 方案（`*-test-scheme`） | 测试分类 + Case 清单（唯一登记） | 设计状态 |
| 用例（`*-case`） | 单 Case 完整设计（一 Case 一文档） | 实现状态 |
| 计划（`*-test-plan`） | 可执行作业指令（Go/No-Go + ENV 分配 + 逐 Case 序列） | 活动组织 |
| 报告（`*-test-report`） | 本次执行结论（逐 Case + Verdict + 覆盖复算 + Gate） | 执行状态 + Verdict |
| 资产（`asset-design`） | 测试件契约与自检（阶段无关，跨层复用） | 资产开发/验证状态 |

各层模板：

| 层 | scheme | case | plan | report |
|---|---|---|---|---|
| 单元 | `tests.unit-test-scheme` | `tests.unit-case` | `tests.unit-test-plan` | `tests.unit-test-report` |
| 模块 | `tests.module-test-scheme` | `tests.module-case` | `tests.module-test-plan` | `tests.module-test-report` |
| 子系统 | `tests.subsystem-test-scheme` | `tests.subsystem-case` | `tests.subsystem-test-plan` | `tests.subsystem-test-report` |
| 系统 | `tests.system-test-scheme` | `tests.system-case` | `tests.system-test-plan` | `tests.system-test-report` |
| 通用 | — | `tests.asset-design` | — | — |

## 6. 通用测试规范

以下约定跨所有层级通用，具体落地见各模板族。

### 6.1 状态分层

- **设计状态**（方案 `*-test-scheme` §3 清单持有）：用例是否已设计（Designed 等）。
- **实现状态**（`*-case` §7 持有）：测试脚本 Planned / Implemented。
- **执行状态 + Verdict**（`*-test-report` 持有）：执行状态（`NOT_RUN`/`BLOCKED`/`INVALID`）
  与判定（`PASS`/`FAIL`）只出现在 Run 报告。

三层不混用：方案不填执行结果，case 不预填 Verdict，报告不重写用例设计。

### 6.2 测试资产

测试件（harness、替身/fake、受控时钟、生成器、注入框架）不是产品功能，有自己的契约与自检：

- 资产契约以 `tests.asset-design` 文档为唯一 authority；方案/case/计划只引用，不复制行为。
- 资产两层状态：开发状态（Planned/Implemented）+ 验证状态（Unverified/Verified）。
- 测试计划 Step 0 只接受 `Verified` 的资产进入执行；自检 PASS 不是产品 PASS。

### 6.3 环境模型

- **方案定义环境类型**（`*-test-scheme` §1.7）：列出抽象环境类别及其行为/真伪。
- **计划分配 ENV 实例**（`*-test-plan` §4）：编号 + 配置 + Owner + 分配给哪些 Case。
- **case 引用类型 + 编号**（`*-case` §2）：不重复描述环境本身。

### 6.4 命名与工件

Case ID 格式 `<阶段前缀>-<对象短名>-<NNN>`，阶段前缀随层固定：`UT`/`MT`/`IT`/`ST`。

`<对象短名>` 取被测对象的正式短名（在对象登记表登记；未登记时用对象 ID）。Case 一文档一 Case，
Document ID = Case ID；Case 文档与脚本同名（同 stem），脚本文件名 = Case ID 字面 + 语言后缀。

方案（scheme）与计划（plan）每阶段一份，无独立前缀，按阶段落位、用文件名
`<stage>-test-scheme.md` / `<stage>-test-plan.md` 引用。

### 6.5 报告与证据

- 报告是 Verdict 的唯一权威；没有有效 Run 不得写 PASS。
- 逐 Case 结果引用 Run ID 与证据路径，不把 stdout 全文搬进报告。
- 报告引用既有预期，不为通过测试而修改 Oracle；未执行保留 NOT_RUN，不伪造结果。

### 6.6 可测试性缺口

产品缺少注入点/测试接口/可观察出口是可测试性缺口，回路是：方案 Gap 表登记 → 设计文档未决项/
需求变更 → 钩子落地后资产才承接；禁止在测试件里硬绕产品缺陷（如直接改内部状态伪造观察结果）。

## 7. 与其它规范的关系

- 目录结构与落位：见 [repository-layout.md](repository-layout.md) §4.1。
- Case/工件命名与对象 ID：见 [software-object-identifiers.md](software-object-identifiers.md)。
- 模板选择：见 [template-selection.md](template-selection.md)。
- 验证专项编写方法：见 [ai-guides/verification.md](ai-guides/verification.md)。
