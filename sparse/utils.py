# Regex-based cleaning utilities

import re

def remove_punctuation(text):
    """Remove punctuation from text."""
    return re.sub(r'[^\w\s]', '', text)

def lowercase(text):
    """Convert text to lowercase."""
    return text.lower()

# TODO: Add more utility functions