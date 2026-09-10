# 系统设计图文样板资产

本目录供 STD 模板和编写指南共用。图是原创、虚构的教学表达，不是项目方案或实现证据；
未使用保密 demo、HIFM 商业素材或其他项目截图。它们不要求项目采用示例设备或部署方式。

| 图号 | 文件 | 适用位置与讲述任务 | 状态 |
|---|---|---|---|
| EX-SCENE-01 | [逻辑应用场景图](application-scene-logical.png)、[生成记录](application-scene-logical.prompt.md) | 系统模板 §2.3：相机采集流水线图像，工控机处理，简化人形坐在桌前查看结果；不表示实际部署 | 虚构 Target / Planned / NOT_RUN |
| EX-DEPLOY-01 | [展示图](deployment-in-host.png)、[可编辑源](deployment-in-host.svg) | 原有同机安装样板，保留作部署细节参考，不再作为 §2.3 的主场景图 | 虚构 Target / Planned / NOT_RUN |
| EX-ARCH-01 | [轻量架构图](system-architecture-light.png)、[生成提示词](system-architecture-light.prompt.md)；另存[简洁框图](system-architecture.png)及其[SVG 源](system-architecture.svg) | 系统模板 §5.1：系统主要组成、软硬件层次与四组主要连接；不展开子系统内部 | 虚构 Target / Planned / NOT_RUN |
| EX-SW-01 | [可复用 SVG](../../../templates/diagrams/software-layered-architecture.svg)、[编辑说明](../../../templates/diagrams/README.md)；保留[PNG 视觉参考](software-architecture.png)与[生成提示词](software-architecture.prompt.md) | 系统模板 §8.1：无图标、无连接线，左侧层次名称与右侧模块分组说明组成 | 虚构 Target / Planned / NOT_RUN |
| EX-HW-01 | [板卡顶层布局](board-top-layout.png)、[SVG 源](../../../templates/diagrams/board-top-layout.svg) | 系统模板 §7.1：自研板卡器件与功能区俯视布局，不是实际 PCB 布线 | 虚构 Target / Planned / NOT_RUN |
| EX-FPGA-01 | [FPGA 程序架构](fpga-program-architecture.png)、[SVG 源](../../../templates/diagrams/fpga-program-architecture.svg) | 系统模板 §9.1：自研逻辑模块和主数据路径，不是 FPGA 芯片资源架构 | 虚构 Target / Planned / NOT_RUN |
| FIG-EX-01 / EX-RPT-01 | [可编辑逻辑上下文图](context-example.svg) | AI 指南 §8.2：报告服务的产品内外职责与交接；不是物理部署样板 | 原有虚构示例，非产品事实 |

## EX-SCENE-01 的教学假定和边界

以用户提供的三维设备图为风格参考，将产线、设备和无五官的人形统一为灰蓝三维插画。
相机位于自动流水线上，显示器放在桌面，操作人员坐在桌前；工控机作为逻辑处理节点单列。
两条箭头分别表示“采集图像”和“检测结果”，不是物理线缆，也不表示产线控制。
画面直接说明“谁在什么环境下用系统完成什么任务”，不要求还原实际厂房、真实人物、
设备位置或距离；图中比例、布局和屏幕内容不是安装、安全或实测依据。

本例客户已有流水线、相机、主机、显示器和检测应用，产品仅补充采集卡与配套驱动；不新增
自动剔除、停线或产线控制。场景图说明使用环境，架构图说明组成与连接，二者使用同一职责
边界。完整场景正文维护在[系统模板 §2.3](../../../templates/design/architecture-design.md)。

## EX-DEPLOY-01 的教学假定和边界（保留参考）

客户已有相机、工控机、显示器和检测软件，本例仅新增采集卡；卡接收/缓存图像，通过 PCIe
交给主机处理。主机显示路径不经过采集卡。外形、板形、端口、相机协议、驱动、lane 数、功耗、
散热和吞吐均未作工程规定。图中相机链路与 PCIe 不表示相同协议，具体接口在项目规格中确定。

当前 §2.3 已采用带流水线和操作人员的场景图；此安装样板及 SVG 保留，不覆盖或删除。

## EX-ARCH-01 的教学假定和边界

