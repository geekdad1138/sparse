"""HTML cleaning and extraction utilities."""

import re


def clean_html(text: str) -> str:
    """Clean HTML content to plain text using BeautifulSoup + bleach."""
    try:
        from bs4 import BeautifulSoup
        import bleach
    except ImportError:
        raise RuntimeError(
            "beautifulsoup4/bleach not installed. Install with: pip install sparse[utils]"
        )

    # Strip scripts/styles
    soup = BeautifulSoup(text, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()

    cleaned = soup.get_text(separator=" ")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    # Sanitize remaining content
    return bleach.clean(cleaned, tags=[], strip=True)


def extract_text(html: str) -> str:
    """Extract text content from HTML."""
    return clean_html(html)


def remove_urls(text: str) -> str:
    """Remove URLs from text."""
    return re.sub(r"https?://\S+|www\.\S+", "", text)
