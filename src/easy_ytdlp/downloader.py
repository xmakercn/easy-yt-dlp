import subprocess
from .platform_utils import find_executable
from .config import get_conf_path, read_proxy

_KEEP_AUDIO_ARGS = ["--extract-audio", "--keep-video", "--audio-format", "m4a"]


def get_ytdlp_cmd() -> str:
    cmd = find_executable("yt-dlp")
    if not cmd:
        raise FileNotFoundError("找不到 yt-dlp，请先运行 install.py")
    return cmd


def _run(url: str, extra: list[str] = [], keep_audio: bool = False) -> None:
    # Load base config + profile config (profile overrides base)
    from .config import get_base_conf_path
    base_conf = str(get_base_conf_path())
    profile_conf = str(get_conf_path())
    
    cmd = [get_ytdlp_cmd(), "--config-locations", base_conf, "--config-locations", profile_conf, "--js-runtimes", "node"]
    cmd += extra
    if keep_audio:
        cmd += _KEEP_AUDIO_ARGS
    cmd += [url]
    subprocess.run(cmd)


def download_single(url: str, keep_audio: bool = False) -> None:
    _run(url, keep_audio=keep_audio)


def download_playlist(url: str, keep_audio: bool = False) -> None:
    _run(url, ["--yes-playlist"], keep_audio=keep_audio)


def download_playlist_range(url: str, start: int, end: int, keep_audio: bool = False) -> None:
    _run(url, ["--yes-playlist", "--playlist-items", f"{start}:{end}"], keep_audio=keep_audio)


def download_playlist_items(url: str, items_str: str, keep_audio: bool = False) -> None:
    _run(url, ["--yes-playlist", "--playlist-items", items_str], keep_audio=keep_audio)


def update_ytdlp() -> None:
    proxy = read_proxy()
    cmd = [get_ytdlp_cmd(), "-U"]
    if proxy:
        cmd += ["--proxy", proxy]
    subprocess.run(cmd)
