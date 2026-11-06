from document_converter.intelligence.models import DocumentIntelligenceResult
from document_converter.intelligence.service import LocalDocumentIntelligence


class FakeBackend:
    name = "Fake local backend"

    def analyze(self, image_path):
        return DocumentIntelligenceResult(
            source_path=image_path,
            backend_name=self.name,
            model_version="test",
            summary="Local analysis complete.",
        )


def test_service_analyzes_supported_image_locally(tmp_path):
    image = tmp_path / "diagram.png"
    image.write_bytes(b"not decoded by the fake backend")

    markdown = LocalDocumentIntelligence(FakeBackend()).analyze_to_markdown(image)

    assert "diagram.png" in markdown
    assert "Local analysis complete." in markdown


def test_service_rejects_non_image_input(tmp_path):
    document = tmp_path / "notes.txt"
    document.write_text("text", encoding="utf-8")

    try:
        LocalDocumentIntelligence(FakeBackend()).analyze_to_markdown(document)
    except ValueError as exc:
        message = str(exc)
    else:
        raise AssertionError("Expected non-image input to be rejected")

    assert "unsupported image format" in message
