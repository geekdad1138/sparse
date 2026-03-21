"""Tests for Textacy engine."""

import unittest
from unittest.mock import patch

try:
    import textacy
    TEXTACY_AVAILABLE = True
except ImportError:
    TEXTACY_AVAILABLE = False


class TestTextacyEngine(unittest.TestCase):
    """Test Textacy engine functionality."""

    @unittest.skipUnless(TEXTACY_AVAILABLE, "textacy not installed")
    def test_textacy_tokenize(self):
        """Test basic tokenization."""
        from sparse.engines.textacy_engine import parse

        with patch('spacy.load') as mock_load:
            mock_nlp = mock_load.return_value
            mock_doc = mock_nlp.return_value
            mock_doc.__iter__ = lambda: iter([])  # Mock doc iteration

            with patch('textacy.extract.words') as mock_words:
                mock_words.return_value = ['hello', 'world']
                result = parse("Hello world", tokenize=True)
                self.assertEqual(result, ['hello', 'world'])

    @unittest.skipUnless(TEXTACY_AVAILABLE, "textacy not installed")
    def test_textacy_joined(self):
        """Test joined output."""
        from sparse.engines.textacy_engine import parse

        with patch('spacy.load'):
            with patch('textacy.preprocessing.remove_punct') as mock_punct:
                mock_punct.return_value = "Hello world"
                result = parse("Hello world!", remove_punctuation=True)
                self.assertEqual(result, "Hello world")

    @unittest.skipUnless(TEXTACY_AVAILABLE, "textacy not installed")
    def test_textacy_keyterms(self):
        """Test keyterm extraction."""
        from sparse.engines.textacy_engine import parse

        with patch('spacy.load') as mock_load:
            mock_nlp = mock_load.return_value
            mock_doc = mock_nlp.return_value

            with patch('textacy.extract.keyterms.textrank') as mock_textrank:
                mock_textrank.return_value = [('hello', 0.8), ('world', 0.6)]
                result = parse("Hello world", keyterms=True)
                self.assertEqual(result, [('hello', 0.8), ('world', 0.6)])

    @unittest.skipUnless(TEXTACY_AVAILABLE, "textacy not installed")
    def test_textacy_readability(self):
        """Test readability statistics."""
        from sparse.engines.textacy_engine import parse

        with patch('spacy.load') as mock_load:
            mock_nlp = mock_load.return_value
            mock_doc = mock_nlp.return_value

            with patch('textacy.text_stats.readability') as mock_readability:
                mock_readability.return_value = {'flesch_kincaid_grade_level': 8.5}
                result = parse("This is a test text.", readability=True)
                self.assertEqual(result, {'flesch_kincaid_grade_level': 8.5})

    def test_textacy_missing_dependency(self):
        """Test error when textacy not installed."""
        from sparse.engines.textacy_engine import parse

        with patch.dict('sys.modules', {'textacy': None}):
            with self.assertRaises(RuntimeError) as cm:
                parse("test")
            self.assertIn("textacy", str(cm.exception))

    @unittest.skipUnless(TEXTACY_AVAILABLE, "textacy not installed")
    def test_textacy_missing_model(self):
        """Test error when spaCy model not found."""
        from sparse.engines.textacy_engine import parse

        with patch('spacy.load', side_effect=OSError("Model not found")):
            with self.assertRaises(RuntimeError) as cm:
                parse("test")
            self.assertIn("spaCy model", str(cm.exception))