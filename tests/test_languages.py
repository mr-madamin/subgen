import unicodedata

from subgen.languages import LANGUAGES, match_title, normalize


def test_normalize_three_letter_tag():
    assert normalize("eng") == "en"


def test_normalize_two_letter_code():
    assert normalize("en") == "en"


def test_normalize_is_case_insensitive():
    assert normalize("EN") == "en"


def test_normalize_messy_input():
    assert normalize("  SPA ") == "es"


def test_normalize_unknown_code_returns_none():
    assert normalize("und") is None


def test_match_title_uppercase_with_extra_text():
    assert match_title("ENGLISH (Director Cut)") == "en"


def test_match_title_unknown():
    assert match_title("Commentary") is None


def test_match_title_empty():
    assert match_title("") is None


def test_match_title_accented_keyword():
    assert match_title("Español 5.1") == "es"


def test_match_title_decomposed_unicode():
    title = unicodedata.normalize("NFD", "Español 5.1")
    assert title != "Español 5.1"
    assert match_title(title) == "es"


def test_keywords_are_nfc():
    for lang in LANGUAGES:
        for keyword in lang.keywords:
            assert unicodedata.is_normalized("NFC", keyword), (
                f"{lang.code2}: {keyword!r} is not NFC"
            )
