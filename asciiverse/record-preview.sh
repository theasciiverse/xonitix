#!/bin/sh
# Records the catalog preview, asciiverse/xonitix.cast (hub/RECORDING.md):
# three games in a row at 100x30, as they would stack up in a shell,
# each played by asciiverse/drive.py until the dots win or it quits with
# q. asciinema records a tmux pane (own socket, no status line, no user
# config) that drive.py reads and plays into. Needs asciinema 3 and tmux.
#   asciiverse/record-preview.sh build/linux/xonitix
set -eu
binary=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
here=$(cd "$(dirname "$0")" && pwd)
out=$here/xonitix.cast
home=$(mktemp -d)
trap 'tmux -L avrec kill-server 2>/dev/null; rm -rf "$home"' EXIT
mkdir "$home/bin" && cp "$binary" "$home/bin/xonitix"
cd "$home"  # nothing in the recording names a local path
export HOME="$home" XDG_STATE_HOME="$home/state" PATH="$home/bin:$PATH" \
  USER=player LOGNAME=player TERM=xterm-256color COLORTERM=truecolor LANG=C.UTF-8
tmux -L avrec -f /dev/null new-session -d -s rec -x 100 -y 30 \
  "xonitix; xonitix; xonitix" \; set -g status off
python3 -I "$here/drive.py" avrec rec &
drive=$!
asciinema rec --headless --overwrite -q \
  --window-size 100x30 --idle-time-limit 2 \
  --capture-env "TERM,COLORTERM,LANG" --title "Xonitix" \
  --command "tmux -L avrec attach -t rec" "$out"
wait "$drive"
