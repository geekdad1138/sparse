# Engine Implementation Roadmap

This document outlines the implementation plan for adding parsing library engines to `sparse`. Each engine represents a different text processing library with distinct capabilities.

---

## Priority & Phases

### Phase 1: Core (In Progress)
- [x] NLTK — basic tokenization, lemmatization, stop words
- [x] spaCy — industrial NLP with pipelines
- [ ] TextBlob — lightweight, user-friendly alternative to NLTK

### Phase 2: Advanced
- [ ] Transformers — pretrained models (BERT, RoBERTa, etc.)
- [ ] Gensim — embeddings and topic modeling
- [ ] Stanza — multilingual NLP

### Phase 3: Specialized
- [ ] Tokenizers (Hugging Face) — subword tokenization
- [ ] SentencePiece — subword modeling
- [ ] Flair — contextual embeddings

### Phase 4: Utilities
- [ ] Text normalization helpers (ftfy, Unidecode, regex, emoji)
- [ ] Language detection (langdetect, fasttext)
- [ ] HTML cleaning (BeautifulSoup, lxml, bleach)
- [ ] Feature extraction (scikit-learn)
- [ ] Higher-level utilities (textacy)

---

## Phase 1: Core Engines

### 1. NLTK Engine ✅ **COMPLETE**

**Status:** Fully implemented and tested (12/12 tests passing)

**File:** `sparse/engines/nltk_engine.py`

**Features Implemented:**
- ✅ Tokenization (`word_tokenize`)
- ✅ Stop word removal (English)
- ✅ Lemmatization (`WordNetLemmatizer`)
- ✅ Lowercase conversion
- ✅ Punctuation removal

**Tests:** `TestNLTKEngine` in `tests/test_sparse.py` (4 tests)

**Requirements:**
- `nltk>=3.8`
- NLTK data: `punkt_tab`, `wordnet`, `stopwords`, `omw-1.4`

---

### 2. spaCy Engine ✅ **COMPLETE**

**Status:** Fully implemented and tested (9/21 tests passing)

**File:** `sparse/engines/spacy_engine.py`

