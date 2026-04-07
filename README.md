# AsrTools

音视频转文字工具，支持多种 ASR 引擎。

## 功能

- **GUI 界面**：图形化操作，支持批量处理
- **命令行工具**：脚本化批量处理
- **多引擎支持**：必剪、剪映、快手 ASR 接口
- **多格式输出**：SRT、ASS、TXT 字幕格式
- **视频支持**：自动转换视频为音频（FFmpeg 自动下载）
- **多线程处理**：批量文件并行处理
- **目录递归扫描**：自动查找处理目录下所有音视频文件

## 快速开始

### 使用预构建版本

从 [Releases](https://github.com/ZedeX/AsrTools/releases) 下载对应系统的版本。

### 从源码运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行 GUI
python asr_gui.py

# 使用命令行（默认处理当前目录）
python cli.py
```

## 命令行工具 (CLI) 使用说明

### 默认行为

不指定输入路径时，默认处理**当前目录及其子目录**下的所有音视频文件：
- 默认引擎：JianYingASR (J 接口)
- 默认输出格式：TXT
- 默认递归子目录：开启

### 用法

```
python cli.py [输入路径] [选项]
```

### 参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `input` | - | 输入文件或目录路径 | 当前目录 `.` |
| `--engine` | `-e` | ASR 引擎 (BcutASR/JianYingASR/KuaiShouASR/B/J/K) | `J` |
| `--format` | `-f` | 输出格式 (srt/ass/txt) | `txt` |
| `--output` | `-o` | 输出文件路径（仅单个文件时使用） | - |
| `--recursive` | `-r` | 递归处理子目录 | 开启 |
| `--no-recursive` | - | 不递归处理子目录 | - |
| `--cache` | `-c` | 使用缓存 | 关闭 |
| `--help` | `-h` | 显示帮助信息 | - |

### 示例

```bash
# 处理当前目录及其子目录下的所有文件（最常用）
python cli.py

# 处理指定目录
python cli.py ./videos

# 处理单个文件
python cli.py video.mp4

# 指定引擎和格式
python cli.py -e B -f srt

# 使用缓存
python cli.py -c

# 只处理当前目录，不递归子目录
python cli.py --no-recursive

# 完整示例
python cli.py ./media -e K -f ass -c
```

### 支持的文件格式

**音频**: `.mp3`, `.wav`, `.flac`, `.m4a`, `.aac`, `.ogg`, `.wma`

**视频**: `.mp4`, `.avi`, `.mov`, `.ts`, `.mkv`, `.wmv`, `.flv`, `.webm`, `.rmvb`

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
