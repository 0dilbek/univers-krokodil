from services.words import normalize_answer


def is_correct_answer(message_text: str, word_text: str) -> bool:
    return normalize_answer(message_text) == normalize_answer(word_text)
