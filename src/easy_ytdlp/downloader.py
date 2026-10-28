import sys
import subprocess
from pathlib import Path
from .platform_utils import find_executable, get_tool_dir
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


def is_pip_ytdlp(cmd: str | None = None) -> bool:
    """Determine whether yt-dlp is installed as a Python package via pip.

    According to official yt-dlp update policy:
    - Standalone binary builds (pyinstaller/exe) can self-update via 'yt-dlp -U'.
    - Pip/wheel packages cannot self-update via '-U' and must be updated via pip.
    """
    tool_dir = get_tool_dir()
    suffix = ".exe" if sys.platform == "win32" else ""
    local_binary = tool_dir / ("yt-dlp" + suffix)

    # Standalone executable placed in tool dir (~/.easy-ytdlp/)
    if local_binary.is_file() and cmd and Path(cmd).resolve() == local_binary.resolve():
        return False

    try:
        import yt_dlp.version
        if getattr(yt_dlp.version, "VARIANT", None) == "pip":
            return True
        if "pip" in getattr(yt_dlp.version, "UPDATE_HINT", "").lower():
            return True
    except Exception:
        pass

    if cmd:
        cmd_path = Path(cmd).resolve()
        py_prefix = Path(sys.prefix).resolve()
        try:
            if cmd_path.is_relative_to(py_prefix):
                return True
        except (AttributeError, ValueError):
            pass

    return False


def update_ytdlp() -> bool:
    proxy = read_proxy()
    cmd = get_ytdlp_cmd()

    if is_pip_ytdlp(cmd):
        pip_cmd = [sys.executable, "-m", "pip", "install", "-U", "yt-dlp[default,curl-cffi]"]
        if proxy:
            pip_cmd += ["--proxy", proxy]
        res = subprocess.run(pip_cmd)
        return res.returncode == 0

    # Standalone binary release update
    update_cmd = [cmd, "-U"]
    if proxy:
        update_cmd += ["--proxy", proxy]
    res = subprocess.run(update_cmd)
    if res.returncode == 0:
        return True

    # Fallback: if standalone update failed, attempt update via pip
    pip_cmd = [sys.executable, "-m", "pip", "install", "-U", "yt-dlp[default,curl-cffi]"]
    if proxy:
        pip_cmd += ["--proxy", proxy]
    fallback_res = subprocess.run(pip_cmd)
    return fallback_res.returncode == 0
