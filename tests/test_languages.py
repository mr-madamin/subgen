from subgen.languages import normalize


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