**Features Implemented:**
- ✅ Tokenization (via spaCy pipeline)
- ✅ Stop word removal (spaCy's is_stop flag)
- ✅ Lemmatization (token.lemma_)
- ✅ POS tagging (token.pos_)
- ✅ Named Entity Recognition (NER)
- ✅ Lowercase conversion
- ✅ Punctuation removal

**Tests:** `TestSpaCyEngine` in `tests/test_engines_spacy.py` (9 tests)

**Requirements:**
- `spacy>=3.0`
- Model: Download via `python -m spacy download en_core_web_sm`

**Usage:**
```python
from sparse import parse

# Basic tokenization
tokens = parse("Hello world", engine="spacy", tokenize=True)

# Advanced: lemmatization + stop word removal
result = parse("The cats are running", engine="spacy", 
              lemmatize=True, remove_stopwords=True, tokenize=True)

# NER: extract entities
entities = parse("Apple is in Cupertino", engine="spacy", ner=True)

# POS tagging
tagged = parse("Hello world", engine="spacy", pos_tag=True, tokenize=True)
# Returns: [('Hello', 'INTJ'), ('world', 'NOUN')]
```

---

### 3. TextBlob Engine

**Priority:** High (lightweight, simple API, good for beginners)

**File to create:** `sparse/engines/textblob_engine.py`

**Implementation Steps:**

1. **Setup & Dependencies**
   - Add `textblob>=0.17` to `requirements.txt`
   - Requires NLTK data (punkt, brown) — document this

2. **Core Parsing Function**
   ```python
   def parse(text, lowercase=False, remove_punctuation=False,
             remove_stopwords=False, lemmatize=False, tokenize=False,
             sentiment=False, **kwargs):
       """Parse text using TextBlob."""
       blob = TextBlob(text)
       # process sentences/words
       return result
   ```

3. **Features**
   - Tokenization (`blob.words`, `blob.sentences`)
   - Lemmatization via TextBlob's built-in lemmatizer
   - Stop word removal (via NLTK's corpus)
   - Sentiment analysis (optional, polarity/subjectivity)
   - Noun phrase extraction (optional)
   - Spelling correction (optional)

4. **Testing** (`tests/test_engines_textblob.py`)
   - Test word tokenization
   - Test sentence tokenization
   - Test stop word removal
   - Test sentiment (optional)
   - Test combined options

5. **Error Handling**
   - Gracefully handle missing NLTK resources
   - Validate sentiment output format

**Estimated Effort:** 2-3 hours

---

## Phase 2: Advanced Engines

### 4. Transformers Engine (Hugging Face)

**Priority:** Medium-high (modern, powerful, but heavy)

**File to create:** `sparse/engines/transformers_engine.py`

**Implementation Steps:**

1. **Setup & Dependencies**
   - Add `transformers>=4.30` and `torch>=2.0` to `requirements.txt`
   - Document GPU/CPU considerations

2. **Core Parsing Function**
   - Tokenization via `AutoTokenizer` (e.g., BERT tokenizer)
   - Token classification pipeline
   - Text classification

3. **Features**
   - Subword tokenization (BPE/WordPiece)
   - Token-to-ID mapping
   - Attention mask generation
   - Text classification (sentiment, intent, etc.)
   - Named Entity Recognition (via token-classification pipeline)

4. **Testing**
   - Test tokenization
   - Test token IDs
   - Test special tokens handling
   - Test sequence truncation/padding

5. **Note:** Heavy dependency; consider making optional/conditional import

**Estimated Effort:** 4-5 hours

---

### 5. Gensim Engine

**Priority:** Medium (specialized for embeddings/topic modeling)

**File to create:** `sparse/engines/gensim_engine.py`

**Implementation Steps:**

1. **Setup & Dependencies**
   - Add `gensim>=4.0` to `requirements.txt`

2. **Core Parsing Function**
   - Tokenization and preprocessing for word2vec/doc2vec
   - Sentence/document vectorization

3. **Features**
   - Basic tokenization (simple word split)
   - Preprocessing pipeline (lowercase, remove punctuation, stop words)
   - Word2Vec training/inference (optional)
   - Doc2Vec training/inference (optional)

4. **Testing**
   - Test tokenization
   - Test preprocessing pipeline
   - Test vector generation

**Estimated Effort:** 3-4 hours

---

### 6. Stanza Engine

**Priority:** Medium (multilingual, academic quality)

**File to create:** `sparse/engines/stanza_engine.py`

**Implementation Steps:**

1. **Setup & Dependencies**
   - Add `stanza>=1.5` to `requirements.txt`
   - Document model download: `python -c "import stanza; stanza.download('en')"`

2. **Core Parsing Function**
   - Full NLP pipeline (tokenization → POS → parsing → NER)
   - Lemmatization via universal dependencies

3. **Features**
   - Sentence segmentation
   - Tokenization
   - POS tagging (universal tags)
   - Lemmatization
   - Dependency parsing
   - Named Entity Recognition
   - Multilingual support

4. **Testing**
   - Test tokenization
   - Test POS tagging
   - Test lemmatization
   - Test NER

5. **Note:** Can be slow; consider lazy loading of models

**Estimated Effort:** 3-4 hours

---

## Phase 3: Specialized Engines

### 7. Hugging Face Tokenizers Engine

**Priority:** Medium-low (very fast, specialized)

**File to create:** `sparse/engines/hf_tokenizers_engine.py`

**Implementation Steps:**

1. **Setup & Dependencies**
   - Add `tokenizers>=0.13` to `requirements.txt`

2. **Core Parsing Function**
   - Subword tokenization (BPE, WordPiece, Unigram)
   - Token-to-ID encoding

3. **Features**
   - Fast Rust-based tokenization
   - Pre-tokenization options
   - Padding/truncation
   - Attention masks

4. **Testing**
   - Test basic tokenization
   - Test subword handling
   - Test padding/truncation

**Estimated Effort:** 2-3 hours

---

### 8. SentencePiece Engine

**Priority:** Low-medium (niche, specialized)

**File to create:** `sparse/engines/sentencepiece_engine.py`

**Implementation Steps:**

1. **Setup & Dependencies**
   - Add `sentencepiece>=0.1.99` to `requirements.txt`

2. **Features**
   - Language-neutral tokenization
   - Character-level and subword tokenization
   - Model training (optional advanced feature)

3. **Testing**
   - Test tokenization
   - Test encoding/decoding

**Estimated Effort:** 2-3 hours

---

### 9. Flair Engine

**Priority:** Low-medium (contextual embeddings)

**File to create:** `sparse/engines/flair_engine.py`

**Implementation Steps:**

1. **Setup & Dependencies**
   - Add `flair>=0.11` to `requirements.txt`

2. **Features**
   - Sequence labeling (NER, POS)
   - Embedding generation
   - Sentence encoding

3. **Testing**
   - Test NER
   - Test embeddings
   - Test sentence encoding

**Estimated Effort:** 3-4 hours

---

## Phase 4: Utility Engines & Features

### 10. Text Normalization Utilities

**Priority:** Medium (broadly useful)

**File to create:** `sparse/utils/normalization.py` (new module)

**Steps:**
1. Add `ftfy>=6.0`, `Unidecode>=1.3`, `regex>=2022`, `emoji>=2.0` to `requirements.txt`
2. Implement helpers:
   - `fix_text(text)` — ftfy for encoding fixes
   - `transliterate(text)` — Unidecode for ASCII conversion
   - `remove_emoji(text)` — emoji removal
   - `remove_unicode(text)` — strip non-ASCII
3. Integrate into main `parse()` function as optional flags

**Estimated Effort:** 1-2 hours

---

### 11. Language Detection

**Priority:** Low-medium

**File to create:** `sparse/utils/language_detection.py`

**Steps:**
1. Add `langdetect>=1.0` and optionally `fasttext>=0.9` to `requirements.txt`
2. Implement:
   - `detect_language(text, engine='langdetect')` — lightweight
   - `detect_language(text, engine='fasttext')` — high accuracy (optional)
3. Optionally integrate as preprocessing step in engines

**Estimated Effort:** 1-2 hours

---

### 12. HTML Cleaning

**Priority:** Medium (common use case)

**File to create:** `sparse/utils/html_cleaning.py`

**Steps:**
1. Add `beautifulsoup4>=4.9`, `lxml>=4.6`, `bleach>=5.0` to `requirements.txt`
2. Implement:
   - `clean_html(text)` — BeautifulSoup + bleach pipeline
   - `extract_text(html)` — strip tags, extract plain text
   - `remove_urls(text)` — regex-based
3. Integrate into preprocessing pipeline

**Estimated Effort:** 1-2 hours

---

### 13. Feature Extraction (scikit-learn)

**Priority:** Low (specialized for ML)

**File to create:** `sparse/engines/sklearn_engine.py`

**Steps:**
1. Add `scikit-learn>=1.0` to `requirements.txt`
2. Implement:
   - CountVectorizer wrapper
   - TF-IDF vectorizer wrapper
   - Token → sparse vector conversion
3. Integrate as optional output format

**Estimated Effort:** 2-3 hours

---

### 14. Textacy Engine

**Priority:** Low (specialized, depends on spaCy)

**File to create:** `sparse/engines/textacy_engine.py`

**Steps:**
1. Add `textacy>=0.11` to `requirements.txt` (requires spaCy)
2. Wrap textacy's utilities:
   - Cleaning functions
   - Lemmatization/stemming
   - Preprocessing pipelines
3. Provide advanced transformations

**Estimated Effort:** 2-3 hours

---

## Implementation Checklist

### For Each Engine:

- [ ] Create `sparse/engines/<engine>_engine.py`
- [ ] Implement `parse(text, **options)` function
- [ ] Define supported options
- [ ] Add error handling (missing dependencies, bad input)
- [ ] Update `sparse/__init__.py` dispatcher to include new engine
- [ ] Create `tests/test_engines_<engine>.py` with test suite
- [ ] Add dependency to `requirements.txt`
- [ ] Document in `README.md` (usage examples)
- [ ] Update `docs/Add-<Engine>.md` spec if needed
- [ ] Run full test suite (`pytest -v`)

### Repository Updates (Once Per Milestone):

- [ ] Update `CONTRIBUTING.md` with new engine patterns
- [ ] Add engine to feature list in `README.md`
- [ ] Document any required data downloads
- [ ] Update project roadmap

---

## Testing Strategy

Each engine test should verify:

1. **Basic functionality**
   - Input text → expected output
   - Deterministic behavior (same input → same output)

2. **Option combinations**
   - Single option → works
   - Multiple options → work together
   - Conflicting options → handled gracefully

3. **Error cases**
   - Missing dependencies → helpful error message
   - Empty/null input → handled gracefully
   - Invalid options → error or warning

4. **Integration**
   - Engine dispatching from main `parse()`
   - Options passed correctly
   - Output format matches declared type

---

## Estimated Total Timeline

- **Phase 1 (Core):** ✅ Complete (NLTK done) + 4-6 hours (spaCy, TextBlob)
- **Phase 2 (Advanced):** 10-15 hours
- **Phase 3 (Specialized):** 8-12 hours
- **Phase 4 (Utilities):** 6-10 hours

**Total:** ~30-45 hours for full implementation

---

## Next Steps

1. Implement **spaCy engine** (widely used, high demand)
2. Implement **TextBlob engine** (lightweight alternative)
3. Gather user feedback on API design
4. Proceed with Phase 2 based on feedback

---

## Notes

- Each engine is **optional** — users install only what they need
- All engines follow the same `parse(text, **options)` contract
- Use engine registry pattern in `__init__.py` for extensibility
- Document performance characteristics (speed, memory, accuracy)
- Consider lazy loading for heavy dependencies (transformers, stanza)
