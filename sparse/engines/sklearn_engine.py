"""Scikit-learn feature extraction engine."""

from typing import Union, List


def parse(text, lowercase=False, remove_punctuation=False, remove_stopwords=False, lemmatize=False, tokenize=False,
          vectorizer="count", **kwargs):
    """Parse text into scikit-learn feature vectors.

    Args:
        text (str): Input text.
        lowercase (bool): Lowercase the text before vectorizing.
        remove_punctuation (bool): Remove punctuation before vectorizing.
        tokenize (bool): If True, return list of token strings instead of vectors.
        vectorizer (str): "count" or "tfidf".
        **kwargs: Additional options passed to vectorizer.

    Returns:
        list or object: Token list (if tokenize=True) or vectorizer output.

    Raises:
        RuntimeError: If scikit-learn is not installed.
    """
    try:
        from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
    except ImportError:
        raise RuntimeError(
            "scikit-learn not installed. Install with: pip install sparse[utils]"
        )

    processed = text
    if lowercase:
        processed = processed.lower()
    if remove_punctuation:
        import re

        processed = re.sub(r"[^\w\s]", "", processed)

    if tokenize:
        return processed.split()

    if vectorizer == "count":
        vec = CountVectorizer(**kwargs)
    elif vectorizer == "tfidf":
        vec = TfidfVectorizer(**kwargs)
    else:
        raise ValueError(f"Unknown vectorizer: {vectorizer}")

    return vec.fit_transform([processed])
