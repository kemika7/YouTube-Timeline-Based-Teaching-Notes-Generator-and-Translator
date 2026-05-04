from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL


class NotesError(Exception):
    pass


PROMPTS = {
    "summary": (
        "You are an expert teacher. Read the following transcript and produce a concise summary "
        "(150-250 words) in {language}. Use clear language and capture the main ideas, "
        "in plain prose without headings."
    ),
    "detailed": (
        "You are an expert teacher. Read the transcript and produce thorough, well-structured "
        "teaching notes in {language}. Use Markdown with:\n"
        "- A short Overview paragraph\n"
        "- Section headings (## and ###)\n"
        "- Bullet points for key ideas\n"
        "- Concrete examples where helpful\n"
        "- A final '## Key Concepts' section listing terms and short definitions\n"
        "- A short '## Summary' at the end."
    ),
    "bullets": (
        "Convert the transcript into clean Markdown bullet-point notes in {language}. "
        "Group related bullets under bold subheadings (e.g. **Heading**). "
        "Keep bullets short and information-dense; avoid filler."
    ),
    "takeaways": (
        "Extract the 5-10 most important key takeaways from the transcript in {language}. "
        "Format as a numbered Markdown list, each item being a single clear sentence."
    ),
}


def _client() -> OpenAI:
    if not OPENAI_API_KEY:
        raise NotesError("OPENAI_API_KEY is not configured. Set it in backend/.env.")
    kwargs = {"api_key": OPENAI_API_KEY}
    if OPENAI_BASE_URL:
        kwargs["base_url"] = OPENAI_BASE_URL
    return OpenAI(**kwargs)


def generate_notes(transcript: str, format: str = "detailed", language: str = "English") -> str:
    if not transcript or not transcript.strip():
        raise NotesError("Transcript is empty.")
    if format not in PROMPTS:
        raise NotesError(f"Unsupported format: {format}")

    system_prompt = PROMPTS[format].format(language=language)

    try:
        client = _client()
        completion = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Transcript:\n\n{transcript}"},
            ],
            temperature=0.4,
        )
        content = completion.choices[0].message.content
        return (content or "").strip()
    except NotesError:
        raise
    except Exception as e:
        raise NotesError(f"AI generation failed: {e}")
