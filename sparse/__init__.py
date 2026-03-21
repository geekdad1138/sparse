from sparse import utils

def parse(text, engine=None, lowercase=False, remove_punctuation=False, 
          remove_stopwords=False, lemmatize=False, tokenize=False,
          fix_text=False, transliterate=False, remove_emoji=False, remove_unicode=False,
          clean_html=False, extract_text=False, remove_urls=False,
          detect_language=False, language_engine='langdetect', **kwargs):
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
        fix_text (bool): Apply encoding fixes (ftfy).
        transliterate (bool): Convert Unicode to ASCII (Unidecode).
        remove_emoji (bool): Drop emoji characters.
        remove_unicode (bool): Strip non-ASCII characters.
        clean_html (bool): Clean HTML content.
        extract_text (bool): Extract text from HTML.
        remove_urls (bool): Remove URLs from text.
        detect_language (bool): If True, return detected language code.
        language_engine (str): Language detection engine ('langdetect', 'fasttext').
        **kwargs: Additional engine-specific options (e.g., pos_tag, ner, model for spacy).
    
    Returns:
        str or list: Processed text or tokens.
    """
    if engine:
        # Delegate to engine
        return _dispatch_engine(engine, text, locals())
    
    # Lightweight (default) pipeline: utils-based
    result = text

    if clean_html:
        result = utils.clean_html(result)
    if extract_text:
        result = utils.extract_text(result)
    if remove_urls:
        result = utils.remove_urls(result)

    if fix_text:
        result = utils.fix_text(result)
    if transliterate:
        result = utils.transliterate(result)
    if remove_emoji:
        result = utils.remove_emoji(result)
    if remove_unicode:
        result = utils.remove_unicode(result)

    if lowercase:
        result = utils.lowercase(result)
    if remove_punctuation:
        result = utils.remove_punctuation(result)

    if detect_language:
        return utils.detect_language(result, engine=language_engine)

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
    elif engine_name == 'spacy':
        try:
            from sparse.engines import spacy_engine
            return spacy_engine.parse(text, **engine_options)
        except ImportError:
            raise ValueError('spaCy engine not available. Install spacy: pip install spacy')
    elif engine_name == 'textblob':
        try:
            from sparse.engines import textblob_engine
            return textblob_engine.parse(text, **engine_options)
        except ImportError:
            raise ValueError('TextBlob engine not available. Install textblob: pip install textblob')
    elif engine_name == 'transformers':
        try:
            from sparse.engines import transformers_engine
            return transformers_engine.parse(text, **engine_options)
        except ImportError:
            raise ValueError(
                'Transformers engine not available. '
                'Install with: pip install sparse[advanced]'
            )
    elif engine_name == 'gensim':
        try:
            from sparse.engines import gensim_engine
            return gensim_engine.parse(text, **engine_options)
        except ImportError:
            raise ValueError(
                'Gensim engine not available. Install with: pip install sparse[advanced]'
            )
    elif engine_name == 'stanza':
        try:
            from sparse.engines import stanza_engine
            return stanza_engine.parse(text, **engine_options)
        except ImportError:
            raise ValueError(
                'Stanza engine not available. Install with: pip install sparse[advanced]'
            )
    elif engine_name == 'hf_tokenizers':
        try:
            from sparse.engines import hf_tokenizers_engine
            return hf_tokenizers_engine.parse(text, **engine_options)
        except ImportError:
            raise ValueError(
                'Hugging Face Tokenizers engine not available. '
                'Install with: pip install sparse[specialized]'
            )
    elif engine_name == 'sentencepiece':
        try:
            from sparse.engines import sentencepiece_engine
            return sentencepiece_engine.parse(text, **engine_options)
        except ImportError:
            raise ValueError(
                'SentencePiece engine not available. Install with: pip install sparse[specialized]'
            )
    elif engine_name == 'flair':
        try:
            from sparse.engines import flair_engine
            return flair_engine.parse(text, **engine_options)
        except ImportError:
            raise ValueError(
                'Flair engine not available. Install with: pip install sparse[specialized]'
            )
    elif engine_name == 'sklearn':
        try:
            from sparse.engines import sklearn_engine
            return sklearn_engine.parse(text, **engine_options)
        except ImportError:
            raise ValueError(
                'scikit-learn engine not available. Install with: pip install sparse[utils]'
            )
    elif engine_name == 'textacy':
        try:
            from sparse.engines import textacy_engine
            return textacy_engine.parse(text, **engine_options)
        except ImportError:
            raise ValueError(
                'Textacy engine not available. Install with: pip install sparse[utils]'
            )
    else:
        raise ValueError(f'Unknown engine: {engine_name}')