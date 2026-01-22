"""spaCy-based text processing engine."""

import spacy
from typing import List, Union


def parse(text, lowercase=False, remove_punctuation=False, remove_stopwords=False,
          lemmatize=False, tokenize=False, pos_tag=False, ner=False, 
          model='en_core_web_sm', **kwargs):
    """
    Parse text using spaCy.
    
    Args:
        text (str): Input text to parse.
        lowercase (bool): Convert to lowercase.
        remove_punctuation (bool): Remove punctuation tokens.
        remove_stopwords (bool): Remove stop words.
        lemmatize (bool): Apply lemmatization.
        tokenize (bool): Return tokens instead of joined string.
        pos_tag (bool): Include POS tags in output (for tokenize=True).
        ner (bool): Perform named entity recognition.
        model (str): spaCy model to load (default: 'en_core_web_sm').
        **kwargs: Additional options (unused).
    
    Returns:
        str or list: Processed text, token list, or NER results depending on options.
    
    Raises:
        RuntimeError: If spaCy model is not installed.
    """
    try:
        nlp = spacy.load(model)
    except OSError:
        raise RuntimeError(
            f"spaCy model '{model}' not found. "
            f"Download with: python -m spacy download {model}"
        )
    
    # Process text through spaCy pipeline
    doc = nlp(text)
    
    # Handle NER separately if requested
    if ner:
        entities = [
            {"text": ent.text, "label": ent.label_, "start": ent.start_char, "end": ent.end_char}
            for ent in doc.ents
        ]
        return entities
    
    # Process tokens
    tokens = []
    for token in doc:
        # Skip punctuation if requested
        if remove_punctuation and token.is_punct:
            continue
        
        # Skip stop words if requested
        if remove_stopwords and token.is_stop:
            continue
        
        # Get token text (lemmatized or original)
        if lemmatize:
            token_text = token.lemma_
        else:
            token_text = token.text
        
        # Apply lowercase if requested
        if lowercase:
            token_text = token_text.lower()
        
        # Append token with optional POS tag
        if pos_tag and tokenize:
            tokens.append((token_text, token.pos_))
        else:
            tokens.append(token_text)
    
    # Return format
    if tokenize:
        return tokens
    else:
        return ' '.join([t[0] if isinstance(t, tuple) else t for t in tokens])
