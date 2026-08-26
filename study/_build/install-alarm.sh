#!/bin/bash
# Install / remove / check the nightly 22:00 review alarm (macOS launchd).
#
#   bash install-alarm.sh            install (or reinstall)
#   bash install-alarm.sh --status   is it loaded? when does it next fire?
#   bash install-alarm.sh --test     fire it right now
#   bash install-alarm.sh --remove   uninstall completely
#   bash install-alarm.sh --time 21 30    install at a different time

set -uo pipefail

LABEL="com.mlnotes.review"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE="$HERE/review-alarm.sh"

# macOS protects ~/Desktop, ~/Documents and ~/Downloads (TCC). A LaunchAgent
# running from there is refused with "Operation not permitted" — exit code 126 —
# even though the same script runs fine from a terminal. So install a copy
# somewhere launchd is allowed to read, and point the agent at that.
INSTALL_DIR="$HOME/Library/Application Support/mlnotes"
SCRIPT="$INSTALL_DIR/review-alarm.sh"
LOG="$HOME/Library/Logs/mlnotes-review.log"
HOUR=22
MINUTE=0

case "${1:-}" in
  --remove)
    launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || launchctl unload "$PLIST" 2>/dev/null
    rm -f "$PLIST"
  rm -rf "$INSTALL_DIR"
    echo "removed. the alarm will not fire again."
    echo "(the log at $LOG is left in place; delete it if you want)"
    exit 0
    ;;
  --status)
    if launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1; then
      echo "loaded ✓"
      launchctl print "gui/$(id -u)/$LABEL" | grep -E 'state|runs|last exit' | sed 's/^/  /'
    else
      echo "NOT loaded ✗   — run:  bash $0"
    fi
    echo
    echo "plist: $PLIST"
    [ -f "$LOG" ] && { echo "last 5 log lines:"; tail -5 "$LOG" | sed 's/^/  /'; }
    exit 0
    ;;
  --test)
    echo "firing the alarm now…"
    bash "$SOURCE"
    echo "done. if you heard nothing, check the volume and $LOG"
    exit 0
    ;;
  --time)
    HOUR="${2:-22}"; MINUTE="${3:-0}"
    ;;
esac

mkdir -p "$INSTALL_DIR"
cp "$SOURCE" "$SCRIPT"
chmod +x "$SOURCE" "$SCRIPT"
mkdir -p "$HOME/Library/LaunchAgents"

cat > "$PLIST" <<PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$LABEL</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$SCRIPT</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>$HOUR</integer>
        <key>Minute</key>
        <integer>$MINUTE</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$LOG</string>
    <key>StandardErrorPath</key>
    <string>$LOG</string>
    <key>ProcessType</key>
    <string>Interactive</string>
</dict>
</plist>
PLISTEOF

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST" 2>/dev/null \
  || launchctl load "$PLIST" 2>/dev/null

printf 'installed ✓  the alarm will sound every day at %02d:%02d\n' "$HOUR" "$MINUTE"
echo
echo "  test it now      bash $0 --test"
echo "  check it         bash $0 --status"
echo "  change the time  bash $0 --time 21 30"
echo "  remove it        bash $0 --remove"
echo
echo "note: if the Mac is asleep at that moment, launchd fires the job when it next wakes."
