"""Flair engine for contextual embeddings and sequence labeling.

This engine leverages Flair for NER, POS tagging, and embedding generation.
"""

from typing import List, Union


def parse(text, lowercase=False, remove_punctuation=False, remove_stopwords=False,
          lemmatize=False, tokenize=False, ner=False, pos_tag=False, **kwargs):
    """
    Parse text using Flair.

    Args:
        text (str): Input text to parse.
        lowercase (bool): Ignored; Flair handles casing.
        remove_punctuation (bool): Ignored.
        remove_stopwords (bool): Ignored.
        lemmatize (bool): Ignored.
        tokenize (bool): Return tokens list instead of joined string.
        ner (bool): Perform named entity recognition.
        pos_tag (bool): Perform POS tagging.
        **kwargs: Additional options (unused).

    Returns:
        list or str: Tokens, entities, or tagged tokens.

    Raises:
        RuntimeError: If flair is not installed.
    """
    try:
        from flair.data import Sentence
        from flair.models import SequenceTagger
    except ImportError:
        raise RuntimeError(
            "Flair library not found. "
            "Install with: pip install sparse[specialized]"
        )

    if ner:
        try:
            tagger = SequenceTagger.load('ner')
        except Exception as e:
            raise RuntimeError(f"Failed to load Flair NER model: {e}")

        sentence = Sentence(text)
        tagger.predict(sentence)
        entities = [
            {"text": ent.text, "label": ent.tag, "start": ent.start_position, "end": ent.end_position}
            for ent in sentence.get_spans('ner')
        ]
        return entities

    if pos_tag:
        try:
            tagger = SequenceTagger.load('pos')
        except Exception as e:
            raise RuntimeError(f"Failed to load Flair POS model: {e}")

        sentence = Sentence(text)
        tagger.predict(sentence)
        tagged = [(token.text, token.tag) for token in sentence]
        return tagged

    # Basic tokenization (simplified)
    sentence = Sentence(text)
    tokens = [token.text for token in sentence]

    if tokenize:
        return tokens
    else:
        return ' '.join(tokens)
