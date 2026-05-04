import axios from 'axios'

const API = axios.create({
  baseURL: '/api',
  timeout: 180000,
})

export async function generateNotes({ url, language, format }) {
  const { data } = await API.post('/generate-notes', { url, language, format })
  return data
}

export async function extractTranscript({ url, language }) {
  const { data } = await API.post('/extract-transcript', { url, language })
  return data
}

export async function translate({ text, target_language, source_language }) {
  const { data } = await API.post('/translate', { text, target_language, source_language })
  return data
}

export async function getHistory() {
  const { data } = await API.get('/history')
  return data.items
}

export async function clearHistory() {
  const { data } = await API.delete('/history')
  return data
}

export async function getLanguages() {
  const { data } = await API.get('/languages')
  return data.languages
}
