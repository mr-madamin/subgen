from faster_whisper import WhisperModel

from .srt import Cue


def _segments_to_cues(segments) -> list[Cue]:
    return [Cue(seg.start, seg.end, seg.text.strip()) for seg in segments]


def transcribe(media_path, lang=None, model_name="small") -> tuple[list[Cue], str]:
    model = WhisperModel(model_name)
    segments, info = model.transcribe(str(media_path), language=lang)
    return _segments_to_cues(segments), info.language
