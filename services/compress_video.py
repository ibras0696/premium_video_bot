import os
import ffmpeg

INPUT_FOLDER = 'input_videos'
OUTPUT_FOLDER = 'compressed_videos'
TARGET_SIZE_MB = 50
MAX_BITRATE_KBPS = 5000  # Максимальный допустимый битрейт (можно поиграться)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def compress_video(input_path, output_path, target_size_mb):
    input_size = os.path.getsize(input_path) / (1024 * 1024)  # В МБ

    if input_size <= target_size_mb:
        print(f"[Пропущено] Уже меньше {target_size_mb} МБ: {input_path}")
        return

    # Примерное ограничение по битрейту
    bitrate_kbps = int((target_size_mb * 8192) / get_video_duration(input_path))
    bitrate_kbps = min(bitrate_kbps, MAX_BITRATE_KBPS)

    print(f"[Сжимаю] {os.path.basename(input_path)} до {bitrate_kbps} кбит/с")

    (
        ffmpeg
        .input(input_path)
        .output(output_path,
                **{
                    'c:v': 'libx264',
                    'b:v': f'{bitrate_kbps}k',
                    'preset': 'fast',
                    'c:a': 'aac',
                    'b:a': '128k',
                    'movflags': '+faststart'
                })
        .overwrite_output()
        .run()
    )


def get_video_duration(path):
    probe = ffmpeg.probe(path)
    return float(probe['format']['duration'])


def compress_all_videos():
    for file in os.listdir(INPUT_FOLDER):
        if file.endswith(('.mp4', '.mov', '.mkv', '.avi')):
            input_path = os.path.join(INPUT_FOLDER, file)
            output_path = os.path.join(OUTPUT_FOLDER, file)
            compress_video(input_path, output_path, TARGET_SIZE_MB)


if __name__ == '__main__':
    compress_all_videos()
