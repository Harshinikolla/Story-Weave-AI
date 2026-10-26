from pathlib import Path
import subprocess

import imageio_ffmpeg


def merge_audio_with_video(
    video_path: str,
    audio_path: str,
    output_path: str,
) -> str:

    video = Path(video_path)
    audio = Path(audio_path)
    output = Path(output_path)

    if not video.exists():
        raise FileNotFoundError(f"Video not found: {video}")

    if not audio.exists():
        raise FileNotFoundError(f"Audio not found: {audio}")

    output.parent.mkdir(parents=True, exist_ok=True)

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    command = [
        ffmpeg,
        "-y",
        "-i", str(video),
        "-i", str(audio),
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        str(output),
    ]

    subprocess.run(
        command,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return str(output)