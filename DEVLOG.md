# 开发日志 (Development Log)

## [2026-10-28 10:08] 修复 yt-dlp 官方更新策略变更导致的更新报错

### 1. 任务目标与需求摘要
- **问题分析**：在菜单中选择选项 8（更新 yt-dlp 到最新稳定版）时，程序调用 `yt-dlp -U` 自更新命令，但由于通过 pip 安装的 yt-dlp 会被官方更新模块识别为 `VARIANT='pip'`，官方策略禁止 pip/wheel 安装的 yt-dlp 使用 `-U` 自更新命令覆盖自身，抛出错误：`ERROR: You installed yt-dlp with pip or using the wheel from PyPi; Use that to update`。同时菜单未校验更新返回值，在报错后仍错误显示“更新完成”。
- **目标**：调查官方更新策略机制，重构 yt-dlp 更新逻辑，支持智能识别 pip 与独立可执行程序（standalone binary）不同安装途径，采用对应的官方更新方式（pip 安装使用 `pip install -U yt-dlp[default,curl-cffi]`，独立二进制使用 `-U`），并提供降级容错及准确的成功/失败状态反馈。

### 2. 核心变更清单
- **模块/文件路径**：
  - `src/easy_ytdlp/downloader.py`：
    - 新增 `is_pip_ytdlp(cmd)` 检测函数：结合 `yt_dlp.version.VARIANT`、`UPDATE_HINT` 以及可执行文件与 Python 环境路径关系（`is_relative_to`），精准识别当前 yt-dlp 是否为 pip 安装；
    - 重构 `update_ytdlp() -> bool`：若为 pip 安装，调用 `[sys.executable, "-m", "pip", "install", "-U", "yt-dlp[default,curl-cffi]"]`，附带配置的代理参数；若为独立二进制则执行 `yt-dlp -U`；若自更新失败自动降级到 pip 尝试；更新函数返回布尔值代表更新成败。
  - `src/easy_ytdlp/menu.py`：
    - 选项 8 接收 `update_ytdlp()` 执行状态，成功时显示绿色“更新完成！”，失败时显示红色“更新失败”提示。
  - `src/easy_ytdlp/i18n_zh_CN.py`：
    - 新增 `"update_failed": "更新失败，请检查网络或代理设置！"` 键值。
  - `src/easy_ytdlp/i18n_en_US.py`：
    - 新增 `"update_failed": "Update failed! Please check network or proxy settings."` 键值。

### 3. 测试验证结果
- **安装源判断验证**：在当前环境执行 `is_pip_ytdlp()`，正确识别当前安装为 pip 安装（`is pip: True`）。
- **更新执行测试**：调用 `update_ytdlp()` 验证，成功通过 pip 将 `yt-dlp` 从 `2026.08.19` 升级到最新版本 `2026.10.26`，执行返回 `True`，不再出现 `ERROR: You installed yt-dlp with pip...`。
- **国际化测试**：测试中英文语言环境下 `update_failed` 与 `update_complete` 显示均正确无误。

### 4. Git 提交信息
- **Commit Message**：`fix(downloader): adapt to yt-dlp update policy for pip installations`
