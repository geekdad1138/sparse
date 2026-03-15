# Add Hugging Face Transformers Engine — Developer Spec

This document describes the design and implementation plan for adding a Hugging Face Transformers engine to `sparse`, the unified text preprocessing library.

---

## Purpose & Scope

- Provide a Transformers-based adapter so `sparse.parse(..., engine="transformers")` can leverage modern pretrained models (BERT, RoBERTa, DistilBERT, etc.)
- Support subword tokenization, text classification, and token-level tasks (NER, POS tagging)
- Maintain consistency with existing engine architecture (NLTK, spaCy, TextBlob)
- Keep implementation modular and optional (heavy dependencies, large models)

---

## Current Repository Context

- **Existing engines:** NLTK, spaCy, TextBlob (all Phase 1 complete, 31/31 tests passing)
- **Engine contract:** All engines implement `parse(text, **options)` with consistent parameter names
- **Standard options:** `lowercase`, `remove_punctuation`, `remove_stopwords`, `lemmatize`, `tokenize`
- **Engine-specific options:** Engine can add custom kwargs (e.g., spaCy has `ner=True`, `pos_tag=True`)
- **Dispatcher pattern:** `sparse/__init__.py` routes to engines with error handling for missing dependencies
- **Dependency strategy:** Extras groups in `pyproject.toml` (`[core]`, `[advanced]`, `[specialized]`, `[utils]`, `[all]`)

---

## Design Decisions & Options

### 1. Model Selection Strategy

**Option A: Single default model (BERT-base)**
- ✅ Pros: Simplest, consistent behavior, fast startup
- ❌ Cons: Limited flexibility for different use cases

**Option B: Configurable model with `model=` parameter**
- ✅ Pros: Users can choose BERT, RoBERTa, DistilBERT, etc.; supports multilingual models
- ❌ Cons: More complex, requires model validation and error handling

**Option C: Auto-detect from HuggingFace Hub**
- ✅ Pros: Maximum flexibility
- ❌ Cons: Requires internet, slow first-time downloads, brittle

**DECISION: Option B (Configurable with sensible default)**
- Default model: `bert-base-uncased` (lightweight, well-tested, fast)
- Allow `model="distilbert-base-uncased"` for even lighter deployments
- Allow `model="bert-base-multilingual-cased"` for multilingual support
- Validate model exists and can be loaded; provide helpful error if not

---

### 2. Supported Features

**Option A: Tokenization only**
- ✅ Pros: Simple, fast, consistent with other engines
- ❌ Cons: Underutilizes Transformers power

**Option B: Tokenization + text classification (sentiment, intent)**
- ✅ Pros: Modern capabilities, matches user expectations
- ❌ Cons: Requires task-specific models

**Option C: Tokenization + token classification (NER, POS)**
- ✅ Pros: Complements spaCy, provides modern NER
- ❌ Cons: Requires different model type

**Option D: All of the above with `task=` parameter**
- ✅ Pros: Maximum flexibility
- ❌ Cons: Complex, many model variants to track

**DECISION: Option A + Option C (Tokenization + token classification)**
- Focus on tokenization (subword tokens) as primary feature
- Add `task="ner"` for Named Entity Recognition (using token-classification pipeline)
- Leave text classification for future consideration (requires text-classification pipeline)
- Simpler initial implementation, expandable later

---

### 3. Return Format & Tokenization

**Option A: Subword tokens only**
```python
parse("hello world", engine="transformers", tokenize=True)
# Returns: ['hello', 'world']
```
- ✅ Pros: Matches other engines (string list)
- ❌ Cons: Loses model-specific token info (IDs, special tokens)

**Option B: Token IDs**
```python
parse("hello world", engine="transformers", tokenize=True)
# Returns: [101, 7592, 2088, 102]  # [CLS], hello, world, [SEP]
```
- ✅ Pros: Raw model input, useful for downstream tasks
- ❌ Cons: Less human-readable

**Option C: Dict with tokens and IDs**
```python
parse("hello world", engine="transformers", tokenize=True)
# Returns: {'tokens': ['[CLS]', 'hello', 'world', '[SEP]'], 
#           'token_ids': [101, 7592, 2088, 102],
#           'attention_mask': [1, 1, 1, 1]}
```
- ✅ Pros: Complete information
- ❌ Cons: Not consistent with other engines

**DECISION: Option A (Subword tokens) with optional IDs**
- Default `tokenize=True` returns subword tokens as list: `['hello', 'world']`
- Add `return_ids=True` to include token IDs: `{'tokens': [...], 'token_ids': [...]}`
- Keep consistency with other engines while allowing power users to get IDs

---

### 4. Device Handling (GPU vs CPU)

**Option A: Auto-detect GPU**
```python
device = "cuda" if torch.cuda.is_available() else "cpu"
```
- ✅ Pros: Transparent, fast if GPU available
- ❌ Cons: May consume memory unexpectedly, hard to debug

**Option B: Default to CPU, allow override**
```python
parse(text, engine="transformers", device="cuda")
```
- ✅ Pros: Predictable, safe, users opt-in to GPU
- ❌ Cons: CPU is slow for transformers

**Option C: Environment variable**
```python
SPARSE_DEVICE=cuda python script.py
```
- ✅ Pros: Global configuration
- ❌ Cons: Less explicit in code

**DECISION: Option A (Auto-detect) with Option B as override**
- Default: Auto-detect GPU if available (`torch.cuda.is_available()`)
- Allow explicit override: `parse(text, engine="transformers", device="cpu")`
- Log device choice for debugging (optional)

---

### 5. Model Loading & Caching

