
"""Custom TXT to Markdown converter.

Consolidated TXT processing module.
Uses Python standard library only for conversion logic.
"""

from __future__ import annotations

import re
from pathlib import Path

from ..core.base_converter import BaseConverter
from ..core.models import ConversionResult
from ..core.validator import validate_file


class BlockSplitter:
    """Split text into blocks separated by blank lines."""

    @staticmethod
    def split(text: str) -> list[str]:
        if not isinstance(text, str):
            raise TypeError("Input must be a string")

        if not text.strip():
            return []

        normalized = (
            text.replace("\r\n", "\n")
            .replace("\r", "\n")
        )

        blocks = re.split(r"\n[ \t]*\n+", normalized)

        return [block for block in blocks if block.strip()]


class BlockClassifier:
    """Identify probable Python code blocks."""

    CODE_PATTERN = re.compile(
        r"^\s*(def|class|async\s+def)\s+\w+"
    )

    @classmethod
    def is_code_block(cls, block: str) -> bool:
        if not isinstance(block, str):
            raise TypeError("Block must be a string")

        lines = block.splitlines()

        if len(lines) < 2:
            return False

        has_code_declaration = any(
            cls.CODE_PATTERN.match(line)
            for line in lines
        )

        has_indentation = any(
            line.startswith(("    ", "\t"))
            for line in lines
        )

        return has_code_declaration and has_indentation


class TXTConverter(BaseConverter):
    """Convert TXT files into Markdown content."""

    H1_UNDERLINE = re.compile(r"^={3,}$")
    H2_UNDERLINE = re.compile(r"^-{3,}$")

    BULLET_PATTERN = re.compile(
        r"^(\s*)([-*•])\s+(.+)$"
        )

    NUMBERED_PATTERN = re.compile(
        r"^(\s*)(\d+)[.)]\s+(.+)$"
        )

    def convert(self, file_path: Path) -> ConversionResult:
        """Read TXT and return its Markdown representation."""

        validate_file(file_path)

        if file_path.suffix.lower() != ".txt":
            raise ValueError(
                "TXTConverter only supports .txt files"
            )

        content = file_path.read_text(encoding="utf-8")
        markdown = self.convert_text(content)

        return ConversionResult(
            source_path=file_path,
            source_format="txt",
            markdown=markdown,
        )

    def convert_text(self, text: str) -> str:
        """Analyze TXT blocks and produce Markdown."""

        blocks = BlockSplitter.split(text)
        markdown_blocks: list[str] = []

        for block in blocks:
            if BlockClassifier.is_code_block(block):
                # Preserve the detected code block as-is.
                markdown_blocks.append(block)
                continue

            markdown_blocks.append(
                self._convert_block(block)
            )

        return "\n\n".join(markdown_blocks)

    def _convert_block(self, block: str) -> str:
        """Convert explicit Setext headings within a block."""

        lines = block.split("\n")
        result: list[str] = []
        index = 0

        while index < len(lines):
            current = lines[index]
            next_line = (
                lines[index + 1].strip()
                if index + 1 < len(lines)
                else ""
            )

            if current.strip() and self.H1_UNDERLINE.fullmatch(next_line):
                result.append(
                    f"# {current.strip()}"
                )
                index += 2

            elif current.strip() and self.H2_UNDERLINE.fullmatch(next_line):
                result.append(
                    f"## {current.strip()}"
                )
                index += 2

            else:
                bullet_match = self.BULLET_PATTERN.fullmatch(current)
                numbered_match = self.NUMBERED_PATTERN.fullmatch(current)

                if bullet_match:
                    indentation, marker, content = bullet_match.groups()
                    result.append(f"{indentation}- {content}")

                elif numbered_match:
                    indentation, number, content = numbered_match.groups()
                    result.append(f"{indentation}{number}. {content}")

                else:
                    result.append(current)

                index += 1

        return "\n".join(result)
