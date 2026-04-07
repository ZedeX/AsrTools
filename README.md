# AsrTools

音视频转文字工具，支持多种 ASR 引擎。

## 功能

- **GUI 界面**：图形化操作，支持批量处理
- **命令行工具**：脚本化批量处理
- **多引擎支持**：必剪、剪映、快手 ASR 接口
- **多格式输出**：SRT、ASS、TXT 字幕格式
- **视频支持**：自动转换视频为音频（FFmpeg 自动下载）
- **多线程处理**：批量文件并行处理

## 快速开始

### 使用预构建版本

从 [Releases](https://github.com/ZedeX/AsrTools/releases) 下载对应系统的版本。

### 从源码运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行 GUI
python asr_gui.py

# 使用命令行
python cli.py video.mp4 -e JianYingASR -f srt
```

## 项目结构

```
AsrTools/
├── asr_gui.py          # GUI 主程序
├── cli.py              # 命令行工具
├── ffmpeg_manager.py   # FFmpeg 自动管理
├── bk_asr/             # ASR 引擎模块
│   ├── BcutASR.py
│   ├── JianYingASR.py
│   └── KuaiShouASR.py
├── asr_gui.spec        # PyInstaller GUI 配置
└── asr_cli.spec        # PyInstaller CLI 配置
```

## 构建

使用 PyInstaller 打包：

```bash
# GUI 版本
pyinstaller asr_gui.spec

# CLI 版本
pyinstaller asr_cli.spec
```

## 许可证

MIT License
