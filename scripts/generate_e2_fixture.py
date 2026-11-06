"""Generate a project-owned network-diagram OCR fixture."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REFERENCE_TEXT = (
    "TOPOLOGI JARINGAN KANTOR INTERNET ROUTER UTAMA 1 GBPS "
    "SWITCH LANTAI 1 KOMPUTER ADMIN"
)


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/segoeui.ttf"),
    )
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def _centered_text(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    font: ImageFont.ImageFont,
) -> None:
    bounds = draw.textbbox((0, 0), text, font=font)
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    x = box[0] + (box[2] - box[0] - width) / 2
    y = box[1] + (box[3] - box[1] - height) / 2
    draw.text((x, y), text, fill="#171614", font=font)


def generate(output: Path) -> None:
    image = Image.new("RGB", (1400, 820), "#F2EFE7")
    draw = ImageDraw.Draw(image)
    title_font = _font(46)
    label_font = _font(32)
    link_font = _font(27)
    draw.text(
        (365, 38),
        "TOPOLOGI JARINGAN KANTOR",
        fill="#171614",
        font=title_font,
    )

    boxes = (
        ((540, 145, 860, 250), "INTERNET"),
        ((500, 340, 900, 455), "ROUTER UTAMA"),
        ((500, 555, 900, 670), "SWITCH LANTAI 1"),
        ((985, 555, 1345, 670), "KOMPUTER ADMIN"),
    )
    for box, label in boxes:
        draw.rounded_rectangle(
            box,
            radius=18,
            fill="#D8D2C5",
            outline="#574D3E",
            width=5,
        )
        _centered_text(draw, box, label, label_font)

    draw.line((700, 250, 700, 340), fill="#574D3E", width=7)
    draw.polygon(((685, 320), (715, 320), (700, 345)), fill="#574D3E")
    draw.line((700, 455, 700, 555), fill="#574D3E", width=7)
    draw.polygon(((685, 535), (715, 535), (700, 560)), fill="#574D3E")
    draw.text((725, 485), "1 GBPS", fill="#574D3E", font=link_font)
    draw.line((900, 612, 985, 612), fill="#574D3E", width=7)
    draw.polygon(((965, 597), (965, 627), (990, 612)), fill="#574D3E")

    output.parent.mkdir(parents=True, exist_ok=True)
    output_format = "PDF" if output.suffix.lower() == ".pdf" else "PNG"
    image.save(output, format=output_format)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    arguments = parser.parse_args()
    generate(arguments.output)
    print(arguments.output.resolve())
    print(f"reference: {REFERENCE_TEXT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
