import subprocess

input_file = "start_videio.mp4"
output_file = "new_start_videio.mp4"

subprocess.run([
    "ffmpeg", "-i", input_file,
    "-vf", "scale=-2:720",  # Масштабируем высоту до 720px, ширина автоматически (-2 = кратно 2)
    "-c:v", "libx264",
    "-b:v", "2400k",  # видео битрейт
    "-preset", "slow",
    "-c:a", "aac",
    "-b:a", "128k",  # аудио битрейт
    "-movflags", "+faststart",  # нужно для Telegram
    output_file
])

# print(f"Видео успешно обработано и сохранено как {output_file}")
