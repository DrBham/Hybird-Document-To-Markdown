from pathlib import Path

from document_converter.core.models import ConversionResult
from document_converter.intelligence.converter import IntelligentDocumentConverter
from document_converter.intelligence.extractor import ExtractedImage


class FakeConverter:
    def convert(self, file_path):
        return ConversionResult(file_path, "docx", "# Existing document\n")


class FakeExtractor:
    def extract(self, source, output_directory):
        image = output_directory / "embedded.png"
        image.write_bytes(b"fixture")
        return (ExtractedImage(image, "Embedded image: diagram.png"),)


class FakeIntelligence:
    def analyze_to_markdown(self, image_path):
        assert image_path.name == "embedded.png"
        return "## Image analysis\n\nRouter connects to switch.\n"


def test_converter_appends_local_image_analysis(tmp_path):
    source = tmp_path / "network.docx"
    source.write_bytes(b"fixture")
    converter = IntelligentDocumentConverter(
        FakeConverter(),
        FakeIntelligence(),
        FakeExtractor(),
    )

    result = converter.convert(source)

    assert result.markdown.startswith("# Existing document")
    assert "# Local document intelligence" in result.markdown
    assert "Embedded image: diagram.png" in result.markdown
    assert "Router connects to switch." in result.markdown
