# Sparse 🧠

**The "Smart" Parse Function for Python.**

[![PyPI version](https://badge.fury.io/py/sparse.svg)](https://pypi.org/project/sparse/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-34%20passed-brightgreen.svg)](https://github.com/yourusername/sparse/actions)

`sparse` is a unified text preprocessing library that abstracts multiple NLP engines behind a single `parse()` function. It bridges raw text to clean data with optional lightweight defaults (no dependencies) or powerful engine-based processing.

**Core philosophy:** Unified interface, pluggable engines, zero-to-hero on install.

---

## 🚀 Quick Start

```python
from sparse import parse

# Simple cleaning (no dependencies)
text = "Hello, World! 🌍"
clean = parse(text, lowercase=True, remove_punctuation=True, remove_emoji=True)
# "hello world"

# Advanced NLP with spaCy
tokens = parse("The cats are running", engine="spacy", lemmatize=True, remove_stopwords=True, tokenize=True)
# ['cat', 'run']

# Sentiment analysis with TextBlob
sentiment = parse("I love this!", engine="textblob", sentiment=True)
# {'polarity': 0.85, 'subjectivity': 0.95}

# Keyterm extraction with Textacy
keyterms = parse("Machine learning is fascinating.", engine="textacy", keyterms=True)
# [('machine learning', 0.85), ('fascinating', 0.72)]

# Language detection
lang = parse("Bonjour le monde", detect_language=True)
# 'fr'
```

## 📦 Installation

`sparse` uses optional dependency groups - install only what you need:

```bash
# Minimal install (lightweight utilities only)
pip install sparse

# Core engines (recommended for most users)
pip install sparse[core]              # NLTK, spaCy, TextBlob (~500MB)

# Advanced engines (powerful, heavy)
pip install sparse[advanced]          # Transformers, Gensim, Stanza (~2-3GB)

# Specialized engines (niche use cases)
pip install sparse[specialized]       # HF Tokenizers, SentencePiece, Flair (~1GB)

# Text utilities (cleaning, detection)
pip install sparse[utils]             # Normalization, HTML cleaning, sklearn (~100MB)

# Everything (for NLP research)
pip install sparse[all]               # All engines and utilities (~3.5GB)

# Development (testing, linting)
pip install sparse[dev]
```

## ✨ Features

### Core API
- **Unified Interface:** One `parse()` function for all text processing
- **Flexible Options:** Mix and match preprocessing steps
- **Engine Agnostic:** Same options work across all engines
- **Smart Defaults:** Lightweight processing when no engine specified

### Implemented Engines

| Engine | Status | Key Features | Install Group |
|--------|--------|--------------|---------------|
| **Default** | ✅ Complete | lowercase, punctuation removal, emoji/unicode handling | `sparse` |
| **NLTK** | ✅ Complete | tokenization, lemmatization, stop words | `[core]` |
| **spaCy** | ✅ Complete | POS tagging, NER, dependency parsing | `[core]` |
| **TextBlob** | ✅ Complete | sentiment analysis, noun phrases | `[core]` |
| **Transformers** | ✅ Complete | BERT tokenization, text classification | `[advanced]` |
| **Gensim** | ✅ Complete | word embeddings, topic modeling | `[advanced]` |
| **Stanza** | ✅ Complete | multilingual NLP, universal dependencies | `[advanced]` |
| **HF Tokenizers** | ✅ Complete | fast subword tokenization | `[specialized]` |
| **SentencePiece** | ✅ Complete | language-neutral tokenization | `[specialized]` |
| **Flair** | ✅ Complete | contextual embeddings, sequence labeling | `[specialized]` |
| **scikit-learn** | ✅ Complete | Count/TF-IDF vectorization | `[utils]` |
| **Textacy** | ✅ Complete | keyterm extraction, readability analysis | `[utils]` |

### Utility Functions
- **Text Normalization:** ftfy encoding fixes, Unidecode transliteration, emoji removal
- **Language Detection:** langdetect and fasttext support
- **HTML Cleaning:** BeautifulSoup parsing, bleach sanitization, URL removal
- **Feature Extraction:** sklearn vectorizers for ML pipelines

## 🎯 Usage Examples

### Basic Preprocessing
```python
from sparse import parse

text = "Hello, World! This is a TEST with some Punctuation... and EMOJIS 😊🌟"

# Multiple cleaning steps
clean = parse(text,
              lowercase=True,
              remove_punctuation=True,
              remove_emoji=True,
              fix_text=True)  # Fix encoding issues
# "hello world this is a test with some punctuation and"

# HTML cleaning
html = "<p>Hello <b>world</b>! <a href='http://example.com'>Link</a></p>"
clean_html = parse(html, clean_html=True, extract_text=True, remove_urls=True)
# "Hello world! Link"
```

### Engine-Specific Features
```python
# spaCy: Named Entity Recognition
entities = parse("Apple Inc. is based in Cupertino, California.",
                 engine="spacy", ner=True)
# [{'text': 'Apple Inc.', 'label': 'ORG', 'start': 0, 'end': 9}, ...]

# TextBlob: Sentiment Analysis
sentiment = parse("This product is amazing!",
                  engine="textblob", sentiment=True)
# {'polarity': 0.75, 'subjectivity': 0.95}

# TextBlob: Noun Phrase Extraction
phrases = parse("The quick brown fox jumps over the lazy dog.",
                engine="textblob", noun_phrases=True)
# ['quick brown fox', 'lazy dog']

# Transformers: Tokenization with BERT
tokens = parse("Hello world", engine="transformers", tokenize=True)
# ['[CLS]', 'hello', 'world', '[SEP]']

# Gensim: Document vectorization
vector = parse("Machine learning is awesome",
               engine="gensim", vectorize=True)
# <gensim.models.keyedvectors.KeyedVectors object>

# Textacy: Readability Statistics
stats = parse("This is a complex sentence with advanced vocabulary and sophisticated structure.",
              engine="textacy", readability=True)
# {'flesch_kincaid_grade_level': 12.3, 'automated_readability_index': 14.2, ...}

# scikit-learn: Feature vectors
from scipy.sparse import csr_matrix
vectors = parse(["Hello world", "Machine learning"],
                engine="sklearn", vectorizer="tfidf")
# <2x1000 sparse matrix of type '<class 'numpy.float64'>'>
```

### Advanced Pipelines
```python
# Combine utilities with engines
text = "<html><body>HELLO WORLD! 🌍 <a href='spam.com'>Click here</a></body></html>"

# Full pipeline: HTML → clean → detect language → tokenize
result = parse(text,
               clean_html=True,
               extract_text=True,
               remove_urls=True,
               lowercase=True,
               remove_punctuation=True,
               remove_emoji=True,
               detect_language=True)
# 'en' (detected language)

# Or get processed text
processed = parse(text,
                  clean_html=True,
                  extract_text=True,
                  remove_urls=True,
                  lowercase=True,
                  remove_punctuation=True,
                  remove_emoji=True)
# "hello world click here"
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v
# 34 passed, 35 skipped (optional dependencies)

# Test specific engine
pytest tests/test_engines_spacy.py -v

# Test core functionality
pytest tests/test_sparse.py -v
```

## 📂 Project Structure

```
sparse/
├── sparse/
│   ├── __init__.py              # Main parse() function & engine dispatcher
│   ├── utils/                   # Utility modules
│   │   ├── __init__.py          # Core utilities
│   │   ├── normalization.py     # Text normalization (ftfy, emoji, etc.)
│   │   ├── language_detection.py # Language detection
│   │   └── html_cleaning.py     # HTML parsing & cleaning
│   └── engines/                 # Engine implementations
│       ├── nltk_engine.py
│       ├── spacy_engine.py
│       ├── textblob_engine.py
│       ├── transformers_engine.py
│       ├── gensim_engine.py
│       ├── stanza_engine.py
│       ├── hf_tokenizers_engine.py
│       ├── sentencepiece_engine.py
│       ├── flair_engine.py
│       ├── sklearn_engine.py
│       └── textacy_engine.py
├── tests/
│   ├── test_sparse.py           # Core API tests
│   ├── test_utils.py            # Utility tests
│   ├── test_engines_*.py        # Engine-specific tests
│   └── __pycache__/
├── docs/spec/
│   ├── Engine-Implementation-Roadmap.md
│   └── *.md                     # Engine specifications
├── pyproject.toml               # Dependencies & build config
├── requirements.txt             # Development dependencies
├── LICENSE
├── README.md
└── sparse.code-workspace        # VS Code workspace
```

## 🤝 Contributing

We welcome contributions! This project follows a modular architecture that makes adding new engines easy.

### Adding a New Engine
1. Create `sparse/engines/{name}_engine.py` with a `parse(text, **options)` function
2. Add engine to dispatcher in `sparse/__init__.py`
3. Add dependencies to `pyproject.toml` extras
4. Create `tests/test_engines_{name}.py`
5. Update documentation

See [Engine Implementation Roadmap](docs/spec/Engine-Implementation-Roadmap.md) for detailed guidelines.

### Development Setup
```bash
git clone https://github.com/yourusername/sparse
cd sparse
pip install -e .[dev]
pytest tests/
```

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built on the shoulders of giants: NLTK, spaCy, Hugging Face Transformers, and the broader NLP community.

---

**Ready to parse smarter, not harder?** Give `sparse` a try and let us know what you think!

Check the [Engine Implementation Roadmap](docs/spec/Engine-Implementation-Roadmap.md) for development priorities.

## ⚖️ License

This project is licensed under the MIT License - see the LICENSE file for details.
