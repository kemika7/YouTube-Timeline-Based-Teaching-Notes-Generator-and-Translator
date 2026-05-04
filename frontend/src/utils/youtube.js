const YT_REGEX =
  /(?:youtube\.com\/(?:[^/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/

export function extractVideoId(url) {
  if (!url) return null
  const m = String(url).match(YT_REGEX)
  return m ? m[1] : null
}

export function isValidYouTubeUrl(url) {
  return !!extractVideoId(url)
}
