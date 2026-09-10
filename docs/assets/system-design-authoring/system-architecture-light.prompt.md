# 轻量系统架构图生成记录

工具：内置 imagegen，编辑模式（非 CLI）。日期：2026-09-10。
编辑输入：本目录已有的原创虚构 `system-architecture-rendered.png`，只保留主要组成和归属。
输出：`system-architecture-light.png`。未读取或发送项目技术资料、HIFM 截图或保密 demo。
本版弱化三维质感，突出四组系统级连接；连线不是逐帧数据路径或底层电气连接依据。
旧渲染图保留为比较稿，不再由模板引用。

最终提示词：

```text
Use case: style-transfer.
Edit the referenced fictional architecture illustration into a LIGHT, PROFESSIONAL ENGINEERING ARCHITECTURE DIAGRAM. Keep its six major components and their ownership/location semantics, but substantially simplify the rendering and make architectural connections explicit.
Style: white background, crisp restrained 2.5D technical pictograms, tiny hints of depth only, thin slate/blue lines, near-zero shadows. NOT photorealistic, NOT glossy, NOT product marketing, NOT heavy 3D. No transparent metal enclosure, no exploded floating glass platforms, no gears as giant decorations. Not plain text-only boxes: camera, capture card and display should be recognizable minimal equipment pictograms.
Layout: landscape, generous whitespace. A large very light thin-line grouping region labelled "工控机" in the center; this is the host location, not a rendered chassis. Inside its lower hardware band, a single simple blue card pictogram labelled "图像采集卡". Inside its upper software band, two small software pictograms labelled "配套驱动" (muted blue) and "检测应用" (gray). Label the bands "软件层" and "硬件层" only once. The industrial camera "工业相机" sits outside the host on the left, and one small "显示器" outside on the right. Do not add any other components.
Connections are the main subject. Use clean thin orthogonal lines with clearly attached endpoints and brief labels, avoiding crossings and running through any text. Draw EXACTLY these four relationships: (1) camera to capture card labelled "采集接口"; (2) capture card to driver across the hardware/software boundary labelled "PCIe / 设备访问"; (3) driver to inspection application labelled "驱动 API"; (4) inspection application to display labelled "显示输出". Use lines without arrowheads, since this is a connection view, not an execution/data-flow sequence. Do not route any line from the capture card directly to the display. No decorative real cables. A software link is not a separate physical device.
Typography: clear dark Simplified Chinese sans-serif, only the component, band and four connector labels stated above. No extra sentences, title, legend, captions, interface IDs, acronyms beyond PCIe and API.
Invariants: exactly one camera, one PC grouping, one card inside the PC, one driver, one application, one display. Blue card and driver are product-supplied; gray equipment/application are customer-supplied. Show only major system composition and hierarchy: NO DMA, cache, RAM, CPU, register, chip, board circuitry, internal subsystem breakdown, or exact hardware dimensions. Purely fictional teaching diagram, no logos, no confidential source. Make the architecture readable at a normal document width.
```
