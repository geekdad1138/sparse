"""Stanza-based text processing engine.

This engine provides basic tokenization and lemmatization via the Stanza
pipeline. It is intentionally simple: the heavy NLP work is delegated to
`stanza` models which must be downloaded separately.
"""

from typing import List, Union


def parse(text, lowercase=False, remove_punctuation=False, remove_stopwords=False,
          lemmatize=False, tokenize=False, ner=False, **kwargs):
    """
    Parse text using Stanza.

    Args:
        text (str): Input text to parse.
        lowercase (bool): If True, convert tokens to lowercase after processing.
        remove_punctuation (bool): Remove tokens that are punctuation.
        remove_stopwords (bool): Remove English stop words using a simple list.
        lemmatize (bool): Use token.lemma to output lemmatized form.
        tokenize (bool): Return list of tokens, otherwise joined string.
        ner (bool): If True, return named entities extracted from the text.
        **kwargs: Additional options (unused).

    Returns:
        list or str or list[dict]: Tokens, joined text, or NER entities.

    Raises:
        RuntimeError: If stanza is not installed or English models are missing.
    """
    try:
        import stanza
    except ImportError:
        raise RuntimeError(
            "Stanza library not found. "
            "Install with: pip install sparse[advanced]"
        )

    # ensure the English model is downloaded; stanza will raise if not
    try:
        nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,ner', verbose=False)
    except Exception as e:
        raise RuntimeError(
            f"Unable to load Stanza English pipeline: {e}. "
            "You may need to install models with ``import stanza; stanza.download('en')``."
        )

    doc = nlp(text)

    if ner:
        entities = []
        for sent in doc.sentences:
            for ent in sent.ents:
                entities.append({
                    "text": ent.text,
                    "type": ent.type,
                    "start_char": ent.start_char,
                    "end_char": ent.end_char,
                })
        return entities

    tokens = []
    # simple english stop words list (could be improved later)
    STOPWORDS = {
        'the', 'a', 'an', 'in', 'on', 'and', 'or', 'is', 'are', 'was', 'were'
    }

    for sentence in doc.sentences:
        for word in sentence.words:
            token_text = word.text

            if remove_punctuation and word.upos == 'PUNCT':
                continue

            if remove_stopwords and token_text.lower() in STOPWORDS:
                continue

            if lemmatize:
                token_text = word.lemma

            if lowercase:
                token_text = token_text.lower()

            tokens.append(token_text)

    if tokenize:
        return tokens
    else:
        return ' '.join(tokens)
