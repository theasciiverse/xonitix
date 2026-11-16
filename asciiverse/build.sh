#!/bin/sh
# Builds Xonitix for the Asciiverse catalog. Leaves the binary in
# build/<platform>/xonitix (xonitix.exe on Windows).
#   Linux:   docker run --rm -v "$PWD":/src -w /src alpine:3.22 sh asciiverse/build.sh
#            (fully static against musl; elsewhere static against the host's libc)
#   macOS:   sh asciiverse/build.sh  (the system's libc++)
#   Windows: sh asciiverse/build.sh  in an MSYS2 UCRT64 or CLANGARM64 shell
#            (static, so no MinGW runtime DLLs are needed)
#
# Upstream's README builds with one line, g++ -Wall -g -std=c++11
# xonitix.cpp -o xonitix; this is that line with optimisation and static
# linking.
set -eu
case "$(uname -s)" in
  Linux)  platform=linux ;;
  Darwin) platform=macos ;;
  MINGW*|MSYS*|UCRT*|CLANG*) platform=windows ;;
  *) echo "unknown platform $(uname -s)" >&2; exit 1 ;;
esac

if [ -f /etc/alpine-release ]; then
  apk add --no-cache g++ >/dev/null
fi

cxx=${CXX:-c++}
flags="-Wall -O2 -std=c++11"
mkdir -p "build/$platform"
case $platform in
  linux)
    $cxx $flags xonitix.cpp -o build/linux/xonitix -static
    strip build/linux/xonitix ;;
  macos)
    $cxx $flags xonitix.cpp -o build/macos/xonitix
    strip build/macos/xonitix ;;
  windows)
    $cxx $flags xonitix.cpp -o build/windows/xonitix.exe -static -luser32
    strip build/windows/xonitix.exe ;;
esac
