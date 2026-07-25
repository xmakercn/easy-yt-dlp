import re
from pathlib import Path
from .platform_utils import get_tool_dir

DEFAULT_PROFILE_ID = "sys_default_1080P-mp4-lean"
_ACTIVE_FILE = "active_profile"


def _profiles_dir() -> Path:
    return get_tool_dir() / "profiles"


def _active_file() -> Path:
    return get_tool_dir() / _ACTIVE_FILE


# ── active profile ────────────────────────────────────────────────────────────

def get_active_profile_id() -> str:
    f = _active_file()
    if f.exists():
        pid = f.read_text(encoding="utf-8").strip()
        if pid:
            return pid
    return DEFAULT_PROFILE_ID


def set_active_profile_id(profile_id: str) -> None:
    _active_file().write_text(profile_id, encoding="utf-8")


# ── profile paths ─────────────────────────────────────────────────────────────

def get_base_conf_path() -> Path:
    """Get path to base config file."""
    return get_tool_dir() / "config" / "base.conf"


def get_conf_path(profile_id: str | None = None) -> Path:
    pid = profile_id or get_active_profile_id()
    return _profiles_dir() / pid / "yt-dlp.conf"


def get_meta_path(profile_id: str | None = None) -> Path:
    pid = profile_id or get_active_profile_id()
    return _profiles_dir() / pid / ".meta"


# ── meta read/write ───────────────────────────────────────────────────────────

def read_meta(profile_id: str | None = None) -> dict[str, str]:
    path = get_meta_path(profile_id)
    if not path.exists():
        return {}
    meta = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            k, _, v = line.partition("=")
            meta[k.strip()] = v.strip()
    return meta


def write_meta(name: str, desc: str, profile_id: str | None = None) -> None:
    path = get_meta_path(profile_id)
    path.write_text(f"name={name}\ndesc={desc}\n", encoding="utf-8")


# ── list profiles ─────────────────────────────────────────────────────────────

def list_profiles() -> list[dict]:
    """Return list of {id, name, desc} sorted by id."""
    result = []
    pd = _profiles_dir()
    if not pd.exists():
        return result
    for d in sorted(pd.iterdir()):
        if d.is_dir():
            meta = read_meta(d.name)
            result.append({
                "id": d.name,
                "name": meta.get("name", d.name),
                "desc": meta.get("desc", ""),
            })
    return result


# ── conf read/write ───────────────────────────────────────────────────────────

def read_proxy(profile_id: str | None = None) -> str:
    """Read proxy from base config."""
    base_conf = get_base_conf_path()
    if not base_conf.exists():
        return ""
    for line in base_conf.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*--proxy[=\s]+(\S+)", line)
        if m:
            return m.group(1)
    return ""


def read_output_path() -> str:
    """Read output path from base config."""
    base_conf = get_base_conf_path()
    if not base_conf.exists():
        return ""
    for line in base_conf.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*--output[=\s]+['\"]?([^'\"]+)/", line)
        if m:
            return m.group(1)
    return ""


def read_browser() -> str:
    """Read browser from base config."""
    base_conf = get_base_conf_path()
    if not base_conf.exists():
        return ""
    for line in base_conf.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*--cookies-from-browser[=\s]+(\S+)", line)
        if m:
            return m.group(1)
    return ""


def update_output_path(path: str, profile_id: str | None = None) -> None:
    """Update output path in base config."""
    base_conf = get_base_conf_path()
    if not base_conf.exists():
        return
    content = base_conf.read_text(encoding="utf-8")
    # Use forward slashes for cross-platform compatibility
    normalized_path = path.replace("\\", "/")
    new_line = f"--output='{normalized_path}/%(title)s.%(ext)s'"
    content = re.sub(r"(?m)^--output=.*", new_line, content)
    base_conf.write_text(content, encoding="utf-8")


def generate_default_conf(
    video_path: str,
    ffmpeg_dir: str,
    proxy: str = "127.0.0.1:10808",
    browser: str = "firefox",
    profile_id: str = DEFAULT_PROFILE_ID,
) -> None:
    conf_path = get_conf_path(profile_id)
    conf_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["#Use a proxy"]
    if proxy:
        lines.append(f"--proxy={proxy}")
    lines += [
        "#Download format: 1080P MP4 -> best merged format -> best available",
        '--format "b[ext=mp4][height=1080]/bv[ext=mp4][height=1080]+ba[ext=m4a]/bv*+ba/b"',
    ]
    if browser:
        lines += [
            f"#Use {browser} browser cookies",
            f"--cookies-from-browser={browser}",
        ]
    lines += [
        "#Disable playlist download by default",
        "--no-playlist",
        "#Output file directory",
        f"--output='{video_path}/%(title)s.%(ext)s'",
    ]
    if ffmpeg_dir:
        lines += ["#Path to ffmpeg", f"--ffmpeg-location='{ffmpeg_dir}'"]
    conf_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Write default meta
    write_meta(
        name=DEFAULT_PROFILE_ID,
        desc="优先下载1080P视频，不保留音频，mp4格式",
        profile_id=profile_id,
    )
    # Set as active
    set_active_profile_id(profile_id)
