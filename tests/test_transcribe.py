from types import SimpleNamespace

from subgen.srt import Cue
from subgen.transcribe import _segments_to_cues


def _seg(start, end, text):
    return SimpleNamespace(start=start, end=end, text=text)


def test_maps_segments_to_cues_in_order():
    segs = [_seg(0.0, 1.0, "Hello"), _seg(2.0, 3.5, "there")]
    assert _segments_to_cues(segs) == [Cue(0.0, 1.0, "Hello"), Cue(2.0, 3.5, "there")]


def test_strips_whisper_leading_space():
    (cue,) = _segments_to_cues([_seg(0.0, 1.0, "  The water  ")])
    assert cue.text == "The water"


def test_empty_segments_gives_empty_list():
    assert _segments_to_cues([]) == []
