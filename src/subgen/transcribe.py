# in transcribe.py
from faster_whisper import WhisperModel

from .srt import Cue


def transcribe(wav_path, lang=None, model_name="small") -> tuple[list[Cue], str]:
    model = WhisperModel(model_name)
    segments, info = model.transcribe(str(wav_path), language=lang)
    cues = [Cue(seg.start, seg.end, seg.text.strip()) for seg in segments]
    return cues, info.language
