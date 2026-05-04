import { useEffect, useState } from 'react'
import UrlInput from './components/UrlInput'
import LanguageSelector from './components/LanguageSelector'
import FormatSelector from './components/FormatSelector'
import VideoPreview from './components/VideoPreview'
import NotesDisplay from './components/NotesDisplay'
import HistoryPanel from './components/HistoryPanel'
import LoadingSpinner from './components/LoadingSpinner'
import ErrorMessage from './components/ErrorMessage'
import {
  generateNotes,
  getLanguages,
  getHistory,
  clearHistory,
} from './services/api'
import { extractVideoId, isValidYouTubeUrl } from './utils/youtube'

const DEFAULT_LANGUAGES = [
  { code: 'en', name: 'English' },
  { code: 'es', name: 'Spanish' },
  { code: 'fr', name: 'French' },
  { code: 'de', name: 'German' },
  { code: 'hi', name: 'Hindi' },
  { code: 'zh-CN', name: 'Chinese (Simplified)' },
  { code: 'ja', name: 'Japanese' },
  { code: 'ar', name: 'Arabic' },
  { code: 'pt', name: 'Portuguese' },
  { code: 'ru', name: 'Russian' },
]

const FORMATS = [
  { value: 'summary', label: 'Summary' },
  { value: 'detailed', label: 'Detailed Notes' },
  { value: 'bullets', label: 'Bullet Points' },
  { value: 'takeaways', label: 'Key Takeaways' },
]

export default function App() {
  const [url, setUrl] = useState('')
  const [language, setLanguage] = useState('en')
  const [format, setFormat] = useState('detailed')
  const [languages, setLanguages] = useState(DEFAULT_LANGUAGES)
  const [notes, setNotes] = useState('')
  const [videoId, setVideoId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [history, setHistory] = useState([])

  useEffect(() => {
    getLanguages()
      .then((langs) => {
        if (langs?.length) setLanguages(langs)
      })
      .catch(() => {})
    refreshHistory()
  }, [])

  async function refreshHistory() {
    try {
      const items = await getHistory()
      setHistory(items)
    } catch {
      // ignore — history is optional
    }
  }

  async function handleGenerate() {
    setError('')
    if (!isValidYouTubeUrl(url)) {
      setError('Please enter a valid YouTube URL.')
      return
    }
    setLoading(true)
    setNotes('')
    setVideoId(extractVideoId(url))
    try {
      const result = await generateNotes({ url, language, format })
      setNotes(result.notes)
      setVideoId(result.video_id || extractVideoId(url))
      refreshHistory()
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
          err.message ||
          'Something went wrong. Please try again.',
      )
    } finally {
      setLoading(false)
    }
  }

  function loadFromHistory(item) {
    setUrl(item.url || '')
    setLanguage(item.language || 'en')
    setFormat(item.format || 'detailed')
    setNotes(item.notes || '')
    setVideoId(item.video_id || extractVideoId(item.url))
    setError('')
  }

  async function handleClearHistory() {
    try {
      await clearHistory()
      refreshHistory()
    } catch {
      // ignore
    }
  }

  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto max-w-6xl px-4 py-5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-lg bg-gradient-to-br from-rose-500 to-orange-500 flex items-center justify-center text-white font-bold">
              YT
            </div>
            <div>
              <h1 className="text-lg font-semibold">YouTube Notes Generator</h1>
              <p className="text-xs text-slate-500">
                Turn any video into structured notes
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-8 grid gap-6 lg:grid-cols-3">
        <section className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 space-y-4">
            <UrlInput value={url} onChange={setUrl} disabled={loading} />
            <div className="grid sm:grid-cols-2 gap-4">
              <LanguageSelector
                value={language}
                onChange={setLanguage}
                options={languages}
                disabled={loading}
              />
              <FormatSelector
                value={format}
                onChange={setFormat}
                options={FORMATS}
                disabled={loading}
              />
            </div>
            <button
              onClick={handleGenerate}
              disabled={loading || !url}
              className="w-full inline-flex items-center justify-center gap-2 rounded-xl bg-rose-600 px-4 py-3 text-white font-medium hover:bg-rose-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              {loading ? (
                <>
                  <LoadingSpinner /> Generating…
                </>
              ) : (
                'Generate Notes'
              )}
            </button>
            <ErrorMessage message={error} />
          </div>

          {videoId && <VideoPreview videoId={videoId} />}

          <NotesDisplay
            notes={notes}
            loading={loading}
            videoId={videoId}
            format={format}
          />
        </section>

        <aside className="lg:col-span-1">
          <HistoryPanel
            items={history}
            onSelect={loadFromHistory}
            onClear={handleClearHistory}
          />
        </aside>
      </main>

      <footer className="mx-auto max-w-6xl px-4 py-8 text-center text-xs text-slate-500">
        Built with FastAPI · React · Tailwind · OpenAI
      </footer>
    </div>
  )
}
