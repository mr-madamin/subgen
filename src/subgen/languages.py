import unicodedata
from dataclasses import dataclass

# Canonical language code is ISO 639-1 (code2), e.g. "en" — what --lang and
# faster-whisper use. ffprobe tags (ISO 639-2, code3) and track titles are
# normalized INTO code2 at the boundary.


@dataclass(frozen=True)
class Language:
    code2: str
    code3: str
    name: str
    keywords: tuple[str, ...] = ()


LANGUAGES = [
    Language("en", "eng", "English", ("english",)),
    Language("es", "spa", "Spanish", ("español", "espanol", "spanish")),
]


def normalize(code: str) -> str | None:
    c = code.strip().lower()
    for lang in LANGUAGES:
        if c == lang.code2 or c == lang.code3:
            return lang.code2
    return None


def match_title(title: str) -> str | None:
    t = unicodedata.normalize("NFC", title.lower())
    for lang in LANGUAGES:
        for keyword in lang.keywords:
            if keyword in t:
                return lang.code2
    return None