**Option A: Load on every call (stateless)**
```python
tokenizer = AutoTokenizer.from_pretrained(model)
model = AutoModel.from_pretrained(model)
# Process, then discard
```
- ✅ Pros: Stateless, no side effects, simple
- ❌ Cons: Very slow (1-2 seconds per call), not practical

**Option B: Module-level cache (stateful)**
```python
_tokenizer_cache = {}
def parse(text, model="bert-base-uncased", ...):
    if model not in _tokenizer_cache:
        _tokenizer_cache[model] = AutoTokenizer.from_pretrained(model)
    tokenizer = _tokenizer_cache[model]
```
- ✅ Pros: Fast after first load, minimal memory overhead
- ❌ Cons: Stateful (breaks pure function pattern)

**Option C: Global state with clear lifecycle**
```python
def load_model(model_name):
    global _transformers_state
    _transformers_state = {...}  # Load and cache

def parse(text, ...):
    # Use cached _transformers_state
```
- ✅ Pros: Explicit control, fast
- ❌ Cons: Requires user to call setup

**DECISION: Option B (Module-level cache)**
- Cache tokenizers and models per model name at module level
- First call loads model (1-2 seconds), subsequent calls instant
- Document that first call is slower; users may want to warm up
- No explicit setup required (differs from spaCy which needs download)

---

### 6. Dependency Management

**Dependencies to add:**
- `transformers>=4.30` (main library)
- `torch>=2.0` (required by transformers)
- Both go in `[advanced]` extras group (not `[core]`)

**Error handling:**
```python
try:
    import torch
    from transformers import AutoTokenizer, AutoModel
except ImportError:
    raise RuntimeError(
        "Transformers engine requires transformers and torch. "
        "Install with: pip install sparse[advanced]"
    )
```

---

## Implementation Checklist

### Phase 1: Core Engine
- [ ] Create `sparse/engines/transformers_engine.py`
  - [ ] Import handling for transformers + torch (with helpful errors)
  - [ ] Module-level cache dictionaries for tokenizers and models
  - [ ] `parse(text, model="bert-base-uncased", device=None, tokenize=False, return_ids=False, task=None, ...)`
  - [ ] Implement standard options: `lowercase`, `remove_punctuation` (applied before tokenization)
  - [ ] Implement subword tokenization with special tokens handling
  - [ ] Support `tokenize=True` → list of subword tokens
  - [ ] Support `return_ids=True` → include token IDs and attention masks
  - [ ] Error handling for missing models (helpful download hints)
  - [ ] Error handling for torch installation

- [ ] Update `sparse/__init__.py`
  - [ ] Add `transformers` case to `_dispatch_engine()` dispatcher
  - [ ] Pass `model`, `device`, `return_ids`, `task` through kwargs

- [ ] Update `pyproject.toml`
  - [ ] Add `transformers>=4.30` and `torch>=2.0` to `[advanced]` extras
  - [ ] (If not already there)

### Phase 2: Token Classification (NER)
- [ ] Add `task="ner"` support in transformers_engine.py
  - [ ] Use `pipeline("token-classification", model=model_name, device=device)`
  - [ ] Parse output to entities: `{'entity': 'PERSON', 'score': 0.99, 'word': 'John'}`
  - [ ] Support `task="ner"` parameter in parse()

### Phase 3: Testing
- [ ] Create `tests/test_engines_transformers.py`
  - [ ] Test 1: Basic tokenization (subword tokens)
  - [ ] Test 2: Tokenization with `tokenize=True`
  - [ ] Test 3: Token IDs with `return_ids=True`
  - [ ] Test 4: Different model (distilbert)
  - [ ] Test 5: `lowercase=True` before tokenization
  - [ ] Test 6: `remove_punctuation=True` before tokenization
  - [ ] Test 7: NER with `task="ner"`
  - [ ] Test 8: Device specification (`device="cpu"`)
  - [ ] Test 9: Error on missing model
  - [ ] Test 10: Error on missing transformers/torch dependency
  - [ ] Set up model downloads in test setup (handle first-run latency)

### Phase 4: Documentation
- [ ] Update `docs/spec/Engine-Implementation-Roadmap.md`
  - [ ] Mark Phase 2 / Transformers as COMPLETE
  - [ ] Add usage examples and features
- [ ] Update [sparse/README.md](../../../../README.md)
  - [ ] Add Transformers to features table
  - [ ] Include example usage

---

## Expected Implementation Time

- **Engine implementation:** 3-4 hours
- **Testing & debugging:** 2-3 hours
- **Documentation:** 1 hour
- **Total:** 6-8 hours

---

## Key Implementation Notes

1. **Model caching happens at module level** — First call to `parse(..., model="bert-base-uncased")` downloads and caches the model; subsequent calls use cache. Explain in docstring.

2. **Special tokens are preserved** — `[CLS]` and `[SEP]` tokens are included in tokenized output. Decide if we should strip them or document this behavior.

3. **Subword tokenization differs from word tokenization** — Users familiar with NLTK/spaCy may be surprised that "unhappy" becomes `['un', '##happy']`. Document clearly.

4. **Models are large** — BERT-base is ~440MB, transformers + torch is ~2GB. This is why it's in `[advanced]`, not `[core]`.

5. **First-call latency** — First `parse()` call with new model takes 1-2 seconds to download and load. Subsequent calls are <100ms. Consider warming up in tests.

6. **NER models are task-specific** — Can't use BERT-base for NER; need `dslim/bert-base-ner` or similar. Provide good defaults or let users specify.

---

## Appendix: Original Specification

This document was created from the following initial specification:

> This file will be a spec for discussion and decisions on how to implement hugging face as part of sparse.
> 
> It will show recommendations, lists of options, detailed information on what each option is for, and then finally decisions made for implementaion.