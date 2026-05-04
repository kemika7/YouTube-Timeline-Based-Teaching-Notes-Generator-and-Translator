export default function UrlInput({ value, onChange, disabled }) {
  return (
    <div>
      <label className="block text-sm font-medium text-slate-700 mb-1.5">YouTube URL</label>
      <input
        type="url"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        placeholder="https://www.youtube.com/watch?v=..."
        className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-rose-500 focus:border-transparent disabled:bg-slate-50"
      />
    </div>
  )
}
