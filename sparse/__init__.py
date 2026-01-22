from sparse import utils

def parse(text, engine=None, lowercase=False, remove_punctuation=False, 
          remove_stopwords=False, lemmatize=False, tokenize=False, **kwargs):
    """
    Parse and preprocess text with optional engine support.
    
    Args:
        text (str): The raw text to parse.
        engine (str, optional): Engine to use ('nltk', 'spacy', etc.). None = lightweight.
        lowercase (bool): Convert to lowercase.
        remove_punctuation (bool): Remove punctuation.
        remove_stopwords (bool): Remove stop words (engine-dependent).
        lemmatize (bool): Apply lemmatization (engine-dependent).
        tokenize (bool): Return tokens instead of joined string (engine-dependent).
        **kwargs: Additional engine-specific options.
    
    Returns:
        str or list: Processed text or tokens.
    """
    if engine:
        # Delegate to engine
        return _dispatch_engine(engine, text, locals())
    
    # Lightweight (default) pipeline: utils-based
    result = text
    if lowercase:
        result = utils.lowercase(result)
    if remove_punctuation:
        result = utils.remove_punctuation(result)
    
    return result


def _dispatch_engine(engine_name, text, options):
    """
    Dispatch to the appropriate engine module.
    
    Args:
        engine_name (str): Name of the engine (e.g., 'nltk', 'spacy').
        text (str): Input text.
        options (dict): Parsed options dict (includes all kwargs).
    
    Returns:
        str or list: Engine's parse result.
    
    Raises:
        ValueError: If engine is unknown or not installed.
    """
    # Clean up options dict
    engine_options = {
        'lowercase': options.get('lowercase', False),
        'remove_punctuation': options.get('remove_punctuation', False),
        'remove_stopwords': options.get('remove_stopwords', False),
        'lemmatize': options.get('lemmatize', False),
        'tokenize': options.get('tokenize', False),
    }
    # Include any extra kwargs the user passed
    extra_kwargs = {k: v for k, v in options.get('kwargs', {}).items()}
    engine_options.update(extra_kwargs)
    
    if engine_name == 'nltk':
        try:
            from sparse.engines import nltk_engine
            return nltk_engine.parse(text, **engine_options)
        except ImportError:
            raise ValueError('NLTK engine not available. Install nltk: pip install nltk')
    else:
        raise ValueError(f'Unknown engine: {engine_name}')