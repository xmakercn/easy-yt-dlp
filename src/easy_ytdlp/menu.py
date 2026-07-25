import re
import subprocess
import sys
from pathlib import Path
from . import __version__
from .platform_utils import colored, find_executable
from .config import (
    update_output_path, get_active_profile_id, set_active_profile_id,
    list_profiles, read_meta, read_proxy, read_output_path, read_browser,
)
from .downloader import (
    download_single, download_playlist, download_playlist_range,
    download_playlist_items, update_ytdlp, get_ytdlp_cmd,
)
from .i18n import t


def _ytdlp_version() -> str:
    try:
        r = subprocess.run([get_ytdlp_cmd(), "--version"], capture_output=True, text=True)
        return r.stdout.strip()
    except Exception:
        return "未知"


def show_header(keep_audio: bool) -> None:
    pid = get_active_profile_id()
    meta = read_meta()
    name = meta.get("name", pid)
    desc = meta.get("desc", "")
    
    # Read current config
    output_path = read_output_path()
    proxy = read_proxy()
    browser = read_browser()

    # Clear screen
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(t("app_description"))
    print("-" * 64)
    print(f"Easy yt-dlp: v{__version__}    yt-dlp: v{_ytdlp_version()}")
    print(colored(f"  ◆ {t('current_profile')}: {name}", "cyan"))
    if desc:
        print(f"    {desc}")
    print("-" * 64)
    
    # Display config
    print(f"  • {t('config_output_path')}: {colored(output_path or 'N/A', 'yellow')}")
    print(f"  • {t('config_proxy')}: {colored(proxy or t('config_none'), 'yellow')}")
    print(f"  • {t('config_browser')}: {colored(browser or t('config_none'), 'yellow')}")
    
    if keep_audio:
        print(f"  • {colored(t('keep_audio_on'), 'cyan')}")
    else:
        print(f"  • {t('keep_audio_off')}")
    print("-" * 64)
    print()  # Empty line before menu


def show_menu(keep_audio: bool) -> None:
    audio_tag = colored(f"[{t('on')}]", "cyan") if keep_audio else f"[{t('off')}]"
    print(t("menu_prompt"))
    for n, key in [
        ("1", "menu_1"),
        ("2", "menu_2"),
        ("3", "menu_3"),
        ("4", "menu_4"),
        ("5", "menu_5"),
        ("6", "menu_6"),
        ("7", "menu_7"),
        ("8", "menu_8"),
        ("9", "menu_9"),
    ]:
        if key == "menu_5":
            print(f"[{n}] {t(key, audio_tag=audio_tag)}")
        else:
            print(f"[{n}] {t(key)}")


def input_url() -> str:
    while True:
        url = input(t("input_url")).strip()
        if url:
            return url
        print(colored(t("url_empty"), "red"))


def input_playlist_range() -> tuple[int, int]:
    while True:
        try:
            start = int(input(t("input_start_index")).strip())
            end = int(input(t("input_end_index")).strip())
            if start > end:
                print(colored(t("start_gt_end"), "red"))
                continue
            return start, end
        except ValueError:
            print(colored(t("index_must_number"), "red"))


def input_playlist_items() -> str:
    while True:
        raw = input(t("input_items")).strip()
        s = raw.replace("，", ",").replace("：", ":")
        if not re.match(r"^\d+(?::\d+)?(?:,\d+(?::\d+)?)*$", s):
            print(colored(t("items_format_error"), "red"))
            continue
        seen: set[int] = set()
        valid = True
        for part in s.split(","):
            if ":" in part:
                a, b = (int(x) for x in part.split(":", 1))
                if a < 1 or b < 1:
                    print(colored(t("range_id_gte_1", part=part), "red")); valid = False; break
                if a >= b:
                    print(colored(t("range_start_lt_end", part=part), "red")); valid = False; break
                for i in range(a, b + 1):
                    if i in seen:
                        print(colored(t("duplicate_id", i=i), "red")); valid = False; break
                    seen.add(i)
                if not valid:
                    break
            else:
                i = int(part)
                if i < 1:
                    print(colored(t("id_gte_1", part=part), "red")); valid = False; break
                if i in seen:
                    print(colored(t("duplicate_id", i=i), "red")); valid = False; break
                seen.add(i)
        if valid:
            ids_str = ','.join(str(i) for i in sorted(seen))
            print(colored(t("items_valid", ids=ids_str), "green"))
            return s


