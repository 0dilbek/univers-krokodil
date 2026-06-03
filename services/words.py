import re
from pathlib import Path
from random import randrange

from constants import DEFAULT_WORDS_FILE
from models.crocodile import CrocodileWord


_SPACE_RE = re.compile(r"\s+")
_PUNCT_RE = re.compile(r"[^\w\s]+", re.UNICODE)
_CYRILLIC_TO_LATIN = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "ё": "yo",
    "ж": "j",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "x",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "ъ": "",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
    "ў": "o'",
    "қ": "q",
    "ғ": "g'",
    "ҳ": "h",
}
_YE_PREVIOUS_CHARS = set(" \t\n\r-_'`ʻʼ’\"([{аоэеиуўюяё")


def cyrillic_to_latin(text: str) -> str:
    result = []
    for index, char in enumerate(text):
        if char == "е":
            previous = text[index - 1] if index else " "
            result.append("ye" if previous in _YE_PREVIOUS_CHARS else "e")
            continue
        result.append(_CYRILLIC_TO_LATIN.get(char, char))
    return "".join(result)


def normalize_answer(text: str) -> str:
    value = cyrillic_to_latin(text.lower().strip())
    value = _PUNCT_RE.sub("", value)
    return _SPACE_RE.sub(" ", value).strip()


def word_mask(text: str) -> str:
    parts = []
    for char in text:
        if char.isspace():
            parts.append("   ")
        elif char in "-'":
            parts.append(char)
        else:
            parts.append("_")
    return " ".join(parts)


async def get_random_word(language: str = "uz") -> CrocodileWord:
    query = CrocodileWord.filter(is_active=True, language=language)
    count = await query.count()
    if count == 0:
        await import_words_from_file(DEFAULT_WORDS_FILE, language=language)
        count = await query.count()
    if count == 0:
        raise ValueError("Active crocodile words not found. Import words first.")
    word = await query.offset(randrange(count)).first()
    return word


async def import_words_from_file(path: str, language: str = "uz") -> int:
    file_path = Path(path)
    if not file_path.exists():
        return 0
    count = 0
    with file_path.open("r", encoding="utf-8") as file:
        for line in file:
            text = line.strip()
            if not text or text.startswith("#"):
                continue
            word, created = await CrocodileWord.get_or_create(
                text=text,
                defaults={"language": language, "difficulty": "medium", "is_active": True},
            )
            if not word.is_active:
                word.is_active = True
                word.language = language
                await word.save()
            if created:
                count += 1
    return count
