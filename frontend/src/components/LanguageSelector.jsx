export default function LanguageSelector({ value, onChange, options, disabled }) {
  return (
    <div>
      <label className="block text-sm font-medium text-slate-700 mb-1.5">Language</label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-rose-500 disabled:bg-slate-50"
      >
        {options.map((opt) => (
          <option key={opt.code} value={opt.code}>
            {opt.name}
          </option>
        ))}
      </select>
    </div>
  )
}