def input_directory() -> str:
    while True:
        path = input(t("input_path")).strip()
        if not path:
            print(colored(t("path_empty"), "red"))
            continue
        p = Path(path).expanduser()
        if p.is_file():
            print(colored(t("path_is_file"), "red"))
            continue
        if not p.exists():
            try:
                p.mkdir(parents=True)
                print(colored(t("dir_created", path=p), "green"))
            except Exception as e:
                print(colored(t("dir_create_failed", error=e), "red"))
                continue
        else:
            print(colored(t("dir_confirmed", path=p), "green"))
        return str(p)


def switch_profile() -> None:
    profiles = list_profiles()
    if not profiles:
        print(colored(t("no_profiles"), "red"))
        return

    active = get_active_profile_id()
    print(f"\n{t('available_profiles')}：")
    for i, p in enumerate(profiles, 1):
        marker = colored("●", "cyan") if p["id"] == active else " "
        print(f"  {marker} [{i}] {p['name']}")
        if p["desc"]:
            print(f"         {p['desc']}")

    choice = input(f"\n{t('input_profile_number')}: ").strip()
    if not choice:
        return
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(profiles):
            new_id = profiles[idx]["id"]
            set_active_profile_id(new_id)
            meta = read_meta(new_id)
            print(colored(t("profile_switched", name=meta.get('name', new_id)) + "\n", "cyan"))
        else:
            print(colored(t("number_out_of_range"), "red"))
    except ValueError:
        print(colored(t("invalid_input"), "red"))


def run_menu() -> None:
    keep_audio = False
    
    while True:
        show_header(keep_audio)
        show_menu(keep_audio)
        try:
            choice = input(f"\n{t('input_choice')}: ").strip()
            if choice == "1":
                download_single(input_url(), keep_audio=keep_audio)
                print(colored(f"\n{t('download_complete')}\n", "green"))
            elif choice == "2":
                download_playlist(input_url(), keep_audio=keep_audio)
                print(colored(f"\n{t('playlist_download_complete')}\n", "green"))
            elif choice == "3":
                url = input_url()
                start, end = input_playlist_range()
                download_playlist_range(url, start, end, keep_audio=keep_audio)
                print(colored(f"\n{t('partial_playlist_complete')}\n", "green"))
            elif choice == "4":
                url = input_url()
                items = input_playlist_items()
                download_playlist_items(url, items, keep_audio=keep_audio)
                print(colored(f"\n{t('partial_playlist_complete')}\n", "green"))
            elif choice == "5":
                keep_audio = not keep_audio
                status = colored(t('audio_on'), "cyan") if keep_audio else t('audio_off')
                print(colored(t("keep_audio_status", status=status) + "\n", "cyan" if keep_audio else "yellow"))
            elif choice == "6":
                switch_profile()
            elif choice == "7":
                path = input_directory()
                update_output_path(path)
                print(colored(t("path_updated", path=path) + "\n", "green"))
            elif choice == "8":
                print(colored(t("updating"), "yellow"))
                update_ytdlp()
                print(colored(t("update_complete"), "green"))
                input(t("press_enter"))
            elif choice == "9":
                print(colored(t("exiting"), "yellow"))
                sys.exit(0)
            else:
                print(colored(t("invalid_choice"), "red"))
        except KeyboardInterrupt:
            print("\n")
            sys.exit(0)
        except FileNotFoundError as e:
            print(colored(t("error_msg", error=e), "red"))
            sys.exit(1)
        except Exception as e:
            print(colored(t("error_return_menu", error=e), "red"))
