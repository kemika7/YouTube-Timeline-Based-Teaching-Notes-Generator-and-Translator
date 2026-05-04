#!/usr/bin/env bash
# Run backend (uvicorn) and frontend (vite) together. Ctrl+C stops both.
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

cleanup() {
  echo
  echo "Shutting down..."
  kill 0 2>/dev/null
}
trap cleanup EXIT INT TERM

# --- Backend ---
(
  cd "$ROOT/backend"
  if [ ! -d ".venv" ]; then
    echo "[backend] creating .venv (first run)..."
    python3.12 -m venv .venv
  fi
  # shellcheck disable=SC1091
  source .venv/bin/activate
  if [ ! -f ".venv/.deps_installed" ] || [ requirements.txt -nt .venv/.deps_installed ]; then
    echo "[backend] installing/updating dependencies..."
    pip install --upgrade -r requirements.txt
    touch .venv/.deps_installed
  fi
  echo "[backend] starting uvicorn on http://localhost:8000"
  exec python -m uvicorn app:app --reload --port 8000
) &

# --- Frontend ---
(
  cd "$ROOT/frontend"
  if [ ! -d "node_modules" ]; then
    echo "[frontend] running npm install (first run)..."
    npm install
  fi
  echo "[frontend] starting vite on http://localhost:5173"
  exec npm run dev
) &

wait
