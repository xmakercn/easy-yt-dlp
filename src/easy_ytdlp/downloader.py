import subprocess
from .platform_utils import find_executable
from .config import get_conf_path, read_output_path, read_proxy

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


def _playlist_download_args() -> list[str]:
    """播放列表下载（菜单 2-4）共用：在下载目录下自动新建一个以播放列表标题命名的
    子文件夹，本次下载的所有文件都放入该文件夹（重复下载同一列表时自动复用已有文件夹）。
    实现方式：仅在本条命令上通过命令行参数临时覆盖 --output，
    不影响其他 URL 的下载，也不写入任何配置文件。
    若无法从配置解析出下载根目录，则回退为默认输出（不建子文件夹）。"""
    args = ["--yes-playlist"]
    root = read_output_path().replace("\\", "/").rstrip("/")
    if root:
        args += ["--output", f"{root}/%(playlist_title)s/%(title)s.%(ext)s"]
    return args


def download_playlist(url: str, keep_audio: bool = False) -> None:
    _run(url, _playlist_download_args(), keep_audio=keep_audio)


def download_playlist_range(url: str, start: int, end: int, keep_audio: bool = False) -> None:
    _run(url, _playlist_download_args() + ["--playlist-items", f"{start}:{end}"], keep_audio=keep_audio)


def download_playlist_items(url: str, items_str: str, keep_audio: bool = False) -> None:
    _run(url, _playlist_download_args() + ["--playlist-items", items_str], keep_audio=keep_audio)


def update_ytdlp() -> None:
    proxy = read_proxy()
    cmd = [get_ytdlp_cmd(), "-U"]
    if proxy:
        cmd += ["--proxy", proxy]
    subprocess.run(cmd)
