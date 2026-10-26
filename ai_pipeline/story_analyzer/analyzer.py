import re


STOP_WORDS = {
    "The", "A", "An", "In", "On", "At", "And",
    "But", "She", "He", "They", "It", "One"
}


def split_sentences(story: str) -> list[str]:
    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", story.strip())
        if sentence.strip()
    ]


def extract_characters(story: str) -> list[str]:
    """
    Simple MVP character extraction.
    Finds capitalized names from the story.
    """
    words = re.findall(r"\b[A-Z][a-z]{2,}\b", story)

    characters = []

    for word in words:
        if word not in STOP_WORDS and word not in characters:
            characters.append(word)

    return characters[:10]


def extract_settings(story: str) -> list[str]:
    """
    Detect common locations/settings from the story.
    """
    settings_map = {
        "forest": "Forest",
        "city": "City",
        "village": "Village",
        "school": "School",
        "house": "House",
        "home": "Home",
        "castle": "Castle",
        "beach": "Beach",
        "mountain": "Mountain",
        "garden": "Garden",
        "park": "Park",
        "street": "Street",
        "river": "River",
        "space": "Space",
    }

    story_lower = story.lower()

    settings = []

    for keyword, name in settings_map.items():
        if keyword in story_lower:
            settings.append(name)

    return settings


def extract_events(sentences: list[str]) -> list[str]:
    """
    For the MVP, each sentence is treated as an event.
    """
    return sentences[:10]


def analyze_story(story: str) -> dict:
    """
    Convert raw story text into structured information.
    """

    story = story.strip()

    sentences = split_sentences(story)

    words = re.findall(
        r"\b[A-Za-z][A-Za-z'-]*\b",
        story
    )

    characters = extract_characters(story)

    settings = extract_settings(story)

    events = extract_events(sentences)

    return {
        "story": story,
        "word_count": len(words),
        "sentence_count": len(sentences),
        "characters": characters,
        "settings": settings,
        "events": events,
    }