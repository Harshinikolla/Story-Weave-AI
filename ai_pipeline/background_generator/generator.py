def generate_backgrounds(settings: list[str]) -> list[dict]:
    """
    Convert detected settings into structured background descriptions.
    """

    background_profiles = []

    background_map = {
        "Forest": {
            "environment": "Dense green forest",
            "elements": [
                "Trees",
                "Grass",
                "Bushes",
                "Sunlight",
            ],
            "atmosphere": "Peaceful and magical",
        },
        "City": {
            "environment": "Modern city",
            "elements": [
                "Buildings",
                "Roads",
                "Street lights",
                "Cars",
            ],
            "atmosphere": "Busy and energetic",
        },
        "Village": {
            "environment": "Quiet village",
            "elements": [
                "Small houses",
                "Trees",
                "Dirt roads",
                "Fields",
            ],
            "atmosphere": "Calm and peaceful",
        },
        "Beach": {
            "environment": "Sunny beach",
            "elements": [
                "Ocean",
                "Sand",
                "Palm trees",
                "Waves",
            ],
            "atmosphere": "Relaxing and bright",
        },
        "Mountain": {
            "environment": "Mountain landscape",
            "elements": [
                "Mountains",
                "Rocks",
                "Trees",
                "Clouds",
            ],
            "atmosphere": "Grand and adventurous",
        },
        "School": {
            "environment": "School campus",
            "elements": [
                "Classrooms",
                "Desks",
                "Blackboards",
                "Students",
            ],
            "atmosphere": "Friendly and educational",
        },
        "House": {
            "environment": "Cozy house",
            "elements": [
                "Furniture",
                "Windows",
                "Doors",
                "Lights",
            ],
            "atmosphere": "Warm and comfortable",
        },
        "Home": {
            "environment": "Comfortable home",
            "elements": [
                "Furniture",
                "Sofa",
                "Windows",
                "Lights",
            ],
            "atmosphere": "Warm and peaceful",
        },
    }

    for setting in settings:

        background = background_map.get(
            setting,
            {
                "environment": setting,
                "elements": [
                    "Environment details",
                    "Lighting",
                    "Objects",
                ],
                "atmosphere": "Natural",
            },
        )

        background_profiles.append({
            "setting": setting,
            "environment": background["environment"],
            "elements": background["elements"],
            "atmosphere": background["atmosphere"],
            "style": "2D animated background",
        })

    return background_profiles
