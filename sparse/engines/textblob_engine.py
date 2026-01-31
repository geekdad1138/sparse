"""TextBlob-based text processing engine."""

from textblob import TextBlob
from typing import Union, List, Dict


def parse(text, lowercase=False, remove_punctuation=False, remove_stopwords=False,
          lemmatize=False, tokenize=False, sentiment=False, noun_phrases=False,
          **kwargs):
    """
    Parse text using TextBlob.
    
    Args:
        text (str): Input text to parse.
        lowercase (bool): Convert to lowercase.
        remove_punctuation (bool): Remove punctuation tokens.
        remove_stopwords (bool): Remove stop words (via NLTK).
        lemmatize (bool): Apply lemmatization (via NLTK WordNetLemmatizer).
        tokenize (bool): Return tokens instead of joined string.
        sentiment (bool): Return sentiment analysis (polarity, subjectivity).
        noun_phrases (bool): Extract noun phrases.
        **kwargs: Additional options (unused).
    
    Returns:
        str or list or dict: Processed text, tokens, sentiment, or structured data.
    
    Raises:
        RuntimeError: If required NLTK data is missing.
    """
    try:
        blob = TextBlob(text)
    except Exception as e:
        raise RuntimeError(f"Error parsing text with TextBlob: {str(e)}")
    
    # Handle sentiment analysis
    if sentiment:
        return {
            "polarity": blob.sentiment.polarity,      # -1 to 1 (negative to positive)
            "subjectivity": blob.sentiment.subjectivity  # 0 to 1 (objective to subjective)
        }
    
    # Handle noun phrases extraction
    if noun_phrases:
        return list(blob.noun_phrases)
    
    # Process tokens
    tokens = []
    for word in blob.words:
        token_text = word
        
        # Apply lowercase if requested
        if lowercase:
            token_text = token_text.lower()
        
        # Skip punctuation if requested
        if remove_punctuation and not token_text.isalnum():
            continue
        
        # Skip stop words if requested
        if remove_stopwords:
            try:
                from nltk.corpus import stopwords
                stop = set(stopwords.words('english'))
                if token_text.lower() in stop:
                    continue
            except LookupError:
                raise RuntimeError(
                    "NLTK stopwords corpus not found. "
                    "Run: python -m nltk.downloader stopwords"
                )
        
        # Apply lemmatization if requested
        if lemmatize:
            try:
                blob_word = TextBlob(token_text)
                # TextBlob lemmatization is basic; use NLTK's lemmatizer for better results
                from nltk.stem import WordNetLemmatizer
                lem = WordNetLemmatizer()
                token_text = lem.lemmatize(token_text)
            except Exception:
                # If lemmatization fails, keep original token
                pass
        
        tokens.append(token_text)
    
    # Return format
    if tokenize:
        return tokens
    else:
        return ' '.join(tokens)
