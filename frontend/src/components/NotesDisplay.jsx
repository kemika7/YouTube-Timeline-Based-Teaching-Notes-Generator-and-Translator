import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import jsPDF from 'jspdf'

const FORMAT_LABELS = {
  summary: 'Summary',
  detailed: 'Detailed Notes',
  bullets: 'Bullet Points',
  takeaways: 'Key Takeaways',
}

export default function NotesDisplay({ notes, loading, videoId, format }) {
  const [copied, setCopied] = useState(false)

  if (loading) {
    return (
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 space-y-3">
        <div className="h-4 w-1/3 bg-slate-200 rounded animate-pulse" />
        <div className="h-3 w-full bg-slate-200 rounded animate-pulse" />
        <div className="h-3 w-5/6 bg-slate-200 rounded animate-pulse" />
        <div className="h-3 w-4/6 bg-slate-200 rounded animate-pulse" />
        <div className="h-3 w-full bg-slate-200 rounded animate-pulse" />
        <div className="h-3 w-3/4 bg-slate-200 rounded animate-pulse" />
      </div>
    )
  }

  if (!notes) return null

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(notes)
      setCopied(true)
      setTimeout(() => setCopied(false), 1500)
    } catch {
      setCopied(false)
    }
  }

  function handleDownloadTxt() {
    const blob = new Blob([notes], { type: 'text/plain;charset=utf-8' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = `notes_${videoId || 'youtube'}.txt`
    link.click()
    URL.revokeObjectURL(link.href)
  }

  function handleDownloadPdf() {
    const doc = new jsPDF({ unit: 'pt', format: 'a4' })
    const margin = 40
    const maxWidth = doc.internal.pageSize.getWidth() - margin * 2
    const pageHeight = doc.internal.pageSize.getHeight()
    doc.setFont('helvetica', 'normal')
    doc.setFontSize(11)
    const lines = doc.splitTextToSize(notes, maxWidth)
    let y = margin
    lines.forEach((line) => {
      if (y > pageHeight - margin) {
        doc.addPage()
        y = margin
      }
      doc.text(line, margin, y)
      y += 14
    })
    doc.save(`notes_${videoId || 'youtube'}.pdf`)
  }

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
      <div className="flex items-center justify-between mb-4 flex-wrap gap-2">
        <h2 className="text-lg font-semibold">{FORMAT_LABELS[format] || 'Notes'}</h2>
        <div className="flex gap-2 text-sm">
          <button
            onClick={handleCopy}
            className="rounded-lg border border-slate-300 px-3 py-1.5 hover:bg-slate-50 transition"
          >
            {copied ? 'Copied!' : 'Copy'}
          </button>
          <button
            onClick={handleDownloadTxt}
            className="rounded-lg border border-slate-300 px-3 py-1.5 hover:bg-slate-50 transition"
          >
            .txt
          </button>
          <button
            onClick={handleDownloadPdf}
            className="rounded-lg border border-slate-300 px-3 py-1.5 hover:bg-slate-50 transition"
          >
            .pdf
          </button>
        </div>
      </div>
      <article className="prose prose-slate max-w-none prose-headings:font-semibold prose-h2:text-xl prose-h3:text-lg prose-p:leading-relaxed">
        <ReactMarkdown>{notes}</ReactMarkdown>
      </article>
    </div>
  )
}
