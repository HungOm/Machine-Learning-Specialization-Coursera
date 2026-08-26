#!/bin/bash
# Nightly review alarm for the ML study notes.
# Run by launchd at 22:00; also runnable by hand to test.
#
#   MLNOTES_SOUND    path to an .aiff            (default: Submarine)
#   MLNOTES_REPEATS  how many times to play it   (default: 3)
#   MLNOTES_OPEN     1 = also open review.html   (default: 0)

set -uo pipefail

SOUND="${MLNOTES_SOUND:-/System/Library/Sounds/Submarine.aiff}"
REPEATS="${MLNOTES_REPEATS:-3}"
OPEN_PAGE="${MLNOTES_OPEN:-0}"

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REVIEW_PAGE="$(cd "$HERE/.." && pwd)/review.html"
LOG="$HOME/Library/Logs/mlnotes-review.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] alarm fired" >> "$LOG"

# --- the actual computer sound -------------------------------------------
# afplay blocks until the clip finishes, so repeats space themselves out.
if [ -f "$SOUND" ]; then
  for _ in $(seq 1 "$REPEATS"); do
    afplay "$SOUND" 2>>"$LOG"
  done
else
  echo "  sound not found: $SOUND — falling back to the terminal bell" >> "$LOG"
  printf '\a\a\a'
fi

# --- a banner you can actually see ----------------------------------------
osascript -e 'display notification "Time for your spaced-repetition review — open study/review.html" with title "ML study review" subtitle "10 pm" sound name "Submarine"' 2>>"$LOG" || true

# --- optionally open the page ---------------------------------------------
if [ "$OPEN_PAGE" = "1" ] && [ -f "$REVIEW_PAGE" ]; then
  open "$REVIEW_PAGE" 2>>"$LOG" || true
  echo "  opened $REVIEW_PAGE" >> "$LOG"
fi

echo "  done" >> "$LOG"
