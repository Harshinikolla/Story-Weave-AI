def generate_animation_plan(
    scenes: list[dict],
    characters: list[dict] | None = None,
) -> list[dict]:
    """
    Create an animation plan for each storyboard scene.

    This is an MVP planning layer.
    Actual AI video generation can be connected later.
    """

    characters = characters or []

    animation_plan = []

    for scene in scenes:
        scene_number = scene.get("scene_number", 1)
        action = scene.get("action", scene.get("text", ""))
        duration = scene.get("duration_seconds", 3)

        scene_characters = scene.get("characters", [])

        character_animations = []

        for character_name in scene_characters:
            character_animations.append({
                "character": character_name,
                "movement": "Walk and interact with the scene",
                "motion_style": "Smooth 2D motion",
                "expression": "Curious",
            })

        animation_plan.append({
            "scene_number": scene_number,
            "action": action,
            "duration_seconds": duration,
            "character_animations": character_animations,
            "camera_animation": {
                "movement": scene.get(
                    "camera_movement",
                    "Slow forward movement"
                ),
                "style": "Cinematic",
            },
            "transition": "Smooth fade",
        })

    return animation_plan