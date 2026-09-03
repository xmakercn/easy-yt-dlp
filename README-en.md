<div align="center">

# Easy yt-dlp

**English | [简体中文](README.md)**

**Easy yt-dlp** is a minimalist interactive frontend tool designed specifically for the versatile and powerful video downloader, yt-dlp. It perfectly addresses the pain points of the original command-line version's overwhelming parameters and high memorization burden, delivering a smooth and satisfying download experience through a fully automated workflow. Featuring auto-installation, auto-updates, and a proprietary Format Preference System (Profile) that remembers your download habits, it operates via a menu-driven interface. Simply paste a URL to download with ease, making it extremely user-friendly for those unfamiliar with the terminal. It supports one-click installation (with portable mode also available), is compatible with Windows, Linux, and macOS, and automatically creates a desktop shortcut upon setup.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](https://github.com/xmakercn/easy-ytdlp)
[![Stars](https://img.shields.io/github/stars/xmakercn/easy-ytdlp?style=social)](https://github.com/xmakercn/easy-ytdlp/stargazers)

[Features](#-features) · [How It Works](#-how-it-works) · [Quick Start](#-quick-start) · [Profile System](#-profile-system) · [Configuration](#-configuration) · [What's New](#-whats-new) · [Contributing](#-contributing)

</div>

---

## ✨ Features

- **Zero Command-Line** — Interactive menu-driven, paste URL and download, no parameters to memorize
- **Profile System** — Different download scenarios with different configs, 1080P video, audio-only, 4K, Bilibili... one-click switch, no interference
- **Hierarchical Configuration** — Base config manages common parameters, Profile config focuses on format selection, child configs can override base config
- **Smart Format Selection** — Built-in format priority strategy, auto-select best quality, auto-merge video + audio streams
- **Fine-Grained Playlist Control** — Download entire list, continuous segments (start-end index), arbitrary specified episodes (e.g., `1,3:5,7`)
- **Keep Audio Toggle** — One-click toggle to keep m4a audio file simultaneously, no config modification needed
- **Auto Dependency Management** — Installation script auto-detects and configures ffmpeg, yt-dlp, no manual setup
- **Desktop Shortcut** — Auto-creates desktop shortcut after installation, double-click to launch
- **Cross-Platform** — Windows / Linux / macOS fully supported, consistent behavior
- **One-Click yt-dlp Update** — Update to latest version directly from menu, always maintain best compatibility

---

## 💡 Design Philosophy

> **Easy yt-dlp simplifies yt-dlp configuration.**

yt-dlp is powerful but has numerous parameters. Typing commands every time is inefficient and error-prone. Easy yt-dlp's approach:

- **Configure once**, save common parameters in Profiles, reuse for every download
- **Different needs, different Profiles**, instead of manually changing parameters each time
- **Tool manages what it should** (playlist control, audio toggle), everything else is up to your configuration

This way you keep yt-dlp's full power without dealing with command-line every time.

---

## ⚙️ How It Works

```
User inputs URL
      │
      ▼
Easy yt-dlp reads configuration
      │
      ├─ Load base config: ~/.easy-ytdlp/config/base.conf
      │  (proxy, browser, ffmpeg, output path, common settings)
      │
      ├─ Load Profile config: ~/.easy-ytdlp/profiles/<profile-id>/yt-dlp.conf
      │  (format selection, can override base config)
      │
      ├─ Append runtime parameters (playlist control, audio toggle, etc.)
      │
      ▼
Assemble complete yt-dlp command and execute
      │
      ▼
ffmpeg auto-merges video + audio streams (if needed)
      │
      ▼
Files saved to specified directory
```

Configurations are stored in user directory, completely separate from project code. Upgrading the tool won't affect your configs.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js (required by installation script)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/xmakercn/easy-ytdlp.git
cd easy-ytdlp

# 2. Run installation script
python install.py
# Select [1] Install, follow prompts to configure:
#   - Browser selection (for cookies)
#   - Video save path
#   - Proxy settings (none/default/custom)

# 3. Launch
# Method 1: Double-click desktop shortcut "Easy yt-dlp"
# Method 2: Run from command line
easy-ytdlp
# (Windows users need to restart terminal or re-login for environment variables to take effect)
```

### Run Without Installation

```bash
cd src
python -m easy_ytdlp
```

### Uninstall

```bash
python install.py
# Select [2] Uninstall
```

---

## 📋 Menu Options

After launch, current Profile info is displayed, then main menu:

| Option | Function                                                 |
| ------ | -------------------------------------------------------- |
| `1`    | Download single video                                    |
| `2`    | Download entire playlist                                 |
| `3`    | Download playlist range (start-end index)                |
| `4`    | Download specific playlist items (e.g., `1,3:5,7`)       |
| `5`    | Toggle keep audio (when enabled, m4a audio file is kept) |
| `6`    | Switch Profile                                           |
| `7`    | Change video save path                                   |
| `8`    | Update yt-dlp to latest version                          |
| `9`    | Exit                                                     |

---

## 🗂️ Profile System

### Concept

A **Profile** = a set of yt-dlp configuration for a specific download scenario:

| Profile Example              | Purpose                             |
| ---------------------------- | ----------------------------------- |
| `sys_default_1080P-mp4-lean` | 1080P mp4, no audio kept (default)  |
| `audio-only`                 | Download audio only, convert to mp3 |
| `bilibili-4K`                | Bilibili 4K specific config         |

### Directory Structure

```
~/.easy-ytdlp/
├── config/
│   └── base.conf               # Base config (proxy, browser, output path, ffmpeg, etc.)
├── active_profile              # Currently active Profile ID
└── profiles/
    ├── sys_default_1080P-mp4-lean/
    │   ├── yt-dlp.conf         # Profile config (usually format-related only)
    │   └── .meta               # Profile name and description
    └── my-custom-profile/
        ├── yt-dlp.conf
        └── .meta
```

### Create Custom Profile

```bash
# 1. Create directory (directory name is Profile ID)
mkdir ~/.easy-ytdlp/profiles/audio-only

# 2. Create .meta
echo "name=audio-only" > ~/.easy-ytdlp/profiles/audio-only/.meta
echo "desc=Download audio only, convert to mp3" >> ~/.easy-ytdlp/profiles/audio-only/.meta

# 3. Create yt-dlp.conf
# Usually only format-related parameters needed, common configs inherited from base.conf
echo '--format "ba/b"' > ~/.easy-ytdlp/profiles/audio-only/yt-dlp.conf
echo '--extract-audio' >> ~/.easy-ytdlp/profiles/audio-only/yt-dlp.conf
echo '--audio-format mp3' >> ~/.easy-ytdlp/profiles/audio-only/yt-dlp.conf
```

Then launch the tool and select `[6] Switch Profile`.

**Note**: Profile config overrides base config. If you need different proxy, browser, or other parameters for a specific Profile, you can specify any configuration in Profile's yt-dlp.conf (except playlist-related parameters, which are managed by the tool automatically).

### Default Profile

`sys_default_1080P-mp4-lean` configuration:

| Config Item  | Value                                                                   |
| ------------ | ----------------------------------------------------------------------- |
| Video Format | `b[ext=mp4][height=1080]/bv[ext=mp4][height=1080]+ba[ext=m4a]/bv*+ba/b` |
| Keep Audio   | No (can be temporarily enabled via option `[5]`)                        |

**Common Config** (shared by all Profiles, stored in `config/base.conf`):

| Config Item    | Value                                                        |
| -------------- | ------------------------------------------------------------ |
| Browser Cookie | Selected during installation (default Firefox)               |
| Proxy          | Selected during installation (default none)                  |
| Playlist       | Disabled for single URL by default (options 2-4 auto-enable) |
| Output Path    | Specified during installation (default ~/Downloads)          |

---

## 📝 Configuration Reference

### Configuration Hierarchy

Easy yt-dlp uses **hierarchical configuration**:

- **Base config** (`config/base.conf`): Common configuration shared by all Profiles
- **Child config** (`profiles/<id>/yt-dlp.conf`): Profile-specific configuration, can override base config

### yt-dlp.conf Format

One parameter per line, identical to yt-dlp command-line syntax, `#` for comments:

```ini
# Proxy
--proxy=127.0.0.1:10808

# Browser cookies (for sites requiring login)
--cookies-from-browser=firefox

# Video format
--format "bv*+ba/b"

# Embed subtitles
--write-subs
--sub-langs zh-Hans,en

# Remove sponsor segments
--sponsorblock-remove sponsor
```

Full parameter list: [yt-dlp official documentation](https://github.com/yt-dlp/yt-dlp#usage-and-options).

### Base Config Parameters (base.conf)

| Parameter                | Description                 |
| ------------------------ | --------------------------- |
| `--proxy`                | Proxy address               |
| `--cookies-from-browser` | Browser cookies             |
| `--output`               | Output path template        |
| `--ffmpeg-location`      | ffmpeg path                 |
| `--no-playlist`          | Disable playlist by default |

### Profile Config Parameters (Recommended)

| Parameter                      | Description             |
| ------------------------------ | ----------------------- |
| `--format`                     | Video format selection  |
| `--merge-output-format`        | Merge output format     |
| `--sub-langs` / `--write-subs` | Subtitle download       |
| `--embed-thumbnail`            | Embed thumbnail         |
| `--sponsorblock-remove`        | Remove sponsor segments |

### Parameters NOT to Write in Config (Auto-managed by Tool)

| Parameter                          | Reason                                 |
| ---------------------------------- | -------------------------------------- |
| `--output`                         | Managed by menu option `[7]`           |
| `--ffmpeg-location`                | Auto-configured by installation script |
| `--no-playlist` / `--yes-playlist` | Auto-controlled by menu options 1-4    |
| `--playlist-items`                 | Auto-passed by menu options 3/4        |
| `--extract-audio` / `--keep-video` | Controlled by menu option `[5]`        |

---

## 🔄 Update yt-dlp

```bash
# Method 1: Menu option [8] (recommended)
easy-ytdlp

# Method 2: Direct pip
pip install -U "yt-dlp[default,curl-cffi]"
```

---

## 📅 What's New

### v1.0.0 · 2026-05-08

- 🎉 First public release
- ✅ Profile system: Multiple configs independently managed, one-click switch
- ✅ Hierarchical configuration: Base config + child config, flexible override
- ✅ Fine-grained playlist download (entire list, segments, specific items)
- ✅ Keep audio toggle
- ✅ Cross-platform installation script (Windows / Linux / macOS)
- ✅ Desktop shortcut auto-creation
- ✅ One-click yt-dlp update

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

- **Bug Reports**: Please include OS, Python version, and complete error message
- **Feature Suggestions**: Open an Issue first to discuss and avoid duplicate work
- **Code Contributions**: Fork → Create branch → Submit PR, maintain consistent code style

### Version Management

This project uses automatic semantic versioning. When submitting a PR, please add one of these labels:

- `major` - Breaking changes (1.0.0 → 2.0.0)
- `minor` - New features (1.0.0 → 1.1.0)
- `patch` - Bug fixes (1.0.0 → 1.0.1)

Version will be automatically bumped when PR is merged. See [VERSION_MANAGEMENT.md](docs/VERSION_MANAGEMENT.md) for details.

---

## ❓ FAQ

**Q: Which websites are supported?**  
A: All websites supported by yt-dlp, including YouTube, Bilibili, Twitter/X, Instagram, etc. Full list: [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

**Q: How to download YouTube content that requires login?**  
A: Configure `--cookies-from-browser=firefox` (or chrome) in Profile's `yt-dlp.conf`, ensure the browser is logged into the corresponding account.

**Q: Proxy not working?**  
A: Check if the `--proxy` address in `yt-dlp.conf` is correct, confirm the proxy service is running.

**Q: How to download 4K videos?**  
A: Create a new Profile, set `--format "bv[height=2160]+ba/bv*+ba/b"` in `yt-dlp.conf`, then switch to that Profile.

---

## 📄 License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

```
Copyright (C) 2026  Easy yt-dlp Contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
```

---

<div align="center">

If this project helps you, please give it a ⭐ Star — it's the best encouragement for developers!

</div>
