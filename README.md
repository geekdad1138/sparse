# Sparse 🧠

**The "Smart" Parse Function for Python.**

`sparse` is a lightweight, extensible library designed to bridge the gap between raw text and clean data. Instead of writing repetitive boilerplate for every NLP project, `sparse` provides a unified interface to clean, tokenize, and normalize text using the industry's best engines.

---

## 🚀 The Vision
Preprocessing text is often the most tedious part of NLP. You find yourself importing `re`, `string`, `nltk`, and `spacy` just to get a sentence ready for a model. 

**Sparse** simplifies this into a single, intuitive function call. It acts as a wrapper that lets you toggle features like lemmatization, stop-word removal, and casing without worrying about the underlying library's specific syntax.

## 🛠️ Current Status & Usage

The core API is now implemented and tested! Here's how to use `sparse`:

```python
from sparse import parse

# 1. Simple, fast cleaning (no dependencies required)
text = "The quick brown fox, jumps over the lazy dog!"
clean = parse(text, lowercase=True, remove_punctuation=True)
# Output: "the quick brown fox jumps over the lazy dog"

# 2. Advanced NLP with engines
tokens = parse(text, engine="spacy", remove_stopwords=True, lemmatize=True, tokenize=True)
# Output: ['quick', 'brown', 'fox', 'jump', 'lazy', 'dog']

# 3. Named Entity Recognition (spaCy)
entities = parse("Apple is in Cupertino", engine="spacy", ner=True)
# Output: [{'text': 'Apple', 'label': 'ORG', ...}, ...]
```

## Installation

```bash
# Minimal (no engines)
pip install sparse

# Recommended (NLTK + spaCy + TextBlob)
pip install sparse[core]

# All engines and utilities
pip install sparse[all]
```

## ✨ Features

* [x] **Unified API:** One function (`parse`) to rule them all
* [x] **Lightweight Default:** No external dependencies required
* [x] **NLTK Engine:** Tokenization, lemmatization, stop-word removal
* [x] **spaCy Engine:** Fast NLP, POS tagging, Named Entity Recognition
* [ ] **TextBlob Engine:** Coming soon
* [ ] **Utilities:** Text cleaning, language detection, HTML parsing

## Supported Engines

| Engine | Install | Features |
|--------|---------|----------|
| Default | `pip install sparse` | lowercase, remove_punctuation |
| NLTK | `pip install sparse[core]` | tokenize, lemmatize, remove_stopwords |
| spaCy | `pip install sparse[core]` | tokenize, lemmatize, remove_stopwords, POS, NER |

See [Engine Implementation Roadmap](docs/spec/Engine-Implementation-Roadmap.md) for planned engines.

## 📂 Project Structure

```text
sparse/
├── sparse/
│   ├── __init__.py           # Main parse() function & dispatcher
│   ├── utils.py              # Lightweight regex utilities
│   └── engines/              # Engine adapters
│       ├── nltk_engine.py
│       └── spacy_engine.py
├── tests/
│   ├── test_sparse.py        # Core & utility tests
│   └── test_engines_spacy.py # spaCy-specific tests
├── docs/spec/
│   └── Engine-Implementation-Roadmap.md
├── pyproject.toml            # Dependencies & extras groups
├── requirements.txt          # Development requirements
└── README.md
```

## Testing

```bash
pytest tests/ -v
# 21 tests passing (core, utilities, NLTK, spaCy)
```

## 🤝 Contributing

This project is in active development! Contributions are welcome:

- **Engine implementations:** See [roadmap](docs/spec/Engine-Implementation-Roadmap.md) for next engines to build
- **Bug reports & features:** Open an issue
- **Documentation:** PRs with examples and clarifications welcome

Check the [Engine Implementation Roadmap](docs/spec/Engine-Implementation-Roadmap.md) for development priorities.

## ⚖️ License

This project is licensed under the MIT License - see the LICENSE file for details.
