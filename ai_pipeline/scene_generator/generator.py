def generate_scenes(story: str, analysis: dict) -> list[dict]:
    events = analysis.get("events", [])
    characters = analysis.get("characters", [])
    settings = analysis.get("settings", [])

    default_setting = settings[0] if settings else "Story World"

    scenes = []

    for index, event in enumerate(events, start=1):
        event_lower = event.lower()

        # Identify characters mentioned in this event
        scene_characters = [
            character
            for character in characters
            if character.lower() in event_lower
        ]

        if not scene_characters:
            scene_characters = characters

        # Detect the setting separately for each scene
        scene_setting = default_setting

        setting_keywords = {
            "forest": "Forest",
            "tree": "Forest",
            "woods": "Forest",
            "city": "City",
            "village": "Village",
            "school": "School",
            "house": "House",
            "home": "Home",
            "castle": "Castle",
            "beach": "Beach",
            "sea": "Beach",
            "ocean": "Beach",
            "mountain": "Mountain",
            "garden": "Garden",
            "park": "Park",
            "street": "Street",
            "river": "River",
            "space": "Space",
        }

        for keyword, setting_name in setting_keywords.items():
            if keyword in event_lower:
                scene_setting = setting_name
                break

        scenes.append({
            "scene_number": index,
            "text": event,
            "characters": scene_characters,
            "setting": scene_setting,
            "action": event,
        })

    return scenes