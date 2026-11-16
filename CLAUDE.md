# Xonitix (Asciiverse packaging)

wildgaru's Xonitix (Breno G. de Oliveira; C++, no libraries, MIT),
packaged for the Asciiverse catalog (id `xonitix`, kind `game`, genre
`arcade`). Not our code: the game stays as its author made it; list
every change in PATCHES.md and keep each one offerable upstream
(UPSTREAM.md).

- `upstream` is github.com/garu/Xonitix (branch `master`); ours is branch
  `asciiverse`, `origin` github.com/theasciiverse/xonitix (private).
  `xonitix.cpp` has CRLF line endings; keep them.
- Build: `sh asciiverse/build.sh` (Linux static in alpine:3.22 under
  docker in CI; locally static against the host's glibc). Binary in
  `build/<platform>/xonitix`.
- Release: tag `v<upstream VERSION>-av.<n>` (first `v1.1-av.1`) and push
  it; `.github/workflows/asciiverse-release.yml` builds Linux, macOS and
  Windows.
- No saves or scores. The only file it writes is the session log, with
  `XONITIX_LOG` set, in `$XDG_STATE_HOME/xonitix`. Scripted runs always
  set a scratch `XDG_STATE_HOME` and `HOME` in the same command, under
  `systemd-run --user --scope -p MemoryMax=4G`.
- The game is one line printed where the cursor is, terminal width less
  30 cells (50 at 80 columns, 70 at 100).
- Preview: `asciiverse/record-preview.sh build/linux/xonitix` (three
  games played by `asciiverse/drive.py`; random each time).
- Catalog drafts: `asciiverse/xonitix.toml` and `.md`; hub pushes are done
  from beast.
