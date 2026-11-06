"""Deterministic Markdown output for local image intelligence."""

from __future__ import annotations

from .models import BoundingBox, DocumentIntelligenceResult


def _cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def _confidence(value: float | None) -> str:
    return "—" if value is None else f"{value:.1%}"


def _bounds(value: BoundingBox | None) -> str:
    if value is None:
        return "—"
    return f"({value.left:g}, {value.top:g})–({value.right:g}, {value.bottom:g})"


def render_intelligence_markdown(result: DocumentIntelligenceResult) -> str:
    """Render a stable, reviewable representation of an image analysis."""

    lines = [
        "## Image analysis",
        "",
        f"**Source:** `{_cell(result.source_path.name)}`  ",
        f"**Engine:** {_cell(result.backend_name)} ({_cell(result.model_version)})",
    ]

    if result.summary.strip():
        lines.extend(("", result.summary.strip()))

    if result.text_regions:
        lines.extend(("", "### Detected text", ""))
        for region in result.text_regions:
            lines.append(
                f"- {_cell(region.text)} "
                f"`{_bounds(region.bounds)}` ({_confidence(region.confidence)})"
            )

    if result.elements:
        lines.extend(
            (
                "",
                "### Visual elements",
                "",
                "| ID | Type | Label | Position | Confidence |",
                "|---|---|---|---|---:|",
            )
        )
        for element in result.elements:
            lines.append(
                "| "
                + " | ".join(
                    (
                        _cell(element.identifier),
                        _cell(element.kind),
                        _cell(element.label),
                        _bounds(element.bounds),
                        _confidence(element.confidence),
                    )
                )
                + " |"
            )

    if result.relationships:
        lines.extend(("", "### Relationships", ""))
        for relationship in result.relationships:
            detail = f" — {_cell(relationship.label)}" if relationship.label else ""
            lines.append(
                f"- `{_cell(relationship.source_id)}` "
                f"→ **{_cell(relationship.kind)}** → "
                f"`{_cell(relationship.target_id)}`{detail} "
                f"({_confidence(relationship.confidence)})"
            )

    if result.warnings:
        lines.extend(("", "> [!WARNING]"))
        lines.extend(f"> {_cell(warning)}" for warning in result.warnings)

    return "\n".join(lines).rstrip() + "\n"
