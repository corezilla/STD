# 软件架构示例图生成记录

工具：内置 imagegen，生成后两轮编辑（非 CLI）。日期：2026-09-10。
输出：`software-architecture.png`，图号 EX-SW-01。
输入：仅以下原创虚构文字提示；沿用已确认架构图的灰蓝视觉语言，没有传入图片、保密 demo 或项目技术资料。

图为工控机主机软件的逻辑模块视图，灰色为客户检测应用，蓝色为产品配套驱动。
模块不等同于进程、线程或部署服务；操作系统条带是依赖边界，不规定驱动 API 的用户态/内核态归属。
本轮只生成软件图；硬件和固件专项图尚未补充。

## 1. 初稿生成提示词（含图标与连线，已被后续编辑替换）

```text
Use case: infographic-diagram.
Create a professional SOFTWARE ARCHITECTURE illustration for a Chinese engineering system-design template. This is a fictional teaching example of the industrial vision capture system already illustrated in the document. The diagram must expand only the host SOFTWARE: customer inspection application and supplied capture driver. It is a LOGICAL MODULE VIEW, not a physical installation, hardware diagram, sequence chart, or actual OS/kernel implementation claim.

Appearance: pure white background, wide landscape approximately 16:10, precise front-facing layout, generous whitespace, restrained light gray and blue palette. Use tasteful shallow 3D software tiles with tiny simple line icons, soft corners, thin grouping borders, barely perceptible shadows. Professional and clean like a technical architecture illustration, NOT a glossy futuristic glass stack. Connectors, containment and layer hierarchy are the focus. Text is short, large, legible Simplified Chinese in dark sans-serif. No paragraphs, no explanatory footnotes, no title banner, no watermark.

Exact structure, top to bottom:
1. A thin outer boundary labelled "工控机主机软件" containing everything.
2. Top light gray application group labelled "客户检测应用". Three equal gray tiles in one horizontal row, left "操作界面" with a window icon, center "检测流程" with a simple workflow icon, right "图像分析" with an image icon. Connect adjacent tiles with clean bidirectional horizontal arrows. Left connector short label "操作 / 结果"; right connector short label "图像 / 判定". These are logical request/result handoffs, not strict frame execution order.
3. Below it a blue-tinted group labelled "配套驱动". At the top INSIDE this group a single wide slim light blue interface bar labelled "驱动 API". The "检测流程" tile above connects to this API bar with TWO clearly separated vertical arrows in the gap: downward arrow labelled "控制请求", upward arrow labelled "图像 / 状态". No arrows bypass the interface bar.
4. Within the SAME driver group, under the API bar, one row of FOUR blue tiles: "设备管理" (device plug icon), "采集控制" (play/stop icon), "图像交付" (stacked images icon), "状态读取" (status pulse icon). Draw a thin vertical connector from the API bar to each tile. These lines are interface-to-module responsibility mapping, not a serial pipeline. Do not connect the four modules in a serial chain.
5. Below the driver group, inside the outer host boundary, a narrow neutral-gray foundation strip labelled "操作系统 / 设备接口". A single short thin connector between the bottom boundary of the driver group and this strip labelled "设备访问". Do not draw additional operating system internals.

Invariants: application tiles are neutral gray (customer supplied); driver modules are blue (product supplied); the interface bar belongs inside the driver group. Exactly three application modules and four driver modules. All connectors end on the intended box boundaries without crossing labels. Keep all labels readable at ordinary document width. Software tiles are logical functions, not servers or physical circuit boards.
Exclude: industrial camera, conveyor, person, monitor hardware, PC enclosure, PCIe board picture, FPGA, firmware blocks, CPU/cache/DMA/register details, network/cloud/database, invented SDK or standalone service, physical cables, microscopic API fields, code paths, extra modules or elaborate annotations. This is a fictional drawing, no confidential technical inputs.
```

## 2. 分层版编辑

工具：内置 imagegen，编辑模式。输入：上述初稿（SHA-256 `b452cdc72aaf4500d70af45136a7852fc1c8ae9f02359d8b7c269f439d6e36a5`）。
按用户要求移除图标和连接线，左侧增加三层名称；没有改变模块职责。

