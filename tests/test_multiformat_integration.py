from zipfile import ZIP_DEFLATED, ZipFile

import pytest
from openpyxl import Workbook
from pptx import Presentation

from document_converter.core.router import ConverterRouter


CONTENT_TYPES_XML = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/'
    'content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-'
    'package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.'
    'openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '</Types>'
)

RELATIONSHIPS_XML = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/'
    'relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/'
    'officeDocument/2006/relationships/officeDocument" '
    'Target="word/document.xml"/>'
    '</Relationships>'
)

DOCUMENT_XML = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/'
    'wordprocessingml/2006/main">'
    '<w:body><w:p><w:r><w:t>Checkpoint C Word</w:t></w:r></w:p></w:body>'
    '</w:document>'
)


def test_real_txt_conversion(tmp_path):
    source = tmp_path / "sample.txt"
    source.write_text("Checkpoint C plain text", encoding="utf-8")

    result = ConverterRouter().convert(source)

    assert "Checkpoint C plain text" in result.markdown


def test_real_docx_conversion(tmp_path):
    source = tmp_path / "sample.docx"

    with ZipFile(source, "w", ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", CONTENT_TYPES_XML)
        archive.writestr("_rels/.rels", RELATIONSHIPS_XML)
        archive.writestr("word/document.xml", DOCUMENT_XML)

    result = ConverterRouter().convert(source)

    assert "Checkpoint C Word" in result.markdown


def test_real_text_pdf_conversion(tmp_path):
    source = tmp_path / "sample.pdf"
    source.write_bytes(
        b"%PDF-1.4\n"
        b"1 0 obj <</Type/Catalog/Pages 2 0 R>> endobj\n"
        b"2 0 obj <</Type/Pages/Kids[3 0 R]/Count 1>> endobj\n"
        b"3 0 obj <</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]"
        b"/Resources<</Font<</F1 4 0 R>>>>/Contents 5 0 R>> endobj\n"
        b"4 0 obj <</Type/Font/Subtype/Type1/BaseFont/Helvetica>> endobj\n"
        b"5 0 obj <</Length 54>> stream\n"
        b"BT /F1 24 Tf 72 720 Td (Checkpoint C PDF) Tj ET\n"
        b"endstream endobj\n"
        b"trailer <</Root 1 0 R>>\n%%EOF"
    )

    result = ConverterRouter().convert(source)

    assert "Checkpoint C PDF" in result.markdown


@pytest.mark.parametrize(
    "extension, content, expected",
    [
        (".csv", "name,value\nCheckpoint C,1\n", "Checkpoint C"),
        (".html", "<h1>Checkpoint C HTML</h1>", "Checkpoint C HTML"),
        (".htm", "<h1>Checkpoint C HTM</h1>", "Checkpoint C HTM"),
        (".json", '{"milestone": "Checkpoint C JSON"}', "Checkpoint C JSON"),
        (".xml", "<milestone>Checkpoint C XML</milestone>", "Checkpoint C XML"),
    ],
)
def test_real_text_format_conversion(tmp_path, extension, content, expected):
    source = tmp_path / f"sample{extension}"
    source.write_text(content, encoding="utf-8")

    result = ConverterRouter().convert(source)

    assert expected in result.markdown


def test_real_pptx_conversion(tmp_path):
    source = tmp_path / "sample.pptx"
    presentation = Presentation()
    slide = presentation.slides.add_slide(presentation.slide_layouts[5])
    slide.shapes.title.text = "Checkpoint C PowerPoint"
    presentation.save(source)

    result = ConverterRouter().convert(source)

    assert "Checkpoint C PowerPoint" in result.markdown


def test_real_xlsx_conversion(tmp_path):
    source = tmp_path / "sample.xlsx"
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Milestone"
    worksheet.append(["Name", "Status"])
    worksheet.append(["Checkpoint C Excel", "Verified"])
    workbook.save(source)

    result = ConverterRouter().convert(source)

    assert "Checkpoint C Excel" in result.markdown
