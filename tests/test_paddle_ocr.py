from document_converter.intelligence.paddle_ocr import (
    PaddleOCRBackend,
    PaddleOCRBackendError,
)


class FakeResult:
    json = {
        "res": {
            "rec_texts": ["Router A", "Switch B"],
            "rec_scores": [0.98, 0.82],
            "rec_boxes": [[10, 20, 80, 50], [100, 20, 180, 50]],
        }
    }


class FakeEngine:
    def predict(self, *, input):
        assert input.endswith("topology.png")
        return [FakeResult()]


def test_paddle_adapter_maps_official_result_shape(tmp_path):
    model_directory = tmp_path / "model"
    (model_directory / "detection").mkdir(parents=True)
    (model_directory / "recognition").mkdir()
    image = tmp_path / "topology.png"
    image.write_bytes(b"fixture")
    factory_calls = []

    def factory(**options):
        factory_calls.append(options)
        return FakeEngine()

    result = PaddleOCRBackend(
        model_directory,
        model_version="test-1",
        engine_factory=factory,
    ).analyze(image)

    assert [region.text for region in result.text_regions] == [
        "Router A",
        "Switch B",
    ]
    assert result.text_regions[0].bounds.right == 80
    assert result.text_regions[0].confidence == 0.98
    assert factory_calls[0]["use_doc_unwarping"] is False


def test_paddle_adapter_requires_complete_local_model(tmp_path):
    image = tmp_path / "topology.png"
    image.write_bytes(b"fixture")

    backend = PaddleOCRBackend(
        tmp_path / "missing-model",
        model_version="test-1",
        engine_factory=lambda **options: FakeEngine(),
    )

    try:
        backend.analyze(image)
    except PaddleOCRBackendError as exc:
        message = str(exc)
    else:
        raise AssertionError("Expected an incomplete model pack to fail")

    assert "incomplete" in message.lower()
