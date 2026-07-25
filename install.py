#!/usr/bin/env python3
"""Easy yt-dlp installer - uses only Python standard library."""
import locale
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path
from urllib.request import urlretrieve

# ── i18n ──────────────────────────────────────────────────────────────────────
def _detect_language():
    """Detect system language: zh_CN or en_US."""
    try:
        lang = locale.getlocale()[0] or os.environ.get("LANG", "")
        if lang.lower().startswith(("zh", "chinese")):
            return "zh_CN"
    except:
        pass
    return "en_US"

_LANG = _detect_language()
_TRANSLATIONS = {
    "zh_CN": {
        "python_version_error": "Python 3.10+ 必须，当前版本 {version}",
        "node_installed": "Node.js 已安装",
        "node_not_found": "未检测到 Node.js（YouTube 下载需要）",
        "node_install_hint": "请手动安装：https://nodejs.org/",
        "browser_firefox": "浏览器：firefox",
        "firefox_not_found": "未检测到 Firefox",
        "firefox_recommended": "Firefox 是推荐的浏览器，原因如下：",
        "firefox_reason_1": "· YouTube 等平台对 Chrome/Edge 的 cookie 提取有限制，可能导致下载失败",
        "firefox_reason_2": "· Firefox 的 cookie 格式与 yt-dlp 兼容性最佳",
        "firefox_download": "Firefox 下载地址：https://www.mozilla.org/firefox/",
        "firefox_install_prompt": "是否已安装或计划安装 Firefox？[Y/n]: ",
        "firefox_install_later": "请安装 Firefox 后重新运行安装脚本，以获得最佳体验。",
        "firefox_continue": "继续安装，将使用 Firefox 作为默认浏览器配置（安装后生效）。",
        "firefox_skipped": "已跳过 Firefox。注意：",
        "firefox_skip_warn_1": "· 使用其他浏览器时，YouTube 会员内容、需登录内容可能无法下载",
        "firefox_skip_warn_2": "· 若遇到「Sign in to confirm you're not a bot」等错误，请改用 Firefox",
        "browser_detected": "检测到已安装的浏览器：{browser}，将使用其进行配置",
        "no_browser_detected": "未检测到任何已安装的浏览器",
        "manual_browser_prompt": "是否手动指定浏览器路径？[y/N]: ",
        "supported_browsers": "支持的浏览器：firefox, chrome, edge, brave",
        "browser_name_prompt": "浏览器名称: ",
        "browser_path_prompt": "浏览器安装路径（可执行文件或目录）: ",
        "browser_verified": "已验证浏览器：{browser}",
        "browser_path_invalid": "路径无效或浏览器不匹配，将跳过 cookie 配置",
        "installing_ytdlp": "正在安装 yt-dlp...",
        "ytdlp_installed": "yt-dlp 安装完成",
        "ytdlp_install_failed": "yt-dlp 安装失败，请检查 pip 是否可用",
        "downloading": "下载中... {pct}%",
        "ffmpeg_exists": "安装目录已有 ffmpeg，跳过下载",
        "ffmpeg_system": "系统已有 ffmpeg，跳过下载",
        "ffmpeg_downloading": "正在下载 ffmpeg...",
        "ffmpeg_extracting": "正在解压 ffmpeg...",
        "ffmpeg_installed": "ffmpeg 安装完成",
        "ffmpeg_not_supported": "当前平台不支持自动安装 ffmpeg，请手动安装",
        "ffmpeg_install_hint": "安装指南：https://github.com/yt-dlp/FFmpeg-Builds",
        "proxy_prompt": "选择代理设置：",
        "proxy_none": "[1] 不使用代理",
        "proxy_default": "[2] 使用默认代理 (127.0.0.1:10808)",
        "proxy_custom": "[3] 自定义代理",
        "proxy_choice": "请选择 [1-3]: ",
        "proxy_custom_prompt": "请输入代理地址（格式：host:port）: ",
        "proxy_set": "代理设置：{proxy}",
        "proxy_disabled": "代理已禁用",
        "output_path_prompt": "视频保存路径",
        "profile_created": "Profile 已创建：{profile}",
        "active_profile_set": "当前 Profile：{profile}",
        "desktop_shortcut_created": "桌面快捷方式已创建",
        "desktop_shortcut_failed": "桌面快捷方式创建失败",
        "env_var_set": "环境变量已设置：EASY_YTDLP_HOME",
        "path_updated": "PATH 已更新",
        "install_complete": "安装完成！",
        "install_complete_hint": "运行 'easy-ytdlp' 启动工具",
        "install_complete_hint_windows": "请重启终端或重新登录以使环境变量生效",
        "existing_install_found": "检测到已有安装：{path}",
        "existing_install_prompt": "是否使用现有安装？[Y/n]: ",
        "existing_install_use": "使用现有安装",
        "existing_install_skip": "跳过，将创建新安装",
        "uninstall_confirm": "确认卸载 Easy yt-dlp？[y/N]: ",
        "uninstalling": "正在卸载...",
        "uninstall_complete": "卸载完成",
        "uninstall_cancelled": "已取消卸载",
        "not_installed": "未检测到安装",
        "updating_ytdlp": "正在更新 yt-dlp...",
        "ytdlp_updated": "yt-dlp 已更新",
        "ytdlp_update_failed": "yt-dlp 更新失败",
        "menu_title": "Easy yt-dlp 安装工具",
        "menu_install": "[1] 安装",
        "menu_uninstall": "[2] 卸载",
        "menu_exit": "[3] 退出",
        "menu_prompt": "请选择 [1-3]: ",
        "invalid_choice": "无效选择",
        "base_config_created": "根配置已生成：{path}",
        "default_profile_created": "默认 Profile 已生成：{path}",
        "profile_desc": "优先下载1080P视频，不保留音频，mp4格式",
        "proxy_choice_prompt": "请选择 [1-3]: ",
        "proxy_address_prompt": "请输入代理地址（格式：host:port）: ",
        "video_path_prompt": "视频保存路径",
        "shortcut_creating": "正在创建桌面快捷方式...",
        "env_setting": "正在设置环境变量...",
        "install_success": "安装完成！",
        "install_hint_run": "运行 'easy-ytdlp' 启动工具",
        "install_hint_restart": "请重启终端或重新登录以使环境变量生效",
        "existing_found": "检测到已有安装：{path}",
        "use_existing_prompt": "是否使用现有安装？[Y/n]: ",
        "use_existing": "使用现有安装",
        "create_new": "创建新安装",
        "uninstall_prompt": "确认卸载 Easy yt-dlp？[y/N]: ",
        "uninstall_progress": "正在卸载...",
        "uninstall_done": "卸载完成",
        "uninstall_cancel": "已取消卸载",
        "not_installed_msg": "未检测到 Easy yt-dlp 安装",
        "update_ytdlp_progress": "正在更新 yt-dlp...",
        "update_ytdlp_done": "yt-dlp 已更新到最新版本",
        "update_ytdlp_fail": "yt-dlp 更新失败",
    },
    "en_US": {
        "python_version_error": "Python 3.10+ required, current version {version}",
        "node_installed": "Node.js installed",
        "node_not_found": "Node.js not detected (required for YouTube downloads)",
        "node_install_hint": "Please install manually: https://nodejs.org/",
        "browser_firefox": "Browser: firefox",
        "firefox_not_found": "Firefox not detected",
        "firefox_recommended": "Firefox is the recommended browser for the following reasons:",
        "firefox_reason_1": "· YouTube and other platforms restrict cookie extraction from Chrome/Edge, which may cause download failures",
        "firefox_reason_2": "· Firefox's cookie format has the best compatibility with yt-dlp",
        "firefox_download": "Firefox download: https://www.mozilla.org/firefox/",
        "firefox_install_prompt": "Have you installed or plan to install Firefox? [Y/n]: ",
        "firefox_install_later": "Please install Firefox and re-run the installer for the best experience.",
        "firefox_continue": "Continuing installation, will use Firefox as default browser config (takes effect after installation).",
        "firefox_skipped": "Firefox skipped. Note:",
        "firefox_skip_warn_1": "· When using other browsers, YouTube premium content and login-required content may not download",
        "firefox_skip_warn_2": "· If you encounter 'Sign in to confirm you're not a bot' errors, please use Firefox",
        "browser_detected": "Detected installed browser: {browser}, will use it for configuration",
        "no_browser_detected": "No installed browser detected",
        "manual_browser_prompt": "Manually specify browser path? [y/N]: ",
        "supported_browsers": "Supported browsers: firefox, chrome, edge, brave",
        "browser_name_prompt": "Browser name: ",
        "browser_path_prompt": "Browser installation path (executable or directory): ",
        "browser_verified": "Browser verified: {browser}",
        "browser_path_invalid": "Invalid path or browser mismatch, will skip cookie configuration",
        "installing_ytdlp": "Installing yt-dlp...",
        "ytdlp_installed": "yt-dlp installed",
        "ytdlp_install_failed": "yt-dlp installation failed, please check if pip is available",
        "downloading": "Downloading... {pct}%",
        "ffmpeg_exists": "ffmpeg already exists in installation directory, skipping download",
        "ffmpeg_system": "ffmpeg found in system, skipping download",
        "ffmpeg_downloading": "Downloading ffmpeg...",
        "ffmpeg_extracting": "Extracting ffmpeg...",
        "ffmpeg_installed": "ffmpeg installed",
        "ffmpeg_not_supported": "Automatic ffmpeg installation not supported on this platform, please install manually",
        "ffmpeg_install_hint": "Installation guide: https://github.com/yt-dlp/FFmpeg-Builds",
        "proxy_prompt": "Select proxy settings:",
        "proxy_none": "[1] No proxy",
        "proxy_default": "[2] Use default proxy (127.0.0.1:10808)",
        "proxy_custom": "[3] Custom proxy",
        "proxy_choice": "Please select [1-3]: ",
        "proxy_custom_prompt": "Enter proxy address (format: host:port): ",
        "proxy_set": "Proxy set: {proxy}",
        "proxy_disabled": "Proxy disabled",
        "output_path_prompt": "Video save path",
        "profile_created": "Profile created: {profile}",
        "active_profile_set": "Active profile: {profile}",
        "desktop_shortcut_created": "Desktop shortcut created",
        "desktop_shortcut_failed": "Desktop shortcut creation failed",
        "env_var_set": "Environment variable set: EASY_YTDLP_HOME",
        "path_updated": "PATH updated",
        "install_complete": "Installation complete!",
        "install_complete_hint": "Run 'easy-ytdlp' to launch the tool",
        "install_complete_hint_windows": "Please restart terminal or re-login for environment variables to take effect",
        "existing_install_found": "Existing installation detected: {path}",
        "existing_install_prompt": "Use existing installation? [Y/n]: ",
        "existing_install_use": "Using existing installation",
        "existing_install_skip": "Skipping, will create new installation",
        "uninstall_confirm": "Confirm uninstall Easy yt-dlp? [y/N]: ",
        "uninstalling": "Uninstalling...",
        "uninstall_complete": "Uninstall complete",
        "uninstall_cancelled": "Uninstall cancelled",
        "not_installed": "Installation not detected",
        "updating_ytdlp": "Updating yt-dlp...",
        "ytdlp_updated": "yt-dlp updated",
        "ytdlp_update_failed": "yt-dlp update failed",
        "menu_title": "Easy yt-dlp Installer",
        "menu_install": "[1] Install",
        "menu_uninstall": "[2] Uninstall",
        "menu_exit": "[3] Exit",
        "menu_prompt": "Please select [1-3]: ",
        "invalid_choice": "Invalid choice",
        "base_config_created": "Base config created: {path}",
        "default_profile_created": "Default profile created: {path}",
        "profile_desc": "Priority 1080P video, no audio kept, mp4 format",
        "proxy_choice_prompt": "Select proxy [1-3]: ",
        "proxy_address_prompt": "Enter proxy address (format: host:port): ",
        "video_path_prompt": "Video save path",
        "shortcut_creating": "Creating desktop shortcut...",
        "env_setting": "Setting environment variables...",
        "install_success": "Installation complete!",
        "install_hint_run": "Run 'easy-ytdlp' to launch",
        "install_hint_restart": "Please restart terminal or re-login for environment variables to take effect",
        "existing_found": "Existing installation found: {path}",
        "use_existing_prompt": "Use existing installation? [Y/n]: ",
        "use_existing": "Using existing installation",
        "create_new": "Creating new installation",
        "uninstall_prompt": "Confirm uninstall Easy yt-dlp? [y/N]: ",
        "uninstall_progress": "Uninstalling...",
        "uninstall_done": "Uninstall complete",
        "uninstall_cancel": "Uninstall cancelled",
        "not_installed_msg": "Easy yt-dlp not installed",
        "update_ytdlp_progress": "Updating yt-dlp...",
        "update_ytdlp_done": "yt-dlp updated to latest version",
        "update_ytdlp_fail": "yt-dlp update failed",
    }
}

