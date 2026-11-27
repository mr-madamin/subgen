import unicodedata

import pytest

from subgen.audio import AudioTrack
from subgen.languages import LANGUAGES, TrackError, match_title, normalize, pick_track


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


def _track(index, language=None, title=None):
    return AudioTrack(
        index=index,
        codec_name="aac",
        channels=2,
        sample_rate=48000,
        language=language,
        title=title,
    )


def test_pick_track_no_match_with_many_tracks_raises():
    tracks = [_track(1, "eng"), _track(2, "fre")]
    with pytest.raises(TrackError):
        pick_track(tracks, "es")


def test_pick_track_by_tag():
    tracks = [_track(1, "eng"), _track(2, "spa")]
    assert pick_track(tracks, "es") == tracks[1]


def test_pick_track_tag_beats_title():
    tracks = [_track(1, None, "Spanish commentary"), _track(2, "spa")]
    assert pick_track(tracks, "es") == tracks[1]


def test_pick_track_title_fallback():
    tracks = [_track(1, None, "Español"), _track(2, "eng")]
    assert pick_track(tracks, "es") == tracks[0]


def test_pick_track_first_of_two_matches():
    tracks = [_track(1, "spa"), _track(2, "spa")]
    assert pick_track(tracks, "es") == tracks[0]


def test_pick_track_single_untagged_track_raises():
    tracks = [_track(1)]
    with pytest.raises(TrackError):
        pick_track(tracks, "es")


def test_pick_track_auto_takes_first():
    tracks = [_track(1), _track(2)]
    assert pick_track(tracks) == tracks[0]
