<!-- STD_DOCUMENT_COVER_BEGIN -->
# {{document_title}}

| 文档字段 | 值 |
|---|---|
| Document ID | `{{document_id}}` |
| Document Version | `{{document_version}}` |
| Status | `{{document_status}}` |
| Project | `{{project}}` |
| Authority | `{{authority}}` |
| Document Owner | {{document_owner}} |
| Authors | {{authors}} |
| Created Date | `{{created_at}}` |
| Last Modified Date | `{{last_modified_at}}` |
| Template ID | `{{template_id}}` |
| Template Version | `{{template_version}}` |
| Template Conformance | `{{template_conformance}}` |
| Tailoring Reference | {{tailoring_ref}} |
| Migration Map Reference | {{migration_map_ref}} |
| Repository | `{{source_repository}}` |
| Canonical Path | `{{source_path}}` |
| Supersedes | {{supersedes}} |

> Reviewer、Approver、Approval Date 和 Release Tag 在进入相应状态时填写。Git commit/tag 是
> 外部不可变证据；不要在文档内容中伪造包含自身的 commit hash。
<!-- STD_DOCUMENT_COVER_END -->

<!--
编写建议：从产品要实现的功能和外部接口开始，再展开器件、电源、时钟、PCB 和验证。
数值必须带单位、条件和证据等级；示例必须替换。编写规范见 docs/design-writing-guide.md。
-->

## 1. 产品用途、问题与成功条件

| 项目 | 内容 |
|---|---|
| 使用场景 | <!-- 示例：单槽 PCIe 加速卡 --> |
| 要解决的问题 | <!-- TODO --> |
| 关键功能 | <!-- TODO --> |
| 成功条件 | <!-- 示例：所有电源轨通过、链路稳定枚举、热稳态不过限 --> |
| Non-goals | <!-- TODO --> |

### 1.1 继承的上级约束与落实方式

<details>
<summary>本节编写建议、规范与示例</summary>

**本节目的**：把系统或父单元分配给板卡的预算和行为要求转为本地设计输入，避免板卡只列
自己的目标，却无法证明其接入后仍满足系统约束。

**必须写清楚**：上级 Document ID、固定版本或提交、Constraint ID、决定状态及适用配置；
继承的功耗、尺寸、散热、链路等预算与启动、保护、制造测试等行为约束；本地落实位置、
内部再分配、可自行选择/不可改变的范围，以及本地验证与系统组合验证的责任和条件。

**编写规范**：用来源文档与 Constraint ID 联合定位，沿用上级 ID；细分项关联父约束，不把
拟议输入当作已批准决定。正文解释落实到哪些器件、电源树、原理图页、PCB 区域、固件或测试
预留，字段和接口引用唯一契约。器件选择可在已给自由度内调整，但不能静默放宽输入功率、
风道、启动时序或故障保护要求。确无父单元时说明独立责任及直接需求来源，不能用 N/A 隐藏
缺失输入；不必另建 `design.definition` 文档来重复承接。

内部预算计入转换损耗、公共开销和余量，以相同负载、温度、配置及测量边界组合校核。板卡
输入功率若已包含 FPGA，系统不能把两者再次相加。§7 保留推导，§10 落实制造测试预留，
§12 按同一约束区分板级验证和整机供电、风道、链路及保护联动验证。缺口记录差值、影响和
裁决责任，不能修改测试预期来假装满足；上级变更只在项目明确采用后重新评估。

**抽象示例**：虚构上级拟议约束 `CON-PWR-01` 限定板卡输入不超过 100 W，已含转换损耗和
板载风扇。板卡暂分逻辑与存储 80 W、损耗和风扇 10 W、余量 10 W，并在电源与热设计中推导
适用负载和环境；可选择器件，不能把损耗移出计账。板级按同一输入边界测量，整机还需验证
规定插槽组合、供电和风道下的行为，单板通过不能关闭整机验证。数值仅为写法示例，不是实测。

**完成条件**：每项继承约束可追到固定来源、本地落实/内部再分配及验证，自由度与禁止变更
边界明确；本地验证与系统组合验证分别有责任、条件和证据状态，待验证或不满足的项不冒称闭合。

</details>

| Constraint ID / 上级基线与决定状态 | 适用条件与测量边界 | 继承预算或行为约束 | 可自行选择/不可改变 | 本地落实/内部再分配 | 本地验证与系统组合验证/责任 | 差距/变更影响/证据状态 |
|---|---|---|---|---|---|---|

## 2. 系统边界与功能清单

| Function ID | 输入 | 硬件行为 | 输出 | 失败/保护 | 验收条件 |
|---|---|---|---|---|---|
| HW-F-001 | 12 V 输入 | 转换并监控核心电源 | 0.85 V rail | OVP/OCP shutdown | 全负载电压在容差内 |

