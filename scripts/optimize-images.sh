#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

MAX_DIM_STATIC="${MAX_DIM_STATIC:-4600}"
QUALITY_STATIC="${QUALITY_STATIC:-92}"
MAX_DIM_PROCESSED="${MAX_DIM_PROCESSED:-3000}"
QUALITY_PROCESSED="${QUALITY_PROCESSED:-90}"
MIN_BYTES="${MIN_BYTES:-800000}"

optimize_one() {
  local file="$1"
  local max_dim="$2"
  local quality="$3"

  local size_before
  size_before="$(stat -f '%z' "$file")"
  if (( size_before < MIN_BYTES )); then
    return
  fi

  local lower
  lower="$(printf '%s' "$file" | tr '[:upper:]' '[:lower:]')"
  local tmp
  if [[ "$lower" == *.jpg || "$lower" == *.jpeg ]]; then
    tmp="${file}.opt.jpg"
    /usr/bin/sips -s format jpeg -s formatOptions "$quality" --resampleHeightWidthMax "$max_dim" "$file" --out "$tmp" >/dev/null
  elif [[ "$lower" == *.png ]]; then
    tmp="${file}.opt.png"
    /usr/bin/sips --resampleHeightWidthMax "$max_dim" "$file" --out "$tmp" >/dev/null
  else
    return
  fi

  local size_after
  size_after="$(stat -f '%z' "$tmp")"
  if (( size_after < size_before )); then
    mv "$tmp" "$file"
    local before_mb after_mb
    before_mb="$(perl -e "printf('%.2f', $size_before/1048576)")"
    after_mb="$(perl -e "printf('%.2f', $size_after/1048576)")"
    printf 'optimized\t%s\t%sMB -> %sMB\n' "$file" "$before_mb" "$after_mb"
  else
    rm -f "$tmp"
  fi
}

echo "Optimizing static/images ..."
while IFS= read -r -d '' file; do
  optimize_one "$file" "$MAX_DIM_STATIC" "$QUALITY_STATIC"
done < <(find "$ROOT/static/images" -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \) -print0)

echo "Optimizing static/processed/project ..."
while IFS= read -r -d '' file; do
  optimize_one "$file" "$MAX_DIM_PROCESSED" "$QUALITY_PROCESSED"
done < <(find "$ROOT/static/processed/project" -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \) -print0)

echo "Done."
