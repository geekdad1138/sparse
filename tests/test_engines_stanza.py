"""Tests for the Stanza engine."""

import unittest
from sparse import parse


class TestStanzaEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import stanza  # noqa: F401
            # try loading pipeline; if model missing, skip
            try:
                stanza.Pipeline(lang='en', processors='tokenize')
            except Exception:
                raise unittest.SkipTest("Stanza English models not installed")
        except ImportError:
            raise unittest.SkipTest("Stanza not installed")

    def test_stanza_tokenize(self):
        result = parse("Hello world", engine="stanza", tokenize=True)
        self.assertIsInstance(result, list)
        self.assertIn("Hello", result)
        self.assertIn("world", result)

    def test_stanza_lemmatize(self):
        result = parse("cats dogs running", engine="stanza", tokenize=True, lemmatize=True)
        # depending on stanza version, lemmas may be lowercase or not
        lemmas = [t.lower() for t in result]
        self.assertIn("cat", lemmas)
        self.assertIn("dog", lemmas)

    def test_stanza_remove_punct(self):
        result = parse("Hello, world!", engine="stanza", tokenize=True, remove_punctuation=True)
        self.assertNotIn(",", result)
        self.assertNotIn("!", result)

    def test_stanza_joined(self):
        joined = parse("Hello world", engine="stanza", tokenize=False)
        self.assertIsInstance(joined, str)
        self.assertIn("Hello", joined)

    def test_stanza_ner(self):
        ents = parse("Apple is in Cupertino", engine="stanza", ner=True)
        self.assertIsInstance(ents, list)
        self.assertGreaterEqual(len(ents), 1)
        self.assertIsInstance(ents[0], dict)
        self.assertIn("text", ents[0])


if __name__ == '__main__':
    unittest.main()
