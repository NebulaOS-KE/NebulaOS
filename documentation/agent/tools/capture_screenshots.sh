#!/usr/bin/env bash
#
# Capture real NebulaScreen screenshots, headless, and record the commit.
#
# The application has a built-in screenshot tour: GUPPY_SIM_SHOTS=<dir> walks
# every page and state, writes a binary PPM of each, and exits. It captures a
# copy of the LVGL framebuffer rather than a window, so no display server is
# needed - SDL_VIDEODRIVER=offscreen is enough. The tour also suppresses the
# normal simulator demo data, prompts and notifications, so the captures are
# clean and reproducible.
#
# This is real UI rendered by the real application at a known commit. It is not
# hardware: the machine.nebulaos.* panels need a live NebulaOS printer, so those
# screens show errors or empty values here and must not be published as if they
# were a working printer.
#
# Usage:  capture_screenshots.sh <screen-checkout> <output-dir>
set -euo pipefail

SRC=${1:?usage: capture_screenshots.sh <screen-checkout> <output-dir>}
OUT=${2:?usage: capture_screenshots.sh <screen-checkout> <output-dir>}
SRC=$(cd "$SRC" && pwd)
COMMIT=$(git -C "$SRC" rev-parse HEAD)
WORK="${TMPDIR:-/tmp}/nebulascreen-shots"

echo "screen checkout : $SRC"
echo "commit          : $COMMIT"

# --- build (once) ---------------------------------------------------------
# Two things the documented build instructions do not mention and that both
# stop the build dead in this environment:
#
#  1. The default LDFLAGS contain -static. There is no static SDL2 here, and
#     /usr/lib/libSDL2-2.0.so.0 is 32-bit i386 so it cannot satisfy a 64-bit
#     link anyway. A 64-bit SDL2 does exist in /lib64, and a non-static link
#     finds it. So LDFLAGS is overridden below with -static removed.
#  2. The submodule patches must be applied first, or spdlog/fmt fails.
if [ ! -x "$SRC/build/bin/nebulascreen" ]; then
  ( cd "$SRC/spdlog" && git apply --check ../patches/0002-spdlog_fmt_initializer_list.patch 2>/dev/null \
      && git apply ../patches/0002-spdlog_fmt_initializer_list.patch || true )
  ( cd "$SRC/lvgl" && git apply --check ../patches/0003-lvgl-dpi-text-scale.patch 2>/dev/null \
      && git apply ../patches/0003-lvgl-dpi-text-scale.patch || true )
  make -C "$SRC" libhv.a
  make -C "$SRC" libspdlog.a
  make -C "$SRC" GUPPY_SMALL_SCREEN=1 -j"$(nproc)" \
    LDFLAGS="-lm -Llibhv/lib -Lspdlog/build -l:libhv.a -latomic -lpthread -lstdc++fs -l:libspdlog.a"
fi

# --- config ---------------------------------------------------------------
# The app aborts at startup if the directory holding log_path does not exist
# (spdlog throws). Create it before the first run.
mkdir -p "$WORK/thumbs" "$OUT"
cat > "$SRC/build/bin/nebulascreen.json" <<JSON
{
  "log_path": "$WORK/nebulascreen.log",
  "thumbnail_path": "$WORK/thumbs",
  "default_printer": "sim",
  "printers": { "sim": { "moonraker_host": "127.0.0.1", "moonraker_port": 7125,
                         "moonraker_api_key": false } }
}
JSON
cp -r "$SRC/themes" "$SRC/build/bin/" 2>/dev/null || true

# --- capture --------------------------------------------------------------
PPM="$WORK/ppm"
rm -rf "$PPM"; mkdir -p "$PPM"
( cd "$SRC/build/bin" && SDL_VIDEODRIVER=offscreen GUPPY_SIM_SHOTS="$PPM" ./nebulascreen >"$WORK/tour.log" 2>&1 )

# --- convert and stamp ----------------------------------------------------
python3 - "$PPM" "$OUT" "$COMMIT" <<'PY'
import sys, os, glob, json
from PIL import Image
ppm, out, commit = sys.argv[1], sys.argv[2], sys.argv[3]
rows = []
for f in sorted(glob.glob(os.path.join(ppm, "*.ppm"))):
    im = Image.open(f)
    name = os.path.basename(f)[:-4] + ".png"
    im.save(os.path.join(out, name), "PNG", optimize=True)
    rows.append({"image": name, "size": list(im.size)})
meta = {"commit": commit, "count": len(rows),
        "source": "NebulaScreen SDL simulator, GUPPY_SIM_SHOTS tour",
        "resolution": "480x272 (GUPPY_SMALL_SCREEN=1, the KE's real panel)",
        "caveat": ("real UI from the real application at this commit; not hardware. "
                   "machine.nebulaos.* panels need a live printer and are not "
                   "truthful here."),
        "images": rows}
with open(os.path.join(out, "screenshots.json"), "w") as fh:
    json.dump(meta, fh, indent=2, sort_keys=True)
print(f"{len(rows)} screenshots -> {out} (commit {commit[:7]})")
PY
