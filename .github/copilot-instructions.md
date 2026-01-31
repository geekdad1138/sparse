# Copilot Instructions for `sparse`

## Project Overview

**sparse** is a unified text preprocessing library that abstracts multiple NLP engines (NLTK, spaCy, TextBlob) behind a single `parse()` function. It bridges raw text to clean data with optional lightweight defaults (no dependencies) or powerful engine-based processing.

Core philosophy: **unified interface, pluggable engines, zero-to-hero on install**.

---

## Architecture & Component Structure

### 1. **The Central API** ([sparse/__init__.py](sparse/__init__.py))
- Single entry point: `parse(text, engine=None, lowercase=False, remove_punctuation=False, ...)`
- Dispatcher pattern: lightweight pipeline for defaults, delegates to engines for advanced features
- **Key pattern:** Options dict flows through: `parse()` → `_dispatch_engine()` → `engine.parse()`
- All engines implement identical `parse(text, **kwargs)` signature for consistency

### 2. **Engine Architecture** ([sparse/engines/](sparse/engines/))
Each engine (NLTK, spaCy, TextBlob) follows this contract:
- **Module location:** `sparse/engines/{name}_engine.py`
- **Export:** Single `parse(text, **options)` function
- **Standard options:** lowercase, remove_punctuation, remove_stopwords, lemmatize, tokenize
- **Engine-specific options:** pos_tag/ner (spaCy), sentiment/noun_phrases (TextBlob)
- **Return types:** str (joined tokens) or list (tokenized) based on `tokenize=True`
- **Error handling:** Raise `RuntimeError` with clear install instructions for missing data

Example ([sparse/engines/nltk_engine.py](sparse/engines/nltk_engine.py)):
```python
def parse(text, lowercase=False, remove_punctuation=False, ...):
    tokens = word_tokenize(text)
    # Apply filters: lowercase → remove_punctuation → remove_stopwords → lemmatize
    if tokenize: return tokens
    return ' '.join(tokens)
```

### 3. **Utilities** ([sparse/utils.py](sparse/utils.py))
Lightweight regex-based functions used by default `parse()`:
- `lowercase()`, `remove_punctuation()` — no dependencies required
- Serves as fallback when no engine specified

---

## Key Patterns & Conventions

### **Options Flow Pattern**
```python
# In parse():
if engine:
    return _dispatch_engine(engine, text, locals())
# In _dispatch_engine():
engine_options = {'lowercase': ..., 'remove_punctuation': ..., **extra_kwargs}
from sparse.engines import {engine}_engine
return {engine}_engine.parse(text, **engine_options)
```
All engines receive flattened dict of options as kwargs — **do not modify this dispatch pattern**.

### **Token Processing Pipeline** (Standard Order)
All engines apply transformations in this order for consistency:
1. **Tokenize** (lowercase early if needed for filtering)
2. **Remove punctuation** (filter tokens)
3. **Remove stop words** (filter tokens)
4. **Lemmatize** (transform tokens)
5. **Format output** (tokenized list or joined string)

See [spacy_engine.py](sparse/engines/spacy_engine.py#L50-L80) for reference implementation.

### **NLTK Data Management**
- Engines detect missing data and raise `RuntimeError` with exact download command
- Preferred data: `punkt_tab` (newer NLTK), fallback to `punkt`
- Always check availability before use (see [nltk_engine.py](sparse/engines/nltk_engine.py#L33-L38))

### **Optional Dependency Pattern**
- **Core imports fail gracefully:** `try/except ImportError` in `_dispatch_engine()`
- **Runtime errors:** Clear messages with installation commands (e.g., `python -m spacy download en_core_web_sm`)
- **Extras groups:** `pyproject.toml` defines core/advanced/specialized/utils—installed separately by users

---

## Testing & Development Workflow

### Running Tests
```bash
pytest tests/ -v              # Run all (21 tests)
pytest tests/test_sparse.py   # Core utilities & parse()
pytest tests/test_engines_spacy.py  # spaCy-specific tests
```

### Test Organization
- **[test_sparse.py](tests/test_sparse.py):** Core parse() + utils tests (no engine dependencies)
- **[test_engines_spacy.py](tests/test_engines_spacy.py):** Engine-specific tests (requires model)
- **Pattern:** Use `unittest.TestCase`, assert actual behavior (not aspirations)

### Adding a New Engine
1. Create `sparse/engines/{name}_engine.py` with `parse(text, **kwargs)` function
2. Add engine-specific options as kwargs (e.g., `model=` for spaCy)
3. Update `_dispatch_engine()` with new elif branch for routing
4. Add `test_engines_{name}.py` with basic tokenization + feature tests
5. Update [Engine-Implementation-Roadmap.md](docs/spec/Engine-Implementation-Roadmap.md) to mark complete

---

## Cross-Component Communication

- **No shared state:** Engines are stateless functions, instantiate library internals on each call
- **Config flow:** Options always pass through kwargs dict, never globals
- **Error propagation:** Engines raise exceptions (never silent failures); main parse() lets them bubble
- **Import safety:** `_dispatch_engine()` handles ImportError for missing optional deps

---

## Project-Specific Gotchas

1. **Order matters in token processing:** Don't lowercase before stop-word filtering (affects accuracy)
2. **spaCy model required:** Always check `nlp = spacy.load(model)` fails gracefully with download hint
3. **Punctuation removal differs by engine:** NLTK keeps tokens, TextBlob filters non-alphanumeric
4. **Return type consistency:** Respect `tokenize=True` for all engines—must return list or str
5. **NLTK corpus data:** `punkt_tab` vs `punkt` compatibility—check both before failing

---

## Resources

- **Roadmap:** [Engine-Implementation-Roadmap.md](docs/spec/Engine-Implementation-Roadmap.md)
- **Main API:** [sparse/__init__.py](sparse/__init__.py)
- **Engines reference:** [nltk_engine.py](sparse/engines/nltk_engine.py), [spacy_engine.py](sparse/engines/spacy_engine.py), [textblob_engine.py](sparse/engines/textblob_engine.py)
- **Tests:** [tests/](tests/)
- **Config:** [pyproject.toml](pyproject.toml) (extras groups), [requirements.txt](requirements.txt) (dev deps)
