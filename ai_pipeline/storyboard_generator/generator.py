def generate_storyboard(scenes: list[dict]) -> list[dict]:
    """
    Convert scenes into detailed storyboard shots.
    """

    storyboard = []

    for scene in scenes:

        setting = scene.get("setting", "Story World")
        action = scene.get("action", scene.get("text", ""))
        characters = scene.get("characters", [])

        if characters:
            character_text = ", ".join(characters)
        else:
            character_text = "the main character"

        visual_description = (
            f"{character_text} in a {setting.lower()} setting. "
            f"The scene shows {action.lower()}"
        )

        storyboard.append({
            **scene,
            "visual_description": visual_description,
            "camera": "Medium cinematic shot",
            "camera_movement": "Slow forward movement",
            "lighting": "Natural cinematic lighting",
            "mood": "Calm and immersive",
            "duration_seconds": 3,
        })

    return storyboard
