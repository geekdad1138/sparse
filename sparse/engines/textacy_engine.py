"""Textacy engine for higher-level text processing."""

from typing import Union, List, Dict


def parse(text: str, lowercase: bool = False, remove_punctuation: bool = False,
          remove_stopwords: bool = False, lemmatize: bool = False, tokenize: bool = False,
          keyterms: bool = False, readability: bool = False, **kwargs) -> Union[str, List[str], List[tuple], Dict]:
    """Parse text using textacy for advanced NLP processing.

    Args:
        text (str): Input text.
        lowercase (bool): Convert to lowercase.
        remove_punctuation (bool): Remove punctuation.
        remove_stopwords (bool): Remove stop words.
        lemmatize (bool): Apply lemmatization.
        tokenize (bool): Return list of tokens instead of joined string.
        keyterms (bool): Extract key terms using TextRank.
        readability (bool): Compute readability statistics.
        **kwargs: Additional options (e.g., lang for language).

    Returns:
        str or list or dict: Processed text, tokens, keyterms, or readability stats.

    Raises:
        RuntimeError: If textacy or spaCy is not installed.
    """
    try:
        import textacy
        import spacy
    except ImportError:
        raise RuntimeError(
            "textacy and spacy not installed. Install with: pip install sparse[utils]"
        )

    lang = kwargs.get('lang', 'en')
    model_name = f"{lang}_core_web_sm"

    try:
        nlp = spacy.load(model_name)
    except OSError:
        raise RuntimeError(
            f"spaCy model '{model_name}' not found. "
            f"Download with: python -m spacy download {model_name}"
        )

    doc = nlp(text)

    # Special features
    if keyterms:
        return list(textacy.extract.keyterms.textrank(doc, topn=10))

    if readability:
        return textacy.text_stats.readability(doc)

    # Standard preprocessing pipeline
    processed = text

    if lowercase:
        processed = processed.lower()

    if remove_punctuation:
        processed = textacy.preprocessing.remove_punct(processed)

    if remove_stopwords:
        processed = textacy.preprocessing.remove_stopwords(processed, lang=lang)

    if lemmatize:
        processed = textacy.preprocessing.lemmatize(processed, model=model_name)

    if tokenize:
        # Extract words as tokens
        tokens = list(textacy.extract.words(
            doc,
            filter_stops=remove_stopwords,
            filter_punct=remove_punctuation,
            filter_nums=True
        ))
        return tokens

    return processed