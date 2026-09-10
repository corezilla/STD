# 逻辑应用场景图生成记录

工具：内置 imagegen，编辑模式（非 CLI）。日期：2026-09-10。
输出：`application-scene-logical.png`，图号 EX-SCENE-01。

输入一：`application-scene-production-line.png`，上一版偏写实的原创虚构场景，用于保留角色和任务。
输入二：用户提供的三维设备示意 `codex-clipboard-af06cdf2-0d29-479f-90de-7ed3c6887048.png`，仅作灰蓝配色和三维插画风格参考。
本次未读取、使用或发送保密 demo；不包含项目设备规格或业务资料。

修改内容：将产线、设备和操作人员统一为简化三维示意，以逻辑箭头解释采集图像和检测结果的交接。
操作人员为无五官的灰色示意人形；图中布局、比例、距离和箭头不是实际安装或布线依据。
原偏写实稿作为比较稿保留，不再由模板和 AI 编写指南展示。

最终提示词：

```text
Use case: style-transfer.
Input image 1 is the EDIT TARGET: a too-photorealistic conveyor-camera-desk scene. Input image 2 is the STYLE REFERENCE: isolated neutral-gray/blue technical 3D device illustrations on white. Redraw the edit target as a LOGICAL APPLICATION SCENARIO in that illustrative style. It is NOT a real factory photograph, not a floor plan, and not a physical wiring diagram.

Primary objective: immediately explain the business use: parts arrive on an automated conveyor, a mounted camera captures them, the industrial PC processes the images, and an operator seated at a desk views inspection results. Major environment and human interaction only, NOT system internals.
Composition: wide landscape white background, three loosely arranged conceptual groups with generous whitespace: LEFT a compact simplified conveyor section carrying only three generic workpieces with one gray industrial camera mounted above it and pointing down; CENTER a small neutral-gray industrial PC with a discreet blue capture-card accent; RIGHT an ordinary simple desk with one monitor and one SEATED SIMPLIFIED PERSON looking at the screen. The person is a smooth neutral-gray faceless 3D pictogram/mannequin: no hair, no skin texture, no recognizable face, no realistic clothing. A simple seat, hands near desk and feet below are enough. The monitor sits ON the desk. Screen shows a tiny abstract workpiece image, no busy UI.
Style: professional conceptual illustration, clean soft-edged 3D technical objects with restrained gray/blue materials, minimal shallow shading like the reference. Conveyor, desk, person and PC all share the same simplified style. NOT photorealistic, NOT a toy/cartoon character, no industrial photographic textures, no metal scratches, no detailed nuts or rollers, no actual factory floor, walls, windows, perspective room or realistic spatial constraints. Do not show transparent glass software platforms or software tiles.
Connections: two thin clean BLUE logical arrows across the whitespace: from the camera/conveyor group toward the PC labelled "采集图像"; from PC toward the desk/monitor group labelled "检测结果". They represent logical information exchange, not physical cables. No precise cable routing, no distances, no safety-zone drawing. Do not draw a reverse arrow from PC or operator to the conveyor and do not imply automatic conveyor control.
Text: only short legible Simplified Chinese labels close to the relevant objects: "自动流水线", "工业相机", "工控机", "显示器", "操作人员", plus the two arrow labels above. No title, no explanatory paragraph, no caption, no interface IDs.
Invariants: exactly one camera above conveyor, one PC, one desk-mounted monitor, one seated non-realistic person. No extra processing devices, no robots/rejectors, no duplicated monitors. No DMA/cache/CPU/board circuitry or subsystem breakdown. The exact PC case, distances, workpiece shapes and scale are illustrative, not engineering facts. Preserve the scenario roles while simplifying their appearance. Purely fictional example, no logo or watermark.
```
