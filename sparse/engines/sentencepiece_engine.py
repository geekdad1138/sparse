"""SentencePiece engine for language-neutral tokenization.

This engine uses SentencePiece for subword and character-level tokenization,
suitable for multilingual and low-resource languages.
"""

from typing import List, Union


def parse(text, lowercase=False, remove_punctuation=False, remove_stopwords=False,
          lemmatize=False, tokenize=False, model_file=None, **kwargs):
    """
    Parse text using SentencePiece.

    Args:
        text (str): Input text to parse.
        lowercase (bool): Convert to lowercase before tokenization.
        remove_punctuation (bool): Ignored; SentencePiece handles punctuation.
        remove_stopwords (bool): Ignored.
        lemmatize (bool): Ignored.
        tokenize (bool): Return tokens list instead of joined string.
        model_file (str): Path to SentencePiece model file (required).
        **kwargs: Additional options (unused).

    Returns:
        list or str: Tokens or joined text.

    Raises:
        RuntimeError: If sentencepiece is not installed or model not found.
    """
    try:
        import sentencepiece as spm
    except ImportError:
        raise RuntimeError(
            "SentencePiece library not found. "
            "Install with: pip install sparse[specialized]"
        )

    if not model_file:
        raise RuntimeError("SentencePiece requires a model_file path.")

    try:
        sp = spm.SentencePieceProcessor()
        sp.load(model_file)
    except Exception as e:
        raise RuntimeError(f"Failed to load SentencePiece model '{model_file}': {e}")

    if lowercase:
        text = text.lower()

    # Tokenize
    tokens = sp.encode_as_pieces(text)

    if tokenize:
        return tokens
    else:
        return ' '.join(tokens)