沿用安装案例，教学基线为 EX-CAP-01。系统层级只展示相机、工控机、显示器，以及工控机内
的采集卡、配套驱动和检测应用。采集卡不再展开接收、缓存、DMA 等内部模块。
“仅新增采集卡”指新增硬件，不意味着不需要配套主机软件。既有相机、主机、显示器和业务
检测软件仍由客户提供；不改成卡内进行检测，也不新增生产线控制职责。

当前图用轻量设备插图、工控机边界和软硬件分层表达组成，细线与短标签表达采集接口、
PCIe／设备访问、驱动 API、显示输出四组关系；软件层不是额外硬件。连线表示系统级连接，
不是逐帧数据路径、电气图或执行时序。外形和端口不能作为工程依据。
保留的简洁框图只表现包含关系；旧 `system-architecture-rendered.png` 及其提示词作为
风格比较稿保留，不再由模板和 AI 指南引用。
完整图文只维护在[系统模板 §5.1](../../../templates/design/architecture-design.md)。

用户本轮确认采用轻量架构图，图像保持不变；附件与仓库图片的解码像素一致（1774 × 887）。
§5.2 紧接图逐一描述相机、采集卡、工控机、驱动、检测应用和显示器的职责，图片不再承担
这些文字说明，也不因补充职责而下钻内部结构。

两幅主图分别说明“谁在什么场景下使用”和“由什么组成、怎样连接”。当前已补充这两类样板，
不能据此宣称时序、状态等所有图型齐备，或已完成独立读者验证。

## EX-SW-01 的教学假定和边界

这是 EX-ARCH-01 中检测应用与配套驱动的逻辑展开：客户应用包含操作界面、检测流程和图像
分析；产品驱动包含设备管理、采集控制、图像交付及状态读取，应用统一经驱动 API 使用。
灰色与蓝色沿用总图的客户/产品分工，不把客户检测算法改成驱动功能。

图展示应用层与驱动层，层次名称只在左侧出现，面板内不重复标题；模块采用纯文字框，没有
图标、连接线或箭头。驱动 API 保持在配套驱动组内，四个驱动模块并列，不表示串行流水线。
图不规定独立进程、线程、内核/用户态划分、同步/异步调用或内存复制方式；调用关系和数据流
另图表达。底部“系统定制层／定制操作系统（按需）”是条件式样板，不是本案例已确定的
组成；普通操作系统只记作运行环境，不在图中展开。仅实际定制或改造系统时保留该层，
替换具体名称并描述修改职责；否则删除。硬件接口不放进软件层，实际 Boot/BSP 等按软件职责
单独命名。图像生命周期、并发、失败传播与部署仍需正式设计确定。
完整图文维护在[系统模板 §8.1](../../../templates/design/architecture-design.md)。板卡与 FPGA 程序
图分别维护在 §7.1、§9.1，软件图不能替代它们。

## EX-HW-01 与 EX-FPGA-01 的教学假定和边界

两图是用户确认的原创 SVG 图件，以 EX-CAP-01 的采集卡职责为基础，构造采用 FPGA 和外部
帧缓存的教学变体 EX-CAP-FPGA-01。不表示原案例已作器件选型，不规定任何项目必须采用 DDR、
独立供电或图示模块。绘图未使用保密 demo、芯片厂商内部资源图或真实 PCB 数据。

EX-HW-01 是自研板卡的顶层布局示意：器件和功能区的相对位置便于解释板卡组成，细线仅示
主要接口关系。板形、孔位、封装、布局、供电和链路细节不是制造输入，也不表示 SI/PI 或热设计
已完成。EX-FPGA-01 展开我们设计的程序模块，不展开芯片 LUT/DSP/BRAM 资源；图中主箭头
不是完整控制、时钟、复位或背压网络。程序内帧队列与板外 DDR 不是同一对象，接入时仍需
补出存储访问/控制器及相应关系。两图均不代表实现或验证已完成。

图后职责说明只维护在系统模板对应章节，PNG 与 SVG 原样保留本轮确认的图，不因补正文而重画。
归档 SHA-256 如下；后续显式修改图件时同步复核源、导出图和回归检查。

| 文件 | SHA-256 |
|---|---|
| `board-top-layout.svg` | `90ad9801671ec87d2794454a34616381bdadcf10b7d4961383b3984d7e8043fb` |
| `board-top-layout.png` | `92b3624a634dc8b688cc37dcb595ef125f75a67d6acc9b22c63f5165d20634ed` |
| `fpga-program-architecture.svg` | `ffe4b0fa19bdf7a82b7f9b11a74825a6da2f94c94a286b5d497acfc37701f9fa` |
| `fpga-program-architecture.png` | `9627b7ecb92e7a1b9d0ff219fbf147ec3648a7d8ce2167488ac6f296a74997db` |

