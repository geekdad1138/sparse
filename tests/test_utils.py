"""Tests for utility helper modules."""

import unittest
from sparse import utils


class TestNormalizationUtilities(unittest.TestCase):
    def test_lowercase_and_punctuation(self):
        self.assertEqual(utils.lowercase("HELLO"), "hello")
        self.assertEqual(utils.remove_punctuation("Hello, world!"), "Hello world")

    def test_fix_text_optional(self):
        try:
            _ = utils.fix_text("Ã©")
        except RuntimeError:
            self.skipTest("ftfy not installed")

    def test_transliterate_optional(self):
        try:
            _ = utils.transliterate("Café")
        except RuntimeError:
            self.skipTest("Unidecode not installed")

    def test_remove_emoji_optional(self):
        try:
            self.assertEqual(utils.remove_emoji("hello😀"), "hello")
        except RuntimeError:
            self.skipTest("emoji not installed")


class TestLanguageDetection(unittest.TestCase):
    def test_language_detection_optional(self):
        try:
            lang = utils.detect_language("This is a test", engine="langdetect")
            self.assertIsInstance(lang, str)
        except RuntimeError:
            self.skipTest("langdetect not installed")


class TestHTMLCleaning(unittest.TestCase):
    def test_html_cleaning_optional(self):
        try:
            out = utils.clean_html("<p>Hello <b>world</b></p>")
            self.assertIn("Hello", out)
        except RuntimeError:
            self.skipTest("beautifulsoup4 or bleach not installed")

    def test_remove_urls(self):
        self.assertEqual(utils.remove_urls("Visit https://example.com"), "Visit ")
