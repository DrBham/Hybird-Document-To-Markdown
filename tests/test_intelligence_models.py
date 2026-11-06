from pathlib import Path

import pytest

from document_converter.intelligence.models import (
    BoundingBox,
    DocumentIntelligenceResult,
    TextRegion,
    VisualElement,
    VisualRelationship,
)
from document_converter.intelligence.renderer import render_intelligence_markdown


def test_result_schema_rejects_invalid_geometry_and_confidence():
    with pytest.raises(ValueError, match="out of order"):
        BoundingBox(10, 5, 2, 20)

    with pytest.raises(ValueError, match="confidence"):
        TextRegion("Router", BoundingBox(0, 0, 10, 10), 1.1)


def test_renderer_preserves_text_elements_and_relationships():
    result = DocumentIntelligenceResult(
        source_path=Path("network-diagram.png"),
        backend_name="Local OCR",
        model_version="0.1.0",
        summary="A router connects two office switches.",
        text_regions=(
            TextRegion("Core | Router", BoundingBox(10, 20, 80, 50), 0.98),
        ),
        elements=(
            VisualElement("router-1", "router", "Core Router", confidence=0.9),
            VisualElement("switch-1", "switch", "Office A"),
        ),
        relationships=(
            VisualRelationship(
                "router-1", "switch-1", "connects-to", "1 Gbps", 0.85
            ),
        ),
        warnings=("Review low-resolution labels manually.",),
    )

    markdown = render_intelligence_markdown(result)

    assert "## Image analysis" in markdown
    assert "Core \\| Router" in markdown
    assert "| router-1 | router | Core Router" in markdown
    assert "`router-1` → **connects-to** → `switch-1`" in markdown
    assert "> [!WARNING]" in markdown
