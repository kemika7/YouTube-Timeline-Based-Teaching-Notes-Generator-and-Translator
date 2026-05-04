from deep_translator import GoogleTranslator


class TranslationError(Exception):
    pass


CHUNK_SIZE = 4500


def translate_text(text: str, target_language: str, source_language: str = "auto") -> str:
    if not text:
        return ""
    if source_language and source_language != "auto" and source_language == target_language:
        return text

    try:
        translator = GoogleTranslator(source=source_language or "auto", target=target_language)
        chunks = [text[i : i + CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]
        translated_parts = [translator.translate(chunk) for chunk in chunks if chunk.strip()]
        return " ".join(part for part in translated_parts if part).strip()
    except Exception as e:
        raise TranslationError(f"Translation failed: {e}")