def t(key, **kwargs):
    """Get translated string."""
    text = _TRANSLATIONS.get(_LANG, _TRANSLATIONS["en_US"]).get(key, key)
    return text.format(**kwargs) if kwargs else text

# ── constants ────────────────────────────────────────────────────────────────
TOOL_DIR = Path.home() / ".easy-ytdlp"
CONF_PATH = TOOL_DIR / "yt-dlp.conf"
FFMPEG_BASE = "https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest"

_FFMPEG_PKG = {
    ("windows", "x64"):   ("ffmpeg-master-latest-win64-gpl.zip",      "zip"),
    ("windows", "arm64"): ("ffmpeg-master-latest-winarm64-gpl.zip",   "zip"),
    ("linux",   "x64"):   ("ffmpeg-master-latest-linux64-gpl.tar.xz", "tar"),
    ("linux",   "arm64"): ("ffmpeg-master-latest-linuxarm64-gpl.tar.xz", "tar"),
}

# ── helpers ───────────────────────────────────────────────────────────────────
def _platform():
    if sys.platform == "win32":   return "windows"
    if sys.platform == "darwin":  return "macos"
    return "linux"

def _arch():
    m = os.uname().machine.lower() if hasattr(os, "uname") else ""
    if m in ("arm64", "aarch64"): return "arm64"
    import platform
    if platform.machine().lower() in ("arm64", "aarch64"): return "arm64"
    return "x64"

