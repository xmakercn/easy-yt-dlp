<div align="center">

# Easy yt-dlp

**[English](README.md) | 简体中文**

**yt-dlp 的极简前端 —— 零命令行，Profile 一键切换，跨平台开箱即用**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](https://github.com/xmakercn/easy-ytdlp)
[![Stars](https://img.shields.io/github/stars/xmakercn/easy-ytdlp?style=social)](https://github.com/xmakercn/easy-ytdlp/stargazers)

[功能亮点](#-功能亮点) · [工作原理](#-工作原理) · [快速开始](#-快速开始) · [Profile 系统](#-profile-系统) · [配置参考](#-配置参考) · [最新动态](#-最新动态) · [贡献指南](#-贡献指南)

</div>

---

## ✨ 功能亮点

- **零命令行操作** — 交互式菜单驱动，粘贴 URL 即可下载，无需记忆任何参数
- **Profile 系统** — 不同下载场景对应不同配置，1080P 视频、纯音频、4K、B 站……一键切换，互不干扰
- **层次化配置** — 根配置管理通用参数，Profile 配置专注格式选择，子配置可覆盖根配置
- **智能格式选择** — 内置格式优先级策略，自动选最佳画质，自动合并视频与音频流
- **播放列表精细控制** — 支持下载整个列表、连续片段（起止索引）、任意指定集数（如 `1,3:5,7`）
- **保留音频开关** — 一键切换是否同时保留 m4a 音频文件，无需修改配置
- **自动管理依赖** — 安装脚本自动检测并配置 ffmpeg、yt-dlp，无需手动折腾环境
- **桌面快捷方式** — 安装后自动创建桌面快捷方式，双击即可启动
- **跨平台** — Windows / Linux / macOS 全支持，行为一致
- **一键更新 yt-dlp** — 菜单内直接更新到最新版，始终保持最佳兼容性

---

## 💡 设计理念

> **Easy yt-dlp 的作用是简化 yt-dlp 的配置。**

yt-dlp 功能强大，但参数繁多，每次下载都要拼命令行既低效又容易出错。Easy yt-dlp 的思路是：

- **你只配置一次**，把常用参数写进 Profile，之后每次下载都复用
- **不同需求用不同 Profile**，而不是每次手动改参数
- **工具只管它该管的**（播放列表控制、音频开关），其余完全交给你的配置

这样你既保留了 yt-dlp 的全部能力，又不必每次都和命令行打交道。

---

## ⚙️ 工作原理

```
用户输入 URL
      │
      ▼
Easy yt-dlp 读取配置
      │
      ├─ 加载根配置：~/.easy-ytdlp/config/base.conf
      │  （代理、浏览器、ffmpeg、输出路径等通用配置）
      │
      ├─ 加载 Profile 配置：~/.easy-ytdlp/profiles/<profile-id>/yt-dlp.conf
      │  （格式选择等特定配置，可覆盖根配置）
      │
      ├─ 附加运行时参数（播放列表控制、音频开关等）
      │
      ▼
拼装完整 yt-dlp 命令并执行
      │
      ▼
ffmpeg 自动合并视频 + 音频流（如需要）
      │
      ▼
文件保存到指定目录
```

配置存储在用户目录下，与项目代码完全分离，升级工具不影响你的配置。

---

## 🚀 快速开始

### 前置要求

- Python 3.10+
- Node.js（安装脚本依赖）

### 安装

```bash
# 1. 克隆项目
git clone https://github.com/xmakercn/easy-ytdlp.git
cd easy-ytdlp

# 2. 运行安装脚本
python install.py
# 选择 [1] 安装，按提示完成配置：
#   - 浏览器选择（用于 cookie）
#   - 视频保存路径
#   - 代理设置（不使用/默认/自定义）

# 3. 启动
# 方式一：双击桌面快捷方式「Easy yt-dlp」
# 方式二：命令行运行
easy-ytdlp
# （Windows 需重启终端或重新登录使环境变量生效）
```

### 免安装直接运行

```bash
cd src
python -m easy_ytdlp
```

### 卸载

```bash
python install.py
# 选择 [2] 卸载
```

---

## 📋 功能菜单

启动后显示当前 Profile 信息，然后进入主菜单：

| 选项 | 功能 |
|------|------|
| `1` | 下载单个视频 |
| `2` | 下载完整播放列表 |
| `3` | 下载播放列表连续片段（起止索引） |
| `4` | 下载播放列表指定集数（如 `1,3:5,7`） |
| `5` | 切换保留音频（开启后同时保留 m4a 音频文件） |
| `6` | 切换 Profile |
| `7` | 修改视频保存路径 |
| `8` | 更新 yt-dlp 到最新版 |
| `9` | 退出 |

---

## 🗂️ Profile 系统

### 概念

一个 **Profile** = 一套 yt-dlp 配置，对应一类下载需求：

| Profile 示例 | 用途 |
|---|---|
| `sys_default_1080P-mp4-lean` | 1080P mp4，不保留音频（默认） |
| `audio-only` | 仅下载音频，转为 mp3 |
| `bilibili-4K` | B 站 4K 专用配置 |

### 目录结构

```
~/.easy-ytdlp/
├── config/
│   └── base.conf               # 根配置（代理、浏览器、输出路径、ffmpeg等）
├── active_profile              # 当前激活的 Profile ID
└── profiles/
    ├── sys_default_1080P-mp4-lean/
    │   ├── yt-dlp.conf         # Profile 配置（通常只需格式配置）
    │   └── .meta               # Profile 名称和描述
    └── my-custom-profile/
        ├── yt-dlp.conf
        └── .meta
```

### 新建自定义 Profile

```bash
# 1. 创建目录（目录名即 Profile ID）
mkdir ~/.easy-ytdlp/profiles/audio-only

# 2. 创建 .meta
echo "name=audio-only" > ~/.easy-ytdlp/profiles/audio-only/.meta
echo "desc=仅下载音频，转换为 mp3 格式" >> ~/.easy-ytdlp/profiles/audio-only/.meta

# 3. 创建 yt-dlp.conf
# 通常只需填写格式相关参数，通用配置会自动从 base.conf 继承
echo '--format "ba/b"' > ~/.easy-ytdlp/profiles/audio-only/yt-dlp.conf
echo '--extract-audio' >> ~/.easy-ytdlp/profiles/audio-only/yt-dlp.conf
echo '--audio-format mp3' >> ~/.easy-ytdlp/profiles/audio-only/yt-dlp.conf
```

然后启动工具，选 `[6] 切换 Profile` 即可。

**提示**：Profile 配置会覆盖根配置。如果需要为特定 Profile 使用不同代理、浏览器或其他参数，可以在 Profile 的 yt-dlp.conf 中重新指定任意配置（播放列表相关参数除外，由工具自动管理）。

### 默认 Profile 说明

`sys_default_1080P-mp4-lean` 的配置：

| 配置项 | 值 |
|---|---|
| 视频格式 | `b[ext=mp4][height=1080]/bv[ext=mp4][height=1080]+ba[ext=m4a]/bv*+ba/b` |
| 音频保留 | 否（可通过选项 `[5]` 临时开启） |

**通用配置**（所有 Profile 共享，存储在 `config/base.conf`）：

| 配置项 | 值 |
|---|---|
| 浏览器 Cookie | 安装时选择（默认 Firefox） |
| 代理 | 安装时选择（默认不使用） |
| 播放列表 | 单 URL 默认禁用（选项 2-4 自动启用） |
| 输出路径 | 安装时指定（默认 ~/Downloads） |

---

## 📝 配置参考

### 配置文件层次

Easy yt-dlp 使用**层次化配置**：

- **根配置**（`config/base.conf`）：所有 Profile 共享的通用配置
- **子配置**（`profiles/<id>/yt-dlp.conf`）：Profile 特定配置，可覆盖根配置

### yt-dlp.conf 格式

每行一个参数，与 yt-dlp 命令行写法完全一致，`#` 开头为注释：

```ini
# 代理
--proxy=127.0.0.1:10808

# 浏览器 cookie（用于需要登录的网站）
--cookies-from-browser=firefox

# 视频格式
--format "bv*+ba/b"

# 嵌入字幕
--write-subs
--sub-langs zh-Hans,en

# 去除赞助商片段
--sponsorblock-remove sponsor
```

完整参数列表见 [yt-dlp 官方文档](https://github.com/yt-dlp/yt-dlp#usage-and-options)。

### 根配置参数（base.conf）

| 参数 | 说明 |
|---|---|
| `--proxy` | 代理地址 |
| `--cookies-from-browser` | 浏览器 cookie |
| `--output` | 输出路径模板 |
| `--ffmpeg-location` | ffmpeg 路径 |
| `--no-playlist` | 默认禁用播放列表 |

### Profile 配置参数（推荐）

| 参数 | 说明 |
|---|---|
| `--format` | 视频格式选择 |
| `--merge-output-format` | 合并输出格式 |
| `--sub-langs` / `--write-subs` | 字幕下载 |
| `--embed-thumbnail` | 嵌入封面 |
| `--sponsorblock-remove` | 去除赞助商片段 |

### 不应该写入配置的参数（由工具自动管理）

| 参数 | 原因 |
|---|---|
| `--output` | 由菜单选项 `[7]` 管理 |
| `--ffmpeg-location` | 由安装脚本自动配置 |
| `--no-playlist` / `--yes-playlist` | 由菜单选项 1-4 自动控制 |
| `--playlist-items` | 由菜单选项 3/4 自动传入 |
| `--extract-audio` / `--keep-video` | 由菜单选项 `[5]` 控制 |

---

## 🔄 更新 yt-dlp

```bash
# 方式一：菜单选项 [8]（推荐）
easy-ytdlp

# 方式二：直接 pip
pip install -U "yt-dlp[default,curl-cffi]"
```

---

## 📅 最新动态

### v1.0.0 · 2026-05-08

- 🎉 首次公开发布
- ✅ Profile 系统：多套配置独立管理，一键切换
- ✅ 层次化配置：根配置 + 子配置，灵活覆盖
- ✅ 播放列表精细下载（整列、片段、指定集数）
- ✅ 保留音频开关
- ✅ 跨平台安装脚本（Windows / Linux / macOS）
- ✅ 桌面快捷方式自动创建
- ✅ 一键更新 yt-dlp

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

- **Bug 报告**：请附上操作系统、Python 版本、完整错误信息
- **功能建议**：先开 Issue 讨论，避免重复劳动
- **代码贡献**：Fork → 新建分支 → 提交 PR，保持代码风格一致

### 版本管理

本项目使用自动语义化版本控制。提交 PR 时，请添加以下标签之一：
- `major` - 破坏性变更（1.0.0 → 2.0.0）
- `minor` - 新功能（1.0.0 → 1.1.0）
- `patch` - Bug 修复（1.0.0 → 1.0.1）

PR 合并后版本号将自动更新。详见 [VERSION_MANAGEMENT.md](docs/VERSION_MANAGEMENT.md)。

---

## ❓ 常见问题

**Q: 支持哪些网站？**  
A: 所有 yt-dlp 支持的网站，包括 YouTube、B 站、Twitter/X、Instagram 等，完整列表见 [yt-dlp 支持站点](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)。

**Q: 下载 YouTube 需要登录的内容怎么办？**  
A: 在 Profile 的 `yt-dlp.conf` 中配置 `--cookies-from-browser=firefox`（或 chrome），确保浏览器已登录对应账号。

**Q: 代理不生效？**  
A: 检查 `yt-dlp.conf` 中的 `--proxy` 地址是否正确，确认代理服务正在运行。

**Q: 如何下载 4K 视频？**  
A: 新建一个 Profile，在 `yt-dlp.conf` 中设置 `--format "bv[height=2160]+ba/bv*+ba/b"`，然后切换到该 Profile。



---

## 📄 许可证

本项目基于 [GNU General Public License v3.0](LICENSE) 开源。

```
Copyright (C) 2026  Easy yt-dlp Contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
```

---

<div align="center">

如果这个项目对你有帮助，请给一个 ⭐ Star，这是对开发者最大的鼓励！

</div>
