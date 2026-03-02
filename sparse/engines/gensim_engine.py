"""Gensim-based text processing engine.

This engine leverages `gensim` utilities for lightweight preprocessing and
also optionally uses NLTK for lemmatization when requested. It is intended
as a starting point for Phase 2 functionality (embeddings, topic modeling,
etc.).
"""

from typing import List, Union


def parse(text, lowercase=False, remove_punctuation=False, remove_stopwords=False,
          lemmatize=False, tokenize=False, **kwargs):
    """
    Parse text using gensim preprocessing utilities.

    Args:
        text (str): Input text to parse.
        lowercase (bool): Whether to lowercase tokens (gensim does this by default).
        remove_punctuation (bool): Whether to strip punctuation (handled by gensim).
        remove_stopwords (bool): Remove gensim's built-in stop words.
        lemmatize (bool): Apply NLTK WordNet lemmatizer to tokens.
        tokenize (bool): Return tokens list instead of joined string.
        **kwargs: Additional options (unused).

    Returns:
        list or str: Processed tokens or joined string.

    Raises:
        RuntimeError: If gensim is not installed or required NLTK data is missing.
    """
    try:
        from gensim.utils import simple_preprocess
        from gensim.parsing.preprocessing import STOPWORDS as GENSIM_STOPWORDS
    except ImportError:
        raise RuntimeError(
            "Gensim library not found. "
            "Install with: pip install sparse[advanced]"
        )

    # simple_preprocess lowercases and removes punctuation by default
    # ``deacc=True`` strips accent marks.
    tokens = simple_preprocess(text, deacc=True)

    if remove_stopwords:
        tokens = [t for t in tokens if t not in GENSIM_STOPWORDS]

    if lemmatize:
        try:
            from nltk.stem import WordNetLemmatizer
            lem = WordNetLemmatizer()
            tokens = [lem.lemmatize(t) for t in tokens]
        except LookupError:
            raise RuntimeError(
                "NLTK wordnet corpus not found. "
                "Run: python -m nltk.downloader wordnet omw-1.4"
            )

    if tokenize:
        return tokens
    else:
        return ' '.join(tokens)
