# YouTube Notes Generator

Convert any YouTube video URL into structured, easy-to-read notes — summaries, detailed notes, bullet points, or key takeaways — in 10+ languages.

## Stack

- **Backend:** Python 3.12 · FastAPI · `youtube-transcript-api` · `deep-translator` · OpenAI
- **Frontend:** React 18 (Vite) · Tailwind CSS · axios · jsPDF · react-markdown

## Project structure

```
.
├── backend/
│   ├── app.py                # FastAPI entrypoint
│   ├── config.py             # env loading
│   ├── requirements.txt
│   ├── .env.example
│   ├── models/
│   │   └── schemas.py        # Pydantic request/response models
│   ├── routes/
│   │   └── api.py            # REST endpoints
│   ├── services/
│   │   ├── transcript_service.py
│   │   ├── translation_service.py
│   │   ├── notes_service.py
│   │   ├── cache_service.py
│   │   └── history_service.py
│   └── utils/
│       └── youtube_utils.py
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── postcss.config.js
    ├── index.html
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── index.css
        ├── services/api.js
        ├── utils/youtube.js
        └── components/
            ├── UrlInput.jsx
            ├── LanguageSelector.jsx
            ├── FormatSelector.jsx
            ├── VideoPreview.jsx
            ├── NotesDisplay.jsx
            ├── HistoryPanel.jsx
            ├── LoadingSpinner.jsx
            └── ErrorMessage.jsx
```

## Run locally

### 1. Backend (Python 3.12)

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then edit and add your OPENAI_API_KEY
uvicorn app:app --reload --port 8000
```

The API will be available at `http://localhost:8000` (interactive docs at `http://localhost:8000/docs`).

### 2. Frontend

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The Vite dev server proxies `/api/*` to `http://localhost:8000`, so no extra config is needed.

## Environment variables

`backend/.env` (copy from `.env.example`):

| Variable | Description | Default |
|---|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key | _required_ |
| `OPENAI_MODEL` | Chat model to use | `gpt-4o-mini` |
| `CACHE_DIR` | Folder for transcript cache | `.cache` |
| `HISTORY_FILE` | Path to history JSON | `.cache/history.json` |
| `PORT` | Uvicorn port | `8000` |

## REST API

| Method | Path | Body | Purpose |
|---|---|---|---|
| `POST` | `/api/extract-transcript` | `{ url, language? }` | Fetch & cache transcript |
| `POST` | `/api/translate` | `{ text, target_language, source_language? }` | Translate any text |
| `POST` | `/api/generate-notes` | `{ url, language, format }` | Full pipeline → structured notes |
| `GET`  | `/api/history` | — | List recent generations |
| `DELETE` | `/api/history` | — | Clear history |
| `GET`  | `/api/languages` | — | Supported languages |

`format` is one of: `summary`, `detailed`, `bullets`, `takeaways`.

## Features

- ✅ YouTube URL → transcript → translation → AI notes pipeline
- ✅ 4 output formats (summary, detailed, bullets, takeaways)
- ✅ 10+ languages supported
- ✅ Embedded video preview
- ✅ Copy / download as `.txt` / download as `.pdf`
- ✅ Transcript caching (memory + disk)
- ✅ History of past generations (click to reload)
- ✅ Loading skeletons + friendly error messages
- ✅ Mobile + desktop responsive
- ✅ Modular backend (separate services for transcript, translation, AI)

## Error handling

The backend surfaces clear messages for:

- Invalid YouTube URL
- Video has no transcript / transcripts disabled / video unavailable
- Translation API failure
- Missing or invalid OpenAI key, model errors

Failures return HTTP 4xx/5xx with `{ "detail": "..." }`, which the frontend displays inline.
# YouTube-Timeline-Based-Teaching-Notes-Generator-and-Translator
