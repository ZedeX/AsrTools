
**注意：更多强大功能已经在我另一个项目实现:**

 [VideoCaptioner](https://github.com/WEIFENG2333/VideoCaptioner) 基于 LLM 的智能字幕助手，无需GPU一键高质量字幕视频合成！支持生成、断句、优化、翻译全流程。让视频字幕制作简单高效！


# 🎤 AsrTools
**AsrTools** 是一款基于多种开源和商业 ASR（自动语音识别）引擎的桌面 GUI 应用程序，旨在帮助用户轻松将音频文件转换为文本字幕。它支持批量处理、多线程并发，并提供多种实用功能，提升用户体验和工作效率。

## 🌟 **特色功能**

- 🚀 **无需复杂配置**：无需 GPU 和繁琐的本地配置，小白也能轻松使用。
- 🖥️ **高颜值界面**：基于 **PyQt5** 和 **qfluentwidgets**，界面美观且用户友好。
- ⚡ **效率超人**：多线程并发 + 批量处理，文字转换快如闪电。
- 📄 **多格式支持**：支持生成 `.srt` 和 `.txt` 、`ass`字幕文件，满足不同需求。
- 🧹 **智能清理**：一键清理已完成或跳过的任务，保持列表整洁。
- ⏭️ **智能跳过**：自动跳过已存在输出文件的任务，避免重复处理。
- 🔄 **错误重试**：支持对失败任务进行重新处理，提升成功率。
- 📢 **完成通知**：全部任务处理完毕后显示持久化通知提醒用户。
- 📋 **实时日志**：新增 LOG 菜单，实时查看处理日志，便于调试和监控。

欢迎为项目给上一个 Star ⭐ 。

**主界面截图示例：**

<img src="resources/main_window-1.1.0.png" width="80%" alt="主界面">


### 🖥️ **快速上手**

1. **启动应用**：运行下载的可执行文件或通过命令行启动 GUI 界面。
2. **选择 ASR 引擎**：在下拉菜单中选择你需要使用的 ASR 引擎。
3. **添加文件**：点击“选择文件”按钮或将文件/文件夹拖拽到指定区域。
4. **开始处理**：点击“开始处理”按钮，程序将自动开始转换，并在完成后在原音频目录生成 `.srt` 或 `.txt` 字幕文件。（默认保持 3 个线程运行）

## 🛠️ **安装指南**

###  **1. 从发布版本安装**

我为 Windows 用户提供了打包好的[Release](https://github.com/WEIFENG2333/AsrTools/releases)版本，下载后解压即可直接使用，无需配置环境。

或者从网盘下载： [https://wwwm.lanzoue.com/iUJYZ2clk7xg](https://wwwm.lanzoue.com/iPKZV2eh5ina)

运行解压后的 `AsrTools.exe`，即可启动 GUI 界面。


###  **2. 从源码安装（开发者）**

项目的依赖仅仅为 `requests`。

如果您需要 GUI 界面，请额外安装 `PyQt5`, `qfluentwidgets`。

如果您想从源码运行，请按照以下步骤操作：

1. **克隆仓库并进入项目目录**

    ```bash
    git clone https://github.com/WEIFENG2333/AsrTools.git
    cd AsrTools
    ```

2. **安装依赖并运行**

    - **启动 GUI 界面**

        ```bash
        pip install -r requirements.txt
        python asr_gui.py
        ```
---

## 📦 **打包指南（生成可执行文件）**

如果您想将项目打包成独立的可执行文件（.exe），可以使用 **PyInstaller**。

1. **安装 PyInstaller**

    ```bash
    pip install pyinstaller
    ```

2. **打包应用（优化版）**

    ```bash
    pyinstaller --onedir --windowed \
    --hidden-import PyQt5.QtCore \
    --hidden-import PyQt5.QtGui \
    --hidden-import PyQt5.QtWidgets \
    --hidden-import qfluentwidgets \
    --exclude-module torch \
    --exclude-module torchvision \
    --exclude-module torchaudio \
    --exclude-module pandas \
    --exclude-module scipy \
    --exclude-module yaml \
    --exclude-module setuptools \
    --exclude-module pywin32 \
    --exclude-module Pythonwin \
    --exclude-module markupsafe \
    --exclude-module PIL \
    --exclude-module dateutil \
    --exclude-module pytz \
    --exclude-module google \
    asr_gui.py
    ```

    这个命令排除了常见的多余模块（如 torch、pandas、scipy 等），大幅减小打包大小。运行后检查 `dist/asr_gui/_internal` 目录，如果仍有不需要的模块，添加更多 `--exclude-module`。

3. **添加 ffmpeg**

    由于应用需要调用外部 ffmpeg 进行视频转换，PyInstaller 不会自动包含它。您需要手动下载 ffmpeg 并添加到打包目录：

    - 下载 ffmpeg（Windows 版本）：从 [ffmpeg.org](https://ffmpeg.org/download.html) 或其他来源获取 `ffmpeg.exe`。
    - 将 `ffmpeg.exe` 复制到 `dist/asr_gui/` 目录中。
    - 或者，将 ffmpeg 的 bin 目录添加到系统 PATH。

4. **运行生成的可执行文件**

    在 `dist/asr_gui/` 目录下找到 `asr_gui.exe`，双击运行。如果 ffmpeg 在目录中，应用会自动使用它进行视频转换。

**注意**：
- 使用 `--onedir` 生成的目录大小通常小于 `--onefile`，便于管理。
- 确保 ffmpeg 版本兼容（推荐最新稳定版）。
- 如果仍有问题，检查 exe 运行时的错误日志。

---

## 日志
-  **（v1.2.0）新增任务管理功能**：添加清理已完成任务按钮、智能跳过重复文件、错误任务重试、完成通知和实时日志查看，提升用户体验和效率。
-  **（v1.1.0）已经增加视频文件支持🎥**：支持直接导入视频文件，自动转换为音频进行处理，无需手动转换。

## 📬 **联系与支持**

- **Issues**：[提交问题](https://github.com/WEIFENG2333/AsrTools/issues)

感谢您使用 **AsrTools**！🎉  

目前项目的相关调用和GUI页面的功能仍在不断完善中...

希望这款工具能为您带来便利。😊

---
## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=WEIFENG2333/AsrTools&type=Date)](https://star-history.com/#WEIFENG2333/AsrTools&Date)
