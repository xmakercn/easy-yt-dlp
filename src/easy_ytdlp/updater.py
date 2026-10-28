import os
import re
import sys
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from .platform_utils import get_tool_dir, colored
from .config import read_proxy
from .i18n import t

RAW_BASE_URL = "https://raw.githubusercontent.com/xmakercn/easy-ytdlp/main/src/easy_ytdlp/"

MODULE_FILES = [
    "__init__.py",
    "__main__.py",
    "config.py",
    "downloader.py",
    "i18n.py",
    "i18n_en_US.py",
    "i18n_zh_CN.py",
    "menu.py",
    "platform_utils.py",
    "updater.py",
]


def update_self() -> bool:
    """Download the latest version of Easy yt-dlp from raw githubcontent."""
    proxy = read_proxy()
    proxies = {}
    if proxy:
        proxy_url = proxy if proxy.startswith(("http://", "https://", "socks5://")) else f"http://{proxy}"
        proxies = {"http": proxy_url, "https": proxy_url}

    opener = urllib.request.build_opener(urllib.request.ProxyHandler(proxies))

    downloaded: dict[str, bytes] = {}
    total = len(MODULE_FILES)

    for idx, fname in enumerate(MODULE_FILES, start=1):
        url = f"{RAW_BASE_URL}{fname}"
        print(f"  * {t('update_self_progress', file=fname, current=idx, total=total)}")
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "easy-ytdlp-updater", "Cache-Control": "no-cache"},
            )
            with opener.open(req, timeout=15) as res:
                if res.status == 200:
                    downloaded[fname] = res.read()
                else:
                    print(colored(t("update_self_failed", error=f"HTTP {res.status} on {fname}"), "red"))
                    return False
        except urllib.error.HTTPError as e:
            if e.code == 404 and fname == "updater.py":
                # If updater.py is newly created and not yet pushed to remote, ignore 404 for it
                continue
            print(colored(t("update_self_failed", error=f"{fname}: HTTP {e.code}"), "red"))
            return False
        except Exception as e:
            print(colored(t("update_self_failed", error=f"{fname}: {e}"), "red"))
            return False

    targets: list[Path] = []
    current_pkg_dir = Path(__file__).resolve().parent
    targets.append(current_pkg_dir)

    tool_pkg_dir = get_tool_dir() / "src" / "easy_ytdlp"
    if tool_pkg_dir.exists() and tool_pkg_dir.resolve() != current_pkg_dir.resolve():
        targets.append(tool_pkg_dir)

    try:
        for target_dir in targets:
            target_dir.mkdir(parents=True, exist_ok=True)
            for fname, data in downloaded.items():
                (target_dir / fname).write_bytes(data)
    except Exception as e:
        print(colored(t("update_self_failed", error=f"Write error: {e}"), "red"))
        return False

    init_content = downloaded.get("__init__.py", b"").decode("utf-8", errors="ignore")
    m = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', init_content)
    if m:
        new_ver = m.group(1)
        print(colored(f"  [v{new_ver}]", "green"))

    return True


def restart_app() -> None:
    """Restart Easy yt-dlp to reload all updated modules cleanly."""
    orig_argv = getattr(sys, "orig_argv", None)
    if orig_argv:
        cmd = list(orig_argv)
    else:
        cmd = [sys.executable, "-m", "easy_ytdlp"] + sys.argv[1:]

    if sys.platform == "win32":
        subprocess.call(cmd)
        sys.exit(0)
    else:
        os.execv(cmd[0], cmd)
