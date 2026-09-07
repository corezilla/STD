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
| STD Version | `{{std_version}}` |
| Template ID | `{{template_id}}` |
| Template Conformance | `{{template_conformance}}` |
| Tailoring Reference | {{tailoring_ref}} |
| Migration Map Reference | {{migration_map_ref}} |
| Repository | `{{source_repository}}` |
| Canonical Path | `{{source_path}}` |
| Supersedes | {{supersedes}} |

> Reviewer、Approver、Approval Date 和 Release Tag 在进入相应状态时填写。Git commit/tag 是
> 外部不可变证据；不要在文档内容中伪造包含自身的 commit hash。
<!-- STD_DOCUMENT_COVER_END -->

## 1. Review scope、Revision、Inputs 与 Reviewers

## 2. Schematic Checklist

- [ ] 电源树、上电/掉电顺序和保护完整
- [ ] Clock、Reset、strap、boot 和 programming 路径完整
- [ ] Interface pin、方向、电平、终端和 reference voltage 正确
- [ ] 器件 P/N、封装、NC/DNI 和未用引脚处理明确
- [ ] Test point、debug、measurement 和 bring-up 能力充分

## 3. PCB Stack-up、Placement 与 Routing Checklist

- [ ] Stack-up、阻抗、参考平面和回流路径已冻结
- [ ] 高速 topology、长度、skew、via 和 loss 满足约束
- [ ] 电源完整性、去耦、铜厚、电流和热路径满足预算
- [ ] BGA breakout、器件 keepout、机械和装配间距可制造
- [ ] DFM/DFT、panelization、fiducial 和测试点满足生产要求

## 4. SI/PI、Thermal、Mechanical 与 EMC Evidence

## 5. BOM、Supply、Lifecycle 与 Alternate Review

## 6. Issue Log

| ID | Severity | Finding | Evidence | Owner | Disposition |
|---|---|---|---|---|---|
| <!-- TODO --> | | | | | |

## 7. Review Decision 与 Release Gate