```text
Use case: precise-object-edit.
Input image 1 is the edit target: the existing fictional industrial-vision software architecture diagram.
Revise ONLY the presentation into a clean LAYERED COMPOSITION view. Keep the same software scope, all seven module names and application-versus-driver ownership. No new modules or functionality.

Required changes:
- Remove EVERY module icon, pictogram and decorative symbol.
- Remove EVERY connector, line between modules, arrow and arrowhead. Remove ALL former connector labels: "操作 / 结果", "图像 / 判定", "控制请求", "图像 / 状态", "设备访问". Box outlines are allowed; relationship connector lines are not.
- Express hierarchy ONLY through vertical stacking, containment, alignment and pale grouped background bands.
- Add a clearly separated left-hand column of layer names, centered vertically beside the corresponding band. Exactly three left labels: "应用层", "驱动层", "系统支撑层". These labels are horizontal text, not rotated.
- Make module rectangles compact text-only cards with large centered Chinese names. Avoid giant empty boxes where icons used to be. Uniform row alignment makes the layout extensible to many modules.

Exact arrangement:
Main content stack occupies the right approximately 82% of the landscape image; left label column has generous whitespace and no boxes or brackets.
Small main heading "工控机主机软件" above the right stack.
Top band, aligned with left label "应用层": pale neutral gray group with modest group heading "客户检测应用", containing one row of three equal text-only cards "操作界面", "检测流程", "图像分析".
Middle band, aligned with left label "驱动层": pale blue group with modest heading "配套驱动". Inside the SAME group, one slim full-width bar labelled "驱动 API", then immediately below, with whitespace but absolutely no connecting lines, one row of FOUR equal text-only blue-tinted cards "设备管理", "采集控制", "图像交付", "状态读取". The API remains inside the driver group and is not a separate independent layer.
Bottom band, aligned with left label "系统支撑层": one neutral gray full-width text-only bar "操作系统 / 设备接口". No submodules.

Style: pure white background, restrained gray and blue technical-document palette, front-facing orthogonal alignment, very thin rounded borders, subtle shallow shading, no pronounced 3D, no glass shelves. No gridlines outside box outlines. Strong legible Simplified Chinese sans-serif type. Spacious but compact overall, suitable for an engineering Markdown page around 900 pixels wide. No explanatory paragraphs or legends inside the image.
Do not show physical equipment, camera, conveyor, people, firmware, FPGA, chips, database, cloud, CPU, DMA or cache. This view intentionally omits calls, data flow, sequence and deployment details. Preserve the original text names exactly, no spelling changes, no extra labels, logo or watermark.
```

## 3. 最终配色与排版编辑

工具：内置 imagegen，编辑模式。输入：第 2 步分层版。输出替换 `software-architecture.png`。
层背景更浅，模块卡片更深，统一间距与圆角；结构、名称、无图标/无连线保持不变。
以下为最终编辑提示词，原始生成输出保留在生成工具的本地输出目录。

```text
Use case: precise-object-edit.
Edit the attached software LAYERED COMPOSITION diagram. Polish visual appearance ONLY. Preserve exactly the same labels, three layers, seven modules, grouping/containment and left-side layer-name column. Absolutely NO icons, NO pictograms, NO connector lines, NO arrows and no new content.

Primary improvement: stronger, tasteful distinction between the very pale LAYER BACKGROUND and the more saturated/darker MODULE CARDS sitting inside each layer. Current version is too uniform and pale. Make it feel like a professionally typeset technical architecture figure, not a generic default spreadsheet.

Composition and exact text invariants:
Heading above the main right-side stack: "工控机主机软件".
Left labels aligned vertically with their layers: "应用层", "驱动层", "系统支撑层".
Top group heading "客户检测应用", three equal text-only cards "操作界面", "检测流程", "图像分析".
Middle group heading "配套驱动", one slim full-width interface bar "驱动 API", then four equal text-only cards "设备管理", "采集控制", "图像交付", "状态读取". API belongs inside the driver layer, not a separate new layer.
Bottom layer contains one full-width module "操作系统 / 设备接口".

Visual refinement:
- Pure white page background, clean front view. Broad landscape layout with comfortable outer margins.
- Top application's layer panel almost-white cool neutral #F4F6F8; its module cards clearly stronger slate-gray #D3DCE5, with dark navy-gray text.
- Driver layer panel very pale blue #F0F6FD; four module cards medium soft blue #9FC5EC, noticeably darker than the group background, with dark navy text for strong legibility. The API bar uses intermediate pale blue #D0E3F7 so the interface strip and modules are visibly distinct but belong to the same layer.
- System support layer panel light neutral #F4F6F8; its single inset full-width module uses slate-gray #D3DCE5, consistent with customer-provided foundation.
- Thin unobtrusive panel borders, module borders just slightly stronger than panel borders. Only a subtle one- or two-pixel lifted shadow on module cards. No glossy metal, glass, neon, strong gradients or excessive 3D.
- Consistent moderate corner radius, carefully balanced internal padding and module gaps, equal card heights within each row, consistent group-header baseline.
- Left layer names in bold dark slate, right module names in semibold dark navy. Clear hierarchy: main title strongest, layer names next, group headings modest, module names prominent and centered. Slightly less oversized type than the source while remaining readable around 900px document width.
- Keep modules compact enough for a practical architecture chart; no empty space reserved for deleted icons.
Maintain blue=product driver, gray=customer application/support. Do NOT add a legend, caption, arrows, connecting lines, decorative stripes, icons, implementation details or any additional wording. Layer panels and cards may have outlines, but nothing connects them. Purely fictional example.
```
