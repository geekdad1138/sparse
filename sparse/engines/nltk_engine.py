"""NLTK-based text processing engine."""

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def parse(text, lowercase=False, remove_punctuation=False, remove_stopwords=False, 
          lemmatize=False, tokenize=False, **kwargs):
    """
    Parse text using NLTK.
    
    Args:
        text (str): Input text to parse.
        lowercase (bool): Convert to lowercase.
        remove_punctuation (bool): Remove punctuation (kept in tokenization).
        remove_stopwords (bool): Remove English stop words.
        lemmatize (bool): Apply lemmatization.
        tokenize (bool): Return tokens instead of joined string.
        **kwargs: Additional options (unused).
    
    Returns:
        str or list: Processed text or tokens.
    
    Raises:
        RuntimeError: If required NLTK data is missing.
    """
    try:
        # Ensure NLTK data is available (punkt_tab is newer NLTK versions)
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            nltk.data.find('tokenizers/punkt')
    except LookupError:
        raise RuntimeError(
            "NLTK punkt tokenizer not found. "
            "Run: python -m nltk.downloader punkt_tab"
        )
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Apply lowercase early if requested
    if lowercase:
        tokens = [t.lower() for t in tokens]
    
    # Remove punctuation if requested
    if remove_punctuation:
        # Keep only alphanumeric and spaces
        tokens = [t for t in tokens if t.isalnum() or t.isspace()]
    
    # Remove stop words
    if remove_stopwords:
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            raise RuntimeError(
                "NLTK stopwords corpus not found. "
                "Run: python -m nltk.downloader stopwords"
            )
        stop = set(stopwords.words('english'))
        tokens = [t for t in tokens if t.lower() not in stop]
    
    # Apply lemmatization
    if lemmatize:
        try:
            lem = WordNetLemmatizer()
            tokens = [lem.lemmatize(t) for t in tokens]
        except LookupError:
            raise RuntimeError(
                "NLTK wordnet corpus not found. "
                "Run: python -m nltk.downloader wordnet omw-1.4"
            )
    
    # Return tokens or joined string
    if tokenize:
        return tokens
    else:
        return ' '.join(tokens)
