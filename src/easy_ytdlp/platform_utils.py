import sys
import os
import platform
import shutil
from pathlib import Path

# Enable ANSI on Windows
if sys.platform == "win32":
    import ctypes
    ctypes.windll.kernel32.SetConsoleMode(
        ctypes.windll.kernel32.GetStdHandle(-11), 7
    )

_COLORS = {"red": "31", "green": "32", "yellow": "33", "cyan": "36"}


def get_platform() -> str:
    if sys.platform == "win32":
        return "windows"
    if sys.platform == "darwin":
        return "macos"
    return "linux"


def get_arch() -> str:
    m = platform.machine().lower()
    if m in ("arm64", "aarch64"):
        return "arm64"
    return "x64"


def get_tool_dir() -> Path:
    return Path.home() / ".easy-ytdlp"


def colored(text: str, color: str) -> str:
    code = _COLORS.get(color, "0")
    return f"\033[{code}m{text}\033[0m"


def find_executable(name: str) -> str | None:
    # Check tool dir first (ffmpeg/ffprobe placed there by installer)
    tool_dir = get_tool_dir()
    suffix = ".exe" if get_platform() == "windows" else ""
    candidate = tool_dir / (name + suffix)
    if candidate.is_file():
        return str(candidate)
    return shutil.which(name)
