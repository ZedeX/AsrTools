#!/usr/bin/env python3
"""
ASRTools 命令行工具 v1.3.0

使用方法:
    python cli.py <输入文件> [选项]

选项:
    -e, --engine ENGINE    ASR 引擎 (BcutASR, JianYingASR, KuaiShouASR)
                           默认: JianYingASR
    -f, --format FORMAT    输出格式 (srt, ass, txt)
                           默认: srt
    -o, --output FILE      输出文件路径 (可选)
    -c, --cache            使用缓存 (可选)
    -h, --help             显示帮助信息

示例:
    python cli.py video.mp4
    python cli.py audio.mp3 -e BcutASR -f txt
    python cli.py input.wav -o output.srt -c
"""

import argparse
import logging
import os
import sys
from pathlib import Path

# 导入 ASR 引擎
from bk_asr import BcutASR, JianYingASR, KuaiShouASR

# 导入 FFmpeg 管理器
from ffmpeg_manager import get_ffmpeg_manager, get_ffmpeg_path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def video2audio(input_file: str, output: str = "") -> bool:
    """使用ffmpeg将视频转换为音频"""
    import platform
    import subprocess

    ffmpeg_mgr = get_ffmpeg_manager()

    # 检查 ffmpeg
    if not ffmpeg_mgr.is_ffmpeg_available():
        logging.info("未找到 FFmpeg，尝试自动下载...")
        print("\n" + "=" * 60)
        print("FFmpeg 未找到")
        print("正在从 GitHub (BtbN/FFmpeg-Builds) 自动下载...")
        print("=" * 60 + "\n")

        def show_progress(p):
            print(f"\r下载进度: [{'#' * (p // 5)}{' ' * (20 - p // 5)}] {p:3d}%", end='', flush=True)

        def show_status(msg):
            print(f"\n{msg}")

        success = ffmpeg_mgr.download_ffmpeg(
            progress_callback=show_progress,
            status_callback=show_status
        )

        if not success:
            print("\n\n错误：FFmpeg 下载失败！")
            print("\n请手动下载 FFmpeg：")
            print("1. 访问 https://github.com/BtbN/FFmpeg-Builds/releases")
            print("2. 下载对应系统的 ffmpeg")
            print("3. 将 ffmpeg (或 ffmpeg.exe) 放置在程序目录或添加到 PATH\n")
            return False

        print("\nFFmpeg 下载成功！\n")

    # 创建output目录
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output = str(output)

    # 获取 ffmpeg 路径
    ffmpeg_path = get_ffmpeg_path()
    if not ffmpeg_path:
        return False

    cmd = [
        ffmpeg_path,
        '-i', input_file,
        '-ac', '1',
        '-f', 'mp3',
        '-af', 'aresample=async=1',
        '-y',
        output
    ]

    # 构建 subprocess.run 的参数字典
    kwargs = {
        'capture_output': True,
        'check': True,
        'encoding': 'utf-8',
        'errors': 'replace'
    }

    # 在 Windows 上添加隐藏窗口的配置
    if platform.system() == 'Windows':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        kwargs['startupinfo'] = startupinfo
        kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW

    result = subprocess.run(cmd, **kwargs)

    if result.returncode == 0 and Path(output).is_file():
        return True
    else:
        return False


def get_engine_class(engine_name):
    """根据引擎名称获取引擎类"""
    engines = {
        'BcutASR': BcutASR,
        'JianYingASR': JianYingASR,
        'KuaiShouASR': KuaiShouASR,
        'bcut': BcutASR,
        'jianying': JianYingASR,
        'kuaishou': KuaiShouASR,
        'B': BcutASR,
        'J': JianYingASR,
        'K': KuaiShouASR,
    }
    return engines.get(engine_name, JianYingASR)


def main():
    parser = argparse.ArgumentParser(
        description='ASRTools 命令行工具 v1.3.0 - 音视频转文字',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s video.mp4
  %(prog)s audio.mp3 -e BcutASR -f txt
  %(prog)s input.wav -o output.srt -c
        """
    )

    parser.add_argument('input', help='输入音视频文件路径')
    parser.add_argument(
        '-e', '--engine',
        default='JianYingASR',
        help='ASR 引擎 (BcutASR, JianYingASR, KuaiShouASR) 默认: JianYingASR'
    )
    parser.add_argument(
        '-f', '--format',
        default='srt',
        choices=['srt', 'ass', 'txt'],
        help='输出格式 (srt, ass, txt) 默认: srt'
    )
    parser.add_argument(
        '-o', '--output',
        help='输出文件路径 (可选)'
    )
    parser.add_argument(
        '-c', '--cache',
        action='store_true',
        help='使用缓存 (可选)'
    )

    args = parser.parse_args()

    # 检查输入文件是否存在
    input_path = Path(args.input)
    if not input_path.exists():
        logging.error(f"错误: 文件不存在: {args.input}")
        sys.exit(1)

    # 确定输出路径
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix(f'.{args.format.lower()}')

    # 检查文件类型，如果不是音频则转换
    audio_path = str(input_path)
    temp_audio = None
    audio_exts = ['.mp3', '.wav', '.flac', '.m4a']

    if not any(input_path.suffix.lower() == ext for ext in audio_exts):
        logging.info("正在转换视频为音频...")
        temp_audio = str(input_path.with_suffix('.mp3'))
        if not video2audio(str(input_path), temp_audio):
            logging.error("错误: 音频转换失败，请确保已安装 ffmpeg")
            sys.exit(1)
        audio_path = temp_audio

    try:
        # 获取引擎类
        engine_class = get_engine_class(args.engine)
        logging.info(f"使用引擎: {engine_class.__name__}")

        # 初始化 ASR
        asr = engine_class(audio_path, use_cache=args.cache)

        # 运行识别
        logging.info("开始语音识别...")
        result = asr.run()

        # 导出结果
        save_ext = args.format.lower()
        if save_ext == 'srt':
            result_text = result.to_srt()
        elif save_ext == 'ass':
            result_text = result.to_ass()
        elif save_ext == 'txt':
            result_text = result.to_txt()
        else:
            result_text = result.to_srt()

        # 保存文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result_text)

        logging.info(f"处理完成! 输出文件: {output_path}")

    except Exception as e:
        logging.error(f"处理出错: {str(e)}")
        sys.exit(1)
    finally:
        # 清理临时音频文件
        if temp_audio and Path(temp_audio).exists():
            try:
                Path(temp_audio).unlink()
            except Exception:
                pass


if __name__ == '__main__':
    main()
