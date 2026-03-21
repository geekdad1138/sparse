# Regex-based cleaning utilities

import re

# Optional helpers; imported lazily to avoid hard dependencies.


def fix_text(text):
    from sparse.utils.normalization import fix_text as _fix_text

    return _fix_text(text)


def transliterate(text):
    from sparse.utils.normalization import transliterate as _transliterate

    return _transliterate(text)


def remove_emoji(text):
    from sparse.utils.normalization import remove_emoji as _remove_emoji

    return _remove_emoji(text)


def remove_unicode(text):
    from sparse.utils.normalization import remove_unicode as _remove_unicode

    return _remove_unicode(text)


def detect_language(text, engine="langdetect"):
    from sparse.utils.language_detection import detect_language as _detect_language

    return _detect_language(text, engine=engine)


def clean_html(text):
    from sparse.utils.html_cleaning import clean_html as _clean_html

    return _clean_html(text)


def extract_text(text):
    from sparse.utils.html_cleaning import extract_text as _extract_text

    return _extract_text(text)


def remove_urls(text):
    from sparse.utils.html_cleaning import remove_urls as _remove_urls

    return _remove_urls(text)


def remove_punctuation(text):
    """Remove punctuation from text."""
    return re.sub(r"[^\w\s]", "", text)


def lowercase(text):
    """Convert text to lowercase."""
    return text.lower()
