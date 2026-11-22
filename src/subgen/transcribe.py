from faster_whisper import WhisperModel


def transcribe(wav_path, lang=None, model_name="small"):
    model = WhisperModel(model_name)
    segments, info = model.transcribe(str(wav_path), language=lang)
    print(f"detected language: {info.language} ({info.language_probability:.2f})")
    for seg in segments:
        print(f"[{seg.start:6.2f} -> {seg.end:6.2f}] {seg.text}")
