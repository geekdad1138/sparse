"""Text normalization helpers.

These functions are optional and rely on third-party libraries when available.
"""


def fix_text(text: str) -> str:
    """Fix mojibake/encoding issues using ftfy."""
    try:
        import ftfy

        return ftfy.fix_text(text)
    except ImportError:
        raise RuntimeError(
            "ftfy not installed. Install with: pip install sparse[utils]"
        )


def transliterate(text: str) -> str:
    """Convert Unicode text to ASCII using Unidecode."""
    try:
        import Unidecode

        return Unidecode.unidecode(text)
    except ImportError:
        raise RuntimeError(
            "Unidecode not installed. Install with: pip install sparse[utils]"
        )


def remove_emoji(text: str) -> str:
    """Remove emoji characters from text."""
    try:
        import emoji

        return emoji.replace_emoji(text, replace="")
    except ImportError:
        raise RuntimeError(
            "emoji not installed. Install with: pip install sparse[utils]"
        )


def remove_unicode(text: str) -> str:
    """Strip non-ASCII characters."""
    return text.encode("ascii", errors="ignore").decode("ascii")
