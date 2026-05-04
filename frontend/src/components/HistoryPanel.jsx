export default function HistoryPanel({ items, onSelect, onClear }) {
  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 lg:sticky lg:top-6">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-base font-semibold">History</h2>
        {items.length > 0 && (
          <button
            onClick={onClear}
            className="text-xs text-slate-500 hover:text-rose-600 transition"
          >
            Clear
          </button>
        )}
      </div>
      {items.length === 0 ? (
        <p className="text-sm text-slate-500">Generated notes will appear here.</p>
      ) : (
        <ul className="space-y-2 max-h-[60vh] overflow-y-auto pr-1">
          {items.map((item) => (
            <li key={item.id}>
              <button
                onClick={() => onSelect(item)}
                className="w-full text-left rounded-xl border border-slate-200 hover:border-rose-300 hover:bg-rose-50 p-3 transition"
              >
                <div className="text-xs text-slate-500 mb-1">
                  {new Date(item.created_at).toLocaleString()} · {item.format} · {item.language}
                </div>
                <div className="text-sm font-medium truncate">
                  {item.url || item.video_id || 'Untitled'}
                </div>
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