## 编辑与导出

安装图和备用框图以 SVG 为可编辑源，相应 PNG 由 SVG 导出。安装图源为 1280 × 800，
备用架构框图源为 1280 × 620；均按 2 倍导出 PNG。修改后在正常正文宽度下检查中文、
裁切和标签位置，不只检查放大画面。

当前模板采用的 `system-architecture-light.png` 是内置 imagegen 编辑生成的原始位图，
不是 SVG 导出图，也没有声称存在可编辑三维模型。编辑输入为原有原创虚构渲染图，未读取或发送
保密 demo。生成提示词随资产保存；后续渲染修改应重新检查组成、层次和文字，不依赖图像
中的物理细节推导设计事实。

`application-scene-logical.png` 由内置 imagegen 编辑生成：上一版场景作编辑目标，用户提供的
三维设备图作风格参考；最终提示词和输入角色另存于同名 `.prompt.md`。没有对应的 SVG 或
三维模型，不声称能够从矢量源重建它。偏写实的 `application-scene-production-line.png` 及
其提示词作为比较稿保留，不再由模板和 AI 指南展示。

`software-architecture.png` 由内置 imagegen 按原创虚构文字提示生成后，按用户意见编辑为
无图标、无连线的分层组成图，保留灰蓝配色；没有输入保密 demo 或项目资料。初稿与编辑的
完整提示词在同名 `.prompt.md`。该 PNG 保持不变，作为视觉参考保留。
它的重复标题与“操作系统 / 设备接口”已由当前 SVG 修正，不再作为软件组成的语义参考。

后续以灰蓝样式为参考，用 SVG 原生矩形、文字与分组重新绘制并修正了
[`software-layered-architecture.svg`](../../../templates/diagrams/software-layered-architecture.svg)。
这不是对 PNG 的自动矢量化，也不承诺像素相同；当前模板直接展示这份可编辑 SVG。
共用样式集中在其 `<style>`，复制层或模块即可扩展；不维护第二份重复 SVG，不引入 JSON
配置或生成器。复用方式与排版检查见同目录的图形模板编辑说明。

在已安装 `sharp` 的 Node.js 环境中，从 STD 仓库根运行：

```sh
node -e 'require("sharp")("docs/assets/system-design-authoring/deployment-in-host.svg", {density:144}).png().toFile("docs/assets/system-design-authoring/deployment-in-host.png")'
node -e 'require("sharp")("docs/assets/system-design-authoring/system-architecture.svg", {density:144}).png().toFile("docs/assets/system-design-authoring/system-architecture.png")'
node -e 'require("sharp")("templates/diagrams/board-top-layout.svg", {density:144}).png().toFile("docs/assets/system-design-authoring/board-top-layout.png")'
node -e 'require("sharp")("templates/diagrams/fpga-program-architecture.svg", {density:144}).png().toFile("docs/assets/system-design-authoring/fpga-program-architecture.png")'
```

两张新图的 SVG 画布分别为 1440 × 880、1440 × 860；本轮用 sharp 以 `density:144` 导出，
PNG 分别为 2880 × 1760、2880 × 1720。SVG 是编辑源，PNG 是兼容展示；本次同时保留已确认 bytes，
不同字体或渲染器重新导出的文件不承诺相同 hash。

渲染环境需有中文字体，例如本次使用的 macOS PingFang SC；工具和字体差异可能影响字形。
SVG 不嵌入远程图片、外部字体链接或执行脚本。所有展示图均在仓库内以相对路径引用，无需 Mermaid 插件。

## 模板实例化

模板用 `STD_TEMPLATE_EXAMPLE_BEGIN/END` 标记完整教学图文。`new-design` 生成项目空稿时移除
这些明确标记的教学段落，但保留章节、编写建议和项目填写位置，因此不把 STD 相对图片路径
带到另一个仓库，也不把虚构产品结论混入项目设计。作者先打开模板看样板，再在项目稿填写
自己的图文，并把正式图片保存在项目自身的资产目录。手工复制模板时也应替换整段教学内容。
