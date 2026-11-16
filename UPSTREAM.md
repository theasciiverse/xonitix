# Changes for upstream

Hi! These are the small changes the Asciiverse build of Xonitix carries,
written so each can be taken on its own or left out. PATCHES.md has the
full list with the packaging files.

## 1. Put the terminal back at exit

`DetectKeyPress()` turns off `ICANON` and `HideCursor()` hides the
cursor, but neither is undone, so after the game the shell has no
cursor. The change keeps the original `termios`, also turns off `ECHO`
while playing (arrow keys otherwise echo `^[[C` onto the line between
redraws), and restores both plus the cursor from an `atexit()` handler
and from SIGINT, SIGTERM and SIGHUP handlers (which use only
`tcsetattr()` and `write()`). On Windows the cursor is shown again and
`FlushConsoleInputBuffer()` drops the keys `GetAsyncKeyState()` left in
the console's input buffer, so they do not spill into the shell.

## 2. Wall clock and a sleep in the main loop

The loop runs flat out and times itself with `std::clock()`, which is
processor time on Linux and macOS, so the game uses a full core and
redraws the line many thousands of times a second. The change keeps
the same step (10 ms; 30 ms on Windows, as `DELTA_PER_UPDATE` meant
with each platform's `CLOCKS_PER_SEC`), measures it with
`std::chrono::steady_clock`, draws and flushes once per step and
`sleep_until()` the next step. The clock restarts with each level, so
the two second pause after a level does not turn into a burst of steps
on Windows, where `clock()` is wall time.

## 3. A different seed each run

`srand(t_previous)` seeds with `clock()` right at start, which is close
to the same small number every time. `srand(std::clock() ^
std::time(nullptr))` makes each run different.

## 4. An optional session log

With `XONITIX_LOG` set, keys, levels, game over and a once a second
snapshot go to `xonitix.log` in `$XDG_STATE_HOME/xonitix` (or
`~/.local/state/xonitix`, `%LOCALAPPDATA%\xonitix`). Useful for bug
reports; without the variable nothing changes. Easy to leave out.

Thank you for Xonitix!
