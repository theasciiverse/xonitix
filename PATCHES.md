# Changes from upstream

This is the Asciiverse packaging of [Xonitix](https://github.com/garu/Xonitix)
by wildgaru (Breno G. de Oliveira, MIT, `LICENSE`), the one-line action
game made for Terminal Jam 2018. Upstream is the `upstream` remote; this
build is upstream's `master` at `8d0eba8` (2021-06-07), whose
`xonitix.cpp` is unchanged since the first upstream source of
2018-11-12 and says `VERSION = "1.1"`. The `asciiverse` branch carries the
changes below, each small enough to offer upstream (UPSTREAM.md).

## The game

Unchanged: the same line, dots, barriers, scoring, levels, texts and
options. The line is the terminal's width less 30 columns (50 cells at
80 columns, 70 at 100), drawn on the line the cursor is on, as upstream
does; `-l` still sets it. The game writes no saves or scores.

## Code (`xonitix.cpp`)

- **The terminal is put back at exit.** Upstream switched off line
  buffering and hid the cursor and never restored either, so the shell
  (or av) was left with no cursor. Echo is now off while playing too
  (keys pressed used to echo onto the line between redraws). The
  original settings and the cursor come back at exit, also on Ctrl+C,
  SIGTERM and SIGHUP. On Windows the cursor comes back and the keys
  pressed during play, which `GetAsyncKeyState()` leaves in the console's
  input buffer, are dropped rather than reaching the shell.
- **Wall clock and sleep between steps.** The loop spun flat out, timing
  itself with `clock()` (processor time) and redrawing many thousands of
  times a second, so it kept a core busy and flooded the terminal. It
  now takes one step every 10 ms (30 ms on Windows), the same step size
  upstream's `clock()` constants meant, measured with `steady_clock`;
  draws once per step and sleeps until the next. Each level starts its
  clock afresh, so the two second pause after a level is not caught up
  in a burst of steps (which happened on Windows, where `clock()` is wall
  time). Measured under tmux, upstream managed about 77 steps a second
  on Linux; this gives the intended 100.
- **Random seed.** `srand(clock())` at start gave nearly the same seed
  every run (`clock()` is close to zero then); the time of day is mixed
  in, so each run starts differently.
- **Session log** behind `XONITIX_LOG`: set it to anything and every key
  as it arrives (raw bytes; the key code on Windows), each level's start
  and end, game over and a snapshot once a second (level, score, hero,
  cells filled, dot positions) are appended to `xonitix.log` in
  `$XDG_STATE_HOME/xonitix` (else `~/.local/state/xonitix`,
  `%LOCALAPPDATA%\xonitix` on Windows). Without it nothing is written.

## Packaging

- `asciiverse/build.sh` (new): upstream's one compile line with `-O2`,
  static on Linux (Alpine, musl) and Windows (MSYS2), plain on macOS.
- `.github/workflows/asciiverse-release.yml` (new): av archives for Linux
  (static, x86-64 and ARM64), macOS (Intel and Apple silicon) and Windows
  (x86-64 and ARM64), plus SHA256SUMS, on a `*-av.*` tag.
- `.github/workflows/codeql-analysis.yml` (removed on this branch only):
  its weekly schedule runs on the default branch, which here is
  `asciiverse`.
- `.gitignore` (new): `build/`.
- `asciiverse/record-preview.sh`, `asciiverse/drive.py` (new): the
  catalog preview, three games played by a script.
- `asciiverse/xonitix.toml`, `asciiverse/xonitix.md`, `asciiverse/xonitix.cast`
  (new): the catalog manifest, store page and preview, as drafts for hub.
- `CLAUDE.md`, `PATCHES.md`, `UPSTREAM.md` (new): notes.
