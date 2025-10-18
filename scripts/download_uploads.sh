#!/usr/bin/env bash
set -euo pipefail

out="assets/uploads_urls.txt"
max=15
count=0
mkdir -p assets/img

if [ ! -f "$out" ]; then
  echo "URL list $out not found."
  exit 0
fi

while IFS= read -r url || [ -n "$url" ]; do
  # normalize
  url="${url%%$'\r'}"
  [ -z "$url" ] && continue
  case "$url" in http*) ;; *) continue ;; esac
  file=$(basename "${url%%\?*}")
  [ -z "$file" ] && continue
  if [ -f "assets/img/$file" ]; then
    echo "SKIP exists: $file"
    continue
  fi
  # HEAD to check size (timeout 10s)
  size=$(curl -sI --max-time 10 "$url" | tr -d '\r' | awk -F': ' '/[Cc]ontent-[Ll]ength/{print $2}' | tail -n1 || true)
  if [ -n "$size" ]; then
    if [ "$size" -gt $((10*1024*1024)) ]; then
      echo "SKIP too large (>10MB): $file ($size bytes)"
      continue
    fi
  fi
  echo "Downloading: $file"
  if curl -fSL --connect-timeout 10 --max-time 120 --limit-rate 300k -o "assets/img/$file" "$url"; then
    echo "SAVED: assets/img/$file"
    count=$((count+1))
  else
    echo "ERROR downloading: $url"
    rm -f "assets/img/$file" || true
  fi
  sleep 0.6
  if [ "$count" -ge "$max" ]; then break; fi
done < "$out"

echo "Downloaded this run: $count"

echo
ls -l assets/img | tail -n 50
