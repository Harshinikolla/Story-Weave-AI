FPS = 12
WIDTH = 640
HEIGHT = 360
SECONDS_PER_SCENE = 3


def build_timeline(storyboard: list[dict]) -> list[dict]:
    timeline = []
    current = 0.0

    for scene in storyboard:
        duration = float(scene.get("duration_seconds", SECONDS_PER_SCENE))
        timeline.append({
            "scene_number": scene["scene_number"],
            "start": current,
            "end": current + duration,
            "duration": duration,
        })
        current += duration

    return timeline
