"""Hugging Face Transformers–based text processing engine.

This engine provides minimal tokenization and token ID support via the
`transformers` library. It is intentionally lightweight; advanced features
(such as model inference or pipelines) can be added later when the
phase‑2 implementation expands.
"""

from typing import List, Union


def parse(text, lowercase=False, remove_punctuation=False, remove_stopwords=False,
          lemmatize=False, tokenize=False, return_ids=False,
          model_name='bert-base-uncased', **kwargs):
    """
    Parse text using a Hugging Face tokenizer.

    The current implementation focuses on subword tokenization and
    optional ID conversion. Additional features (attention masks, classification,
    etc.) may be added in future updates.

    Args:
        text (str): Input text to parse.
        lowercase (bool): Ignored; tokenizer handles casing based on model.
        remove_punctuation (bool): Ignored; tokenizer handles punctuation.
        remove_stopwords (bool): Ignored.
        lemmatize (bool): Ignored.
        tokenize (bool): If True, return token list; otherwise, return joined
            string of tokens.
        return_ids (bool): If True, return integer token ids (requires
            `tokenize=True`).
        model_name (str): Name of the pretrained tokenizer to load.
        **kwargs: Additional options (unused).

    Returns:
        list or str or list[int]: Tokenized output or text or IDs.

    Raises:
        RuntimeError: If transformers is not installed or model cannot be loaded.
    """
    try:
        from transformers import AutoTokenizer
    except ImportError:
        raise RuntimeError(
            "Transformers library not found. "
            "Install with: pip install sparse[advanced]"
        )

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
    except Exception as e:
        raise RuntimeError(
            f"Unable to load tokenizer '{model_name}': {e}."
            " Make sure the model name is correct and you have internet access."
        )

    # Tokenize the input text
    tokens = tokenizer.tokenize(text)

    # The tokenizer already lowercases/normalizes based on its config, so we
    # don't manually apply lowercase/remove_punctuation/remove_stopwords/lemmatize.

    if return_ids:
        if not tokenize:
            # we need tokens first
            tokens = tokenizer.tokenize(text)
        ids = tokenizer.convert_tokens_to_ids(tokens)
        return ids

    if tokenize:
        return tokens
    else:
        # join tokens with spaces, mimic other engines
        return ' '.join(tokens)
