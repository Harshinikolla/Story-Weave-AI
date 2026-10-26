from pathlib import Path
from gtts import gTTS


ROOT = Path(__file__).resolve().parents[2]
AUDIO_DIR = ROOT / "storage" / "audio"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def generate_narration_audio(
    text: str,
    filename: str = "narration.mp3",
) -> str:
    """
    Convert narration text into an MP3 audio file using gTTS.
    """

    text = text.strip()

    if not text:
        raise ValueError("Narration text cannot be empty.")

    output_path = AUDIO_DIR / filename

    tts = gTTS(
        text=text,
        lang="en",
        slow=False,
    )

    tts.save(str(output_path))

    return str(output_path)


def generate_audio_plan(
    scenes: list[dict],
) -> list[dict]:
    """
    Generate the audio plan for each scene.
    """

    audio_plan = []

    for scene in scenes:
        scene_number = scene.get("scene_number", 1)
        text = scene.get("text", "")
        duration = scene.get("duration_seconds", 3)

        audio_plan.append({
            "scene_number": scene_number,
            "dialogue": text,
            "narration": text,
            "voice": "Default narrator",
            "voice_style": "Warm and friendly",
            "sound_effects": [
                "Ambient environment sound"
            ],
            "background_music": "Soft cinematic music",
            "duration_seconds": duration,
        })

    return audio_plan