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

## 1. Design、Device、Board 与 Toolchain Baseline

固定 RTL commit、IP version、part/package/speed grade、constraints 和工具版本。

## 2. Build Configuration 与 Reproducibility

## 3. Synthesis Results

| Resource | Used | Available | Utilization | Budget | Margin |
|---|---:|---:|---:|---:|---:|
| <!-- TODO --> | | | | | |

## 4. Implementation、Placement 与 Routing Results

## 5. Timing Closure

记录 clocks、WNS/TNS、failing paths、exceptions、unconstrained paths 和 CDC/RDC 结果。

## 6. Power、Thermal 与 Activity Assumptions

## 7. DRC、Methodology、Lint、CDC 与 Formal Results

## 8. Bitstream、Hash、Security 与 Programming

## 9. Simulation、Hardware Test 与 Model Correlation

## 10. Waiver、Known Limitation、Risk 与 Release Gate
