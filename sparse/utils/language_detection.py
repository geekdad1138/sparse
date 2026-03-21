"""Language detection helpers."""


def detect_language(text: str, engine: str = "langdetect") -> str:
    """Detect the language of the given text.

    Args:
        text: Input text.
        engine: Detection backend (`langdetect` or `fasttext`).

    Returns:
        Language code (e.g., 'en').

    Raises:
        RuntimeError: If the selected engine is not installed.
    """
    if engine == "langdetect":
        try:
            from langdetect import detect

            return detect(text)
        except ImportError:
            raise RuntimeError(
                "langdetect not installed. Install with: pip install sparse[utils]"
            )
    elif engine == "fasttext":
        try:
            import fasttext
        except ImportError:
            raise RuntimeError(
                "fasttext not installed. Install with: pip install sparse[utils]"
            )
        # fasttext requires a model; user must provide or manage externally.
        raise RuntimeError("fasttext engine not implemented in this helper yet.")
    else:
        raise ValueError(f"Unknown language detection engine: {engine}")