def _ok(msg):  print(f"  \033[32m✔\033[0m {msg}")
def _warn(msg): print(f"  \033[33m⚠\033[0m {msg}")
def _err(msg):  print(f"  \033[31m✘\033[0m {msg}")
def _info(msg): print(f"  \033[36m→\033[0m {msg}")

def _prompt(prompt, default=""):
    suffix = f" [{default}]" if default else ""
    val = input(f"{prompt}{suffix}: ").strip()
    return val if val else default

# ── detection ─────────────────────────────────────────────────────────────────
def check_existing_installation():
    """Check if Easy yt-dlp is already installed."""
    if _platform() == "windows":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ)
            install_dir, _ = winreg.QueryValueEx(key, "EASY_YTDLP_HOME")
            winreg.CloseKey(key)
            install_path = Path(install_dir)
            # Check if installation is valid
            if install_path.exists() and (install_path / "profiles").exists():
                return install_path
        except:
            pass
    else:
        # Check shell rc files for EASY_YTDLP_HOME
        shell = os.environ.get("SHELL", "")
        rc_files = []
        if "zsh" in shell:
            rc_files = [Path.home() / ".zshrc"]
        elif "bash" in shell:
            rc_files = [Path.home() / ".bashrc", Path.home() / ".bash_profile"]
        else:
            rc_files = [Path.home() / ".profile"]
        
        for rc_file in rc_files:
            if rc_file.exists():
                content = rc_file.read_text(encoding="utf-8")
                import re
                match = re.search(r'export EASY_YTDLP_HOME="([^"]+)"', content)
                if match:
                    install_path = Path(match.group(1))
                    if install_path.exists() and (install_path / "profiles").exists():
                        return install_path
    return None

