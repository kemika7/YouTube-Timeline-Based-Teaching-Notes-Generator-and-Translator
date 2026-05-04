export default function ErrorMessage({ message }) {
  if (!message) return null
  return (
    <div className="rounded-xl bg-rose-50 border border-rose-200 text-rose-700 px-4 py-3 text-sm">
      {message}
    </div>
  )
}
