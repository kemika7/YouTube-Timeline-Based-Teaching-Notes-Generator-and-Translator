export default function FormatSelector({ value, onChange, options, disabled }) {
  return (
    <div>
      <label className="block text-sm font-medium text-slate-700 mb-1.5">Output Format</label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-rose-500 disabled:bg-slate-50"
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  )
}