def check_python():
    if sys.version_info < (3, 10):
        _err(t("python_version_error", version=sys.version.split()[0]))
        sys.exit(1)
    _ok(f"Python {sys.version.split()[0]}")

def check_node():
    if shutil.which("node"):
        _ok(t("node_installed"))
        return True
    _warn(t("node_not_found"))
    _info(t("node_install_hint"))
    return False

def _check_browser_installed(browser: str) -> bool:
    """Check if browser is installed (PATH, registry, or platform-specific locations)."""
    if shutil.which(browser):
        return True
    
    plat = _platform()
    
    if plat == "windows":
        try:
            import winreg
            reg_paths = {
                "firefox": [
                    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Mozilla\Mozilla Firefox"),
                    (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Mozilla\Mozilla Firefox"),
                ],
                "chrome": [
                    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Google\Chrome"),
                    (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Google\Chrome"),
                ],
                "edge": [
                    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Edge"),
                    (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Edge"),
                ],
                "brave": [
                    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\BraveSoftware\Brave-Browser"),
                    (winreg.HKEY_CURRENT_USER, r"SOFTWARE\BraveSoftware\Brave-Browser"),
                ],
            }
            for hkey, subkey in reg_paths.get(browser, []):
                try:
                    winreg.OpenKey(hkey, subkey)
                    return True
                except FileNotFoundError:
                    continue
        except ImportError:
            pass
    
    elif plat == "linux":
        paths = {
            "firefox": ["/usr/bin/firefox", "/usr/lib/firefox/firefox"],
            "chrome": ["/usr/bin/google-chrome", "/usr/bin/google-chrome-stable"],
            "chromium": ["/usr/bin/chromium", "/usr/bin/chromium-browser"],
            "brave": ["/usr/bin/brave-browser", "/usr/bin/brave"],
            "edge": ["/usr/bin/microsoft-edge"],
        }
        return any(Path(p).exists() for p in paths.get(browser, []))
    
    elif plat == "macos":
        apps = {
            "firefox": "/Applications/Firefox.app",
            "chrome": "/Applications/Google Chrome.app",
            "chromium": "/Applications/Chromium.app",
            "brave": "/Applications/Brave Browser.app",
            "edge": "/Applications/Microsoft Edge.app",
        }
        app_path = apps.get(browser)
        return app_path and Path(app_path).exists()
    
    return False

def _verify_browser_path(browser: str, path: str) -> bool:
    """Verify if the given path contains the specified browser."""
    p = Path(path)
    if not p.exists():
        return False
    
    plat = _platform()
    if plat == "windows":
        exe_names = {"firefox": "firefox.exe", "chrome": "chrome.exe", "edge": "msedge.exe", "brave": "brave.exe"}
        exe = exe_names.get(browser)
        return exe and (p / exe).exists() if p.is_dir() else p.name.lower() == exe
    elif plat == "macos":
        return p.suffix == ".app" and p.exists()
    else:  # linux
        return (p / browser).exists() if p.is_dir() else p.name == browser

def detect_browser() -> str:
    if _check_browser_installed("firefox"):
        _ok(t("browser_firefox"))
        return "firefox"

    # Firefox not found — check for alternatives
    alternatives = [b for b in ("chrome", "chromium", "edge", "brave") if _check_browser_installed(b)]

    _warn(t("firefox_not_found"))
    print()
    print(f"  {t('firefox_recommended')}")
    print(f"  {t('firefox_reason_1')}")
    print(f"  {t('firefox_reason_2')}")
    print()
    _info(t("firefox_download"))
    print()
    ans = input(f"  {t('firefox_install_prompt')}").strip().lower()

    if ans in ("", "y"):
        _info(t("firefox_install_later"))
        _info(t("firefox_continue"))
        return "firefox"
    else:
        print()
        _warn(t("firefox_skipped"))
        print(f"  {t('firefox_skip_warn_1')}")
        print(f"  {t('firefox_skip_warn_2')}")
        print()
        if alternatives:
            detected = alternatives[0]
            _info(t("browser_detected", browser=detected))
            return detected
        else:
            _warn(t("no_browser_detected"))
            print()
            ans = input(f"  {t('manual_browser_prompt')}").strip().lower()
            if ans == "y":
                print(f"\n  {t('supported_browsers')}")
                browser = input(f"  {t('browser_name_prompt')}").strip().lower()
                if browser in ("firefox", "chrome", "edge", "brave", "chromium"):
                    path = input(f"  {t('browser_path_prompt')}").strip()
                    if _verify_browser_path(browser, path):
                        _ok(t("browser_verified", browser=browser))
                        return browser
                    else:
                        _err(t("browser_path_invalid"))
            return ""

def install_ytdlp():
    print(f"\n{t('installing_ytdlp')}")
    r = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-U", "yt-dlp[default,curl-cffi]"]
    )
    if r.returncode == 0:
        _ok(t("ytdlp_installed"))
    else:
        _err(t("ytdlp_install_failed"))
        sys.exit(1)

def _progress(count, block, total):
    if total > 0:
        pct = min(count * block * 100 // total, 100)
        print(f"\r  {t('downloading', pct=pct)}", end="", flush=True)

def install_ffmpeg() -> str:
    """Returns the ffmpeg directory (tool dir or system path)."""
    # Check if ffmpeg exists in tool dir
    if (TOOL_DIR / "ffmpeg.exe").exists() if _platform() == "windows" else (TOOL_DIR / "ffmpeg").exists():
        _ok(t("ffmpeg_exists"))
        return str(TOOL_DIR)
    
    if shutil.which("ffmpeg"):
        _ok(t("ffmpeg_system"))
        return shutil.which("ffmpeg").rsplit(os.sep, 1)[0]

    plat = _platform()
    arch = _arch()

    if plat == "macos":
        _warn(t("ffmpeg_not_supported"))
        _info(t("ffmpeg_install_hint"))
        return ""

    key = (plat, arch)
    if key not in _FFMPEG_PKG:
        _warn(t("ffmpeg_not_supported"))
        _info(t("ffmpeg_install_hint"))
        return ""

    filename, fmt = _FFMPEG_PKG[key]
    url = f"{FFMPEG_BASE}/{filename}"
    print(f"\n{t('ffmpeg_downloading')}")

    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp) / filename
        try:
            urlretrieve(url, dest, _progress)
            print()
        except Exception as e:
            _err(f"{t('ytdlp_install_failed')}: {e}")
            return ""

        TOOL_DIR.mkdir(parents=True, exist_ok=True)
        suffix = ".exe" if plat == "windows" else ""

        print(f"{t('ffmpeg_extracting')}")
        if fmt == "zip":
            with zipfile.ZipFile(dest) as zf:
                for name in zf.namelist():
                    base = Path(name).name
                    if base in (f"ffmpeg{suffix}", f"ffprobe{suffix}"):
                        data = zf.read(name)
                        out = TOOL_DIR / base
                        out.write_bytes(data)
                        if plat != "windows":
                            out.chmod(0o755)
        else:
            with tarfile.open(dest, "r:xz") as tf:
                for member in tf.getmembers():
                    base = Path(member.name).name
                    if base in ("ffmpeg", "ffprobe"):
                        f = tf.extractfile(member)
                        if f:
                            out = TOOL_DIR / base
                            out.write_bytes(f.read())
                            out.chmod(0o755)

    _ok(t("ffmpeg_installed"))
    return str(TOOL_DIR)

# ── config generation ─────────────────────────────────────────────────────────
DEFAULT_PROFILE_ID = "sys_default_1080P-mp4-lean"

def _write_conf(video_path: str, ffmpeg_dir: str, proxy: str, browser: str):
    # Write base config (root config)
    config_dir = TOOL_DIR / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    base_conf = config_dir / "base.conf"
    
    base_lines = []
    if proxy:
        base_lines += ["# Use a proxy", f"--proxy={proxy}"]
    if browser:
        base_lines += [f"# Use {browser} browser cookies", f"--cookies-from-browser={browser}"]
    base_lines += [
        "# Disable playlist download by default",
        "--no-playlist",
        "# Output file directory",
        f"--output='{video_path}/%(title)s.%(ext)s'",
    ]
    if ffmpeg_dir:
        base_lines += ["# Path to ffmpeg", f"--ffmpeg-location='{ffmpeg_dir}'"]
    
    base_conf.write_text("\n".join(base_lines) + "\n", encoding="utf-8")
    _ok(t("base_config_created", path=base_conf))
    
    # Write default profile config (format only)
    profile_dir = TOOL_DIR / "profiles" / DEFAULT_PROFILE_ID
    profile_dir.mkdir(parents=True, exist_ok=True)
    conf_path = profile_dir / "yt-dlp.conf"
    
    profile_lines = [
        "# Download format: 1080P MP4 -> best merged format -> best available",
        '--format "b[ext=mp4][height=1080]/bv[ext=mp4][height=1080]+ba[ext=m4a]/bv*+ba/b"',
    ]
    conf_path.write_text("\n".join(profile_lines) + "\n", encoding="utf-8")
    
    # Write meta
    meta_path = profile_dir / ".meta"
    meta_path.write_text(
        f"name={DEFAULT_PROFILE_ID}\ndesc={t('profile_desc')}\n",
        encoding="utf-8"
    )
    # Set as active profile
    (TOOL_DIR / "active_profile").write_text(DEFAULT_PROFILE_ID, encoding="utf-8")
    _ok(t("default_profile_created", path=conf_path))

# ── global command registration ───────────────────────────────────────────────
def _create_desktop_shortcut():
    """Create desktop shortcut with icon."""
    plat = _platform()
    
    # Get desktop path
    if plat == "windows":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
            desktop, _ = winreg.QueryValueEx(key, "Desktop")
            winreg.CloseKey(key)
            desktop = Path(desktop)
        except:
            desktop = Path.home() / "Desktop"
    else:
        desktop = Path.home() / "Desktop"
    
    if not desktop.exists():
        _warn("未找到桌面目录，跳过快捷方式创建")
        return
    
    # Copy icon to tool dir
    if plat == "windows":
        icon_src = Path(__file__).parent / "easy-ytdlp.ico"
        icon_dest = TOOL_DIR / "easy-ytdlp.ico"
    else:
        icon_src = Path(__file__).parent / "app-icon.png"
        icon_dest = TOOL_DIR / "app-icon.png"
    
    if icon_src.exists():
        shutil.copy2(icon_src, icon_dest)
    else:
        icon_dest = None
    
    if plat == "windows":
        shortcut_path = desktop / "Easy yt-dlp.lnk"
        bat_path = TOOL_DIR / "easy-ytdlp.bat"

        # Use PowerShell to create shortcut (supports Unicode paths natively,
        # avoids cscript/VBScript ANSI encoding issues with non-ASCII desktop paths)
        desc = "Easy yt-dlp - Minimalist yt-dlp frontend" if _LANG == "en_US" else "Easy yt-dlp - yt-dlp 极简前端"
        icon_line = f'$lnk.IconLocation = "{icon_dest}"' if icon_dest else ''
        ps_script = (
            f'$ws = New-Object -ComObject WScript.Shell; '
            f'$lnk = $ws.CreateShortcut("{shortcut_path}"); '
            f'$lnk.TargetPath = "{bat_path}"; '
            f'$lnk.WorkingDirectory = "{Path.home()}"; '
            f'{icon_line + "; " if icon_line else ""}'
            f'$lnk.Description = "{desc}"; '
            f'$lnk.Save()'
        )

        try:
            result = subprocess.run(
                [
                    "powershell", "-NoProfile", "-NonInteractive",
                    "-ExecutionPolicy", "Bypass",
                    "-Command", ps_script,
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=10,
            )

            if result.returncode == 0 and shortcut_path.exists():
                _ok(t("desktop_shortcut_created"))
            else:
                raise Exception(result.stderr.strip() or t("desktop_shortcut_failed"))
        except Exception as e:
            _warn(f"{t('desktop_shortcut_failed')}: {e}")
    
    else:  # Linux/macOS
        desktop_file = desktop / "easy-ytdlp.desktop"
        wrapper = Path.home() / ".local" / "bin" / "easy-ytdlp"
        
        comment = "Minimalist yt-dlp frontend" if _LANG == "en_US" else "yt-dlp 极简前端"
        content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Easy yt-dlp
Comment={comment}
Exec={wrapper}
Icon={icon_dest}
Terminal=true
Categories=Utility;
"""
        desktop_file.write_text(content, encoding="utf-8")
        desktop_file.chmod(0o755)
        _ok(t("desktop_shortcut_created"))

def _register_command():
    plat = _platform()
    if plat == "windows":
        bat = TOOL_DIR / "easy-ytdlp.bat"
        bat.write_text(
            f'@echo off\n'
            f'set PYTHONPATH={TOOL_DIR}\\src;%PYTHONPATH%\n'
            f'"{sys.executable}" -m easy_ytdlp %*\n',
            encoding="utf-8"
        )
        # Add EASY_YTDLP_HOME and update PATH via registry
        try:
            import winreg
            import ctypes
            
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE)
            
            # Set EASY_YTDLP_HOME
            winreg.SetValueEx(key, "EASY_YTDLP_HOME", 0, winreg.REG_SZ, str(TOOL_DIR))
            
            # Update PATH
            try:
                user_path, reg_type = winreg.QueryValueEx(key, "Path")
            except FileNotFoundError:
                user_path, reg_type = "", winreg.REG_EXPAND_SZ
            
            # Add %EASY_YTDLP_HOME% to PATH
            path_var = "%EASY_YTDLP_HOME%"
            if path_var.lower() not in user_path.lower() and str(TOOL_DIR).lower() not in user_path.lower():
                new_path = f"{user_path};{path_var}" if user_path else path_var
                winreg.SetValueEx(key, "Path", 0, reg_type, new_path)
            
            winreg.CloseKey(key)
            
            # Broadcast environment change
            ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x001A, 0, "Environment", 0x02, 1000, None)
            _ok(t("env_var_set"))
            _ok(t("path_updated"))
        except Exception as e:
            _warn(f"{t('env_var_set')}: {e}")
    else:
        bin_dir = Path.home() / ".local" / "bin"
        bin_dir.mkdir(parents=True, exist_ok=True)
        wrapper = bin_dir / "easy-ytdlp"
        wrapper.write_text(
            f'#!/bin/sh\n'
            f'export PYTHONPATH="{TOOL_DIR}/src:$PYTHONPATH"\n'
            f'exec "{sys.executable}" -m easy_ytdlp "$@"\n',
            encoding="utf-8"
        )
        wrapper.chmod(0o755)
        _ok(f"{t('env_var_set')}: {wrapper}")
        
        # Add EASY_YTDLP_HOME and PATH to shell rc file
        shell = os.environ.get("SHELL", "")
        rc_files = []
        
        if "zsh" in shell:
            rc_files = [Path.home() / ".zshrc"]
        elif "bash" in shell:
            rc_files = [Path.home() / ".bashrc", Path.home() / ".bash_profile"]
        else:
            rc_files = [Path.home() / ".profile"]
        
        export_home = f'export EASY_YTDLP_HOME="{TOOL_DIR}"\n'
        export_path = f'export PATH="$EASY_YTDLP_HOME:$PATH"\n'
        
        for rc_file in rc_files:
            if rc_file.exists():
                content = rc_file.read_text(encoding="utf-8")
                needs_update = False
                lines_to_add = []
                
                if "EASY_YTDLP_HOME" not in content:
                    lines_to_add.append(export_home)
                    needs_update = True
                
                if "$EASY_YTDLP_HOME" not in content and str(bin_dir) not in content:
                    lines_to_add.append(export_path)
                    needs_update = True
                
                if needs_update:
                    with open(rc_file, "a", encoding="utf-8") as f:
                        f.write("\n" + "".join(lines_to_add))
                    _ok(f"{t('env_var_set')}: {rc_file.name}")
                break
        else:
            # Create .profile if no rc file exists
            profile = Path.home() / ".profile"
            with open(profile, "a", encoding="utf-8") as f:
                f.write(f"\n{export_home}{export_path}")
            _ok(f"{t('env_var_set')}: {profile.name}")
        
        _info(t("install_hint_restart"))

# ── install / uninstall ───────────────────────────────────────────────────────
def do_install():
    print(f"\n=== {t('menu_title')} ===\n")
    
    # Check existing installation
    existing = check_existing_installation()
    if existing:
        _warn(t("existing_found", path=existing))
        confirm = input(f"{t('use_existing_prompt')}").strip().lower()
        if confirm not in ("", "y"):
            print(t("create_new"))
        else:
            print(t("use_existing"))
            return
        print()
    
    print(f"【1/4】{t('node_installed')}")
    check_python()
    plat = _platform()
    arch = _arch()
    _ok(f"{plat} / {arch}")
    check_node()
    browser = detect_browser()

    print(f"\n【2/4】{t('installing_ytdlp')}")
    install_ytdlp()

    print(f"\n【3/4】{t('ffmpeg_downloading')}")
    ffmpeg_dir = install_ffmpeg()

    print(f"\n【4/4】{t('proxy_prompt')}")
    TOOL_DIR.mkdir(parents=True, exist_ok=True)

    default_video = str(Path.home() / "Downloads")
    video_path = _prompt(t("video_path_prompt"), default_video)
    Path(video_path).expanduser().mkdir(parents=True, exist_ok=True)

    print(f"\n{t('proxy_prompt')}")
    print(f"  {t('proxy_none')}")
    print(f"  {t('proxy_default')}")
    print(f"  {t('proxy_custom')}")
    proxy_choice = input(t("proxy_choice_prompt")).strip() or "1"
    
    if proxy_choice == "2":
        proxy = "127.0.0.1:10808"
    elif proxy_choice == "3":
        proxy = input(t("proxy_address_prompt")).strip()
    else:
        proxy = ""
    
    browser = _prompt(f"{t('browser_firefox')}", browser)

    _write_conf(video_path, ffmpeg_dir, proxy, browser)
    
    # Copy src to tool directory
    src_dir = Path(__file__).parent / "src"
    if src_dir.exists():
        dest_src = TOOL_DIR / "src"
        if dest_src.exists():
            shutil.rmtree(dest_src)
        shutil.copytree(src_dir, dest_src)
        _ok(f"Module copied to {dest_src}")
    
    _register_command()
    _create_desktop_shortcut()

    print(f"""
\033[32m{t('install_success')}\033[0m
  {TOOL_DIR}
  Profile: {TOOL_DIR / 'profiles' / DEFAULT_PROFILE_ID}
  
  {t('install_hint_run')}
  {t('install_hint_restart')}
""")

def do_uninstall():
    print(f"\n=== {t('menu_uninstall')} ===\n")
    confirm = input(t("uninstall_prompt")).strip().lower()
    if confirm != "y":
        print(t("uninstall_cancel"))
        return

    print(t("uninstall_progress"))
    if TOOL_DIR.exists():
        shutil.rmtree(TOOL_DIR)
        _ok(f"{TOOL_DIR}")
    
    # Remove desktop shortcut
    plat = _platform()
    if plat == "windows":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
            desktop, _ = winreg.QueryValueEx(key, "Desktop")
            winreg.CloseKey(key)
            desktop = Path(desktop)
        except:
            desktop = Path.home() / "Desktop"
        
        shortcuts = [desktop / "Easy yt-dlp.lnk", desktop / "Easy yt-dlp.bat"]
        for shortcut in shortcuts:
            if shortcut.exists():
                shortcut.unlink()
                _ok(t("desktop_shortcut_created"))
                break
    else:
        desktop = Path.home() / "Desktop"
        shortcut = desktop / "easy-ytdlp.desktop"
        if shortcut.exists():
            shortcut.unlink()
            _ok(t("desktop_shortcut_created"))

    plat = _platform()
    if plat == "windows":
        # Remove environment variables
        try:
            import winreg
            import ctypes
            
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE)
            
            # Remove EASY_YTDLP_HOME
            try:
                winreg.DeleteValue(key, "EASY_YTDLP_HOME")
                _ok(t("env_var_set"))
            except:
                pass
            
            # Remove from PATH
            try:
                user_path, reg_type = winreg.QueryValueEx(key, "Path")
                # Remove both %EASY_YTDLP_HOME% and actual path
                new_path = ";".join(p for p in user_path.split(";") 
                                   if p.lower() not in ("%easy_ytdlp_home%", str(TOOL_DIR).lower()))
                winreg.SetValueEx(key, "Path", 0, reg_type, new_path)
                _ok(t("path_updated"))
            except:
                pass
            
            winreg.CloseKey(key)
            
            # Broadcast environment change
            ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x001A, 0, "Environment", 0x02, 1000, None)
        except Exception as e:
            _warn(f"{t('env_var_set')}: {e}")
    else:
        wrapper = Path.home() / ".local" / "bin" / "easy-ytdlp"
        if wrapper.exists():
            wrapper.unlink()
            _ok(f"{wrapper}")
        
        # Remove from shell rc files
        shell = os.environ.get("SHELL", "")
        rc_files = []
        if "zsh" in shell:
            rc_files = [Path.home() / ".zshrc"]
        elif "bash" in shell:
            rc_files = [Path.home() / ".bashrc", Path.home() / ".bash_profile"]
        else:
            rc_files = [Path.home() / ".profile"]
        
        for rc_file in rc_files:
            if rc_file.exists():
                content = rc_file.read_text(encoding="utf-8")
                lines = content.split("\n")
                new_lines = [line for line in lines if "EASY_YTDLP_HOME" not in line]
                if len(new_lines) != len(lines):
                    rc_file.write_text("\n".join(new_lines), encoding="utf-8")
                    _ok(f"{rc_file.name}")
                break

    print(f"\n\033[32m{t('uninstall_done')}\033[0m\n")

# ── entry point ───────────────────────────────────────────────────────────────
def main():
    print(f"{t('menu_title')}\n")
    print(t("menu_install"))
    print(t("menu_uninstall"))
    print(t("menu_exit"))
    choice = input(f"\n{t('menu_prompt')}").strip()
    if choice == "1":
        do_install()
    elif choice == "2":
        do_uninstall()
    elif choice == "3":
        sys.exit(0)
    else:
        print(t("invalid_choice"))

if __name__ == "__main__":
    main()