## 3. 功能框图、数据流与控制流

```mermaid
flowchart LR
    HOST[Host] -->|PCIe data| FPGA[FPGA/SoC]
    FPGA -->|DDR transactions| MEM[Memory]
    MCU[Controller] -->|power/reset/control| FPGA
```

逐条解释数据、控制、电源、时钟和复位如何穿过各模块。

## 4. 模块、器件与实现位置

| Block | 职责 | 关键器件/P-N | Provided interface | 依赖 | 原理图/PCB 位置 |
|---|---|---|---|---|---|
| Power | 生成核心 rail | <!-- TODO --> | PGOOD | 12 V | `SCH-POWER` |

记录正式料号、封装、生命周期、供应风险、替代料和 qualification 状态。

## 5. 外部接口

| Interface | Connector/Pin | Protocol/Level | Direction | Rate/Timing | Protection | Authority |
|---|---|---|---|---|---|---|
| PCIe | J1 | Gen5 x8 | bidirectional | 32 GT/s | ESD | interface spec |

按 `docs/interface-data-mapping-standard.md` 承接接口族#成员 ID，不另外复制寄存器/信号 authority；标准号、版本、适用部分与项目选项写全，自定义信号明确方向、位宽、时钟/时序、电压/电平及其他适用电气条件。

| 接口/信号/寄存器成员 ID / 上级 Constraint | 机器源 / selector / 版本/revision/hash | 标准绑定 / 项目条件 | 提供/消费 / 器件端口/原理图位置或未实现 | 设计 V → 板级 Case / 系统组合验证 |
|---|---|---|---|---|

## 6. 电源、时钟、复位与启动顺序

| Rail/Clock/Reset | Source | Consumer | Target/Tolerance | Sequence dependency | Monitor |
|---|---|---|---|---|---|
| VCORE | U10 | FPGA core | 0.85 V ±3% | after 12V_OK | ADC0 |

提供启动和关断时序，说明异常时的保护和恢复。

## 7. 高速、PCB、机械与热设计

记录 stack-up、阻抗、loss budget、SI/PI、布局布线、尺寸、安装、风道、热模型和环境范围。
预算关联 §1.1 的 Constraint ID，说明分配、损耗、余量及组合推导，不把本地目标代替上级要求。

| Budget | Target | Condition | Method/tool | Margin | Evidence |
|---|---|---|---|---|---|
| 热阻 | <!-- TODO --> | ambient/load/airflow | simulation | | modeled |

## 8. 配置、BOM 与产品变体

| Variant | Population/config | Capability difference | Compatibility | Identification |
|---|---|---|---|---|
| <!-- TODO --> | | | | |

## 9. 故障、保护、诊断与恢复

| Failure | Detection | Protection | Observable signal | Recovery | Residual risk |
|---|---|---|---|---|---|
| over-temperature | sensor threshold | throttle/shutdown | alert + latch | cool + explicit reset | <!-- TODO --> |

## 10. 制造、测试与 Bring-up

给出 DFM/DFT、test point、边界扫描、产测、首板上电顺序、预期测量值和停止条件。
关联 §1.1 分配的测试能力与 Constraint ID，定位原理图/PCB/固件的预留及装配后的可达性。

## 11. 实现交付物与变更计划

| 顺序 | 交付物/变更 | 文件/页/区域 | Owner | 输入 | 完成条件 |
|---:|---|---|---|---|---|
| 1 | 电源原理图 | `hardware/schematic/power.kicad_sch` | EE | rail budget | ERC + review |

## 12. Verification 与验收

将 §1.1 的 Constraint ID 与功能/需求一起映射到验收。板级检查验证本地落实；系统组合验证
检查多板、供电、散热、链路及保护的共同条件，注明系统责任方和交接证据。两类结果分开记录，
局部 PASS 不关闭系统目标；未执行写 NOT_RUN，差距返回原约束责任方。

| Function/Requirement/Constraint ID | 本地/系统组合范围 | 方法 | 条件与测量边界 | 测量/Oracle | 验证责任 | Evidence | 状态 |
|---|---|---|---|---|---|---|---|
| HW-F-001 | 本地：板卡电源轨 | bench test | min/nominal/max load | voltage tolerance | EE | NOT_RUN | Planned |

区分 analysis、simulation、inspection、demonstration 和 test；区分估算与实测。

## 13. 风险、未决问题与决定

| ID | 问题/风险 | 影响 | Owner | 关闭证据/Gate | 状态 |
|---|---|---|---|---|---|
| <!-- TODO --> | | | | | |
