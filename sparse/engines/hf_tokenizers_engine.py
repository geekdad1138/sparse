"""Hugging Face Tokenizers engine for fast subword tokenization.

This engine uses the `tokenizers` library for high-performance tokenization,
focusing on subword models like BPE, WordPiece, and Unigram.
"""

from typing import List, Union


def parse(text, lowercase=False, remove_punctuation=False, remove_stopwords=False,
          lemmatize=False, tokenize=False, return_ids=False, model_name='bert-base-uncased',
          **kwargs):
    """
    Parse text using Hugging Face tokenizers.

    Args:
        text (str): Input text to parse.
        lowercase (bool): Ignored; tokenizer handles casing.
        remove_punctuation (bool): Ignored; tokenizer handles punctuation.
        remove_stopwords (bool): Ignored.
        lemmatize (bool): Ignored.
        tokenize (bool): Return tokens list instead of joined string.
        return_ids (bool): Return token IDs instead of strings.
        model_name (str): Pretrained tokenizer name (e.g., 'bert-base-uncased').
        **kwargs: Additional options (unused).

    Returns:
        list or str: Tokens or joined text.

    Raises:
        RuntimeError: If tokenizers library is not installed.
    """
    try:
        from tokenizers import Tokenizer
        from tokenizers.models import BPE, WordPiece, Unigram
        from tokenizers.pre_tokenizers import Whitespace
        from tokenizers.decoders import ByteLevel as ByteLevelDecoder
        from tokenizers.normalizers import NFD, StripAccents
        from tokenizers.trainers import BpeTrainer, WordPieceTrainer, UnigramTrainer
    except ImportError:
        raise RuntimeError(
            "Tokenizers library not found. "
            "Install with: pip install sparse[specialized]"
        )

    try:
        # For simplicity, use a basic tokenizer; in practice, load from pretrained
        tokenizer = Tokenizer.from_pretrained(model_name)
    except Exception as e:
        raise RuntimeError(
            f"Unable to load tokenizer '{model_name}': {e}. "
            "Ensure the model name is valid."
        )

    # Encode the text
    encoding = tokenizer.encode(text)

    if return_ids:
        return encoding.ids

    tokens = encoding.tokens

    if tokenize:
        return tokens
    else:
        return ' '.join(tokens)
