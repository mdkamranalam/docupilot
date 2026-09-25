import re


class TextCleaner:
    """Sanitizes raw extracted text by removing null bytes, normalizing whitespace and line breaks."""

    @staticmethod
    def clean(text: str) -> str:
        if not text:
            return ""

        # Remove null bytes
        text = text.replace("\x00", "")

        # Normalize carriage returns
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Replace excessive consecutive spaces/tabs with a single space
        text = re.sub(r"[ \t]+", " ", text)

        # Strip spaces at line beginnings/ends
        lines = [line.strip() for line in text.split("\n")]
        text = "\n".join(lines)

        # Collapse more than two consecutive newlines into two
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()
