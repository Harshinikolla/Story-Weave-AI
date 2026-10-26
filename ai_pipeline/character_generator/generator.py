# def generate_characters(characters: list[str]) -> list[dict]:
#     """
#     Convert character names into structured character profiles.
#     """

#     character_profiles = []

#     for name in characters:
#         character_profiles.append({
#             "name": name,
#             "role": "Main Character",
#             "appearance": {
#                 "style": "Animated",
#                 "color_theme": "Bright",
#                 "design": "Friendly cartoon character",
#             },
#             "personality": [
#                 "Curious",
#                 "Brave",
#                 "Friendly",
#             ],
#             "animation_style": "Smooth 2D animation",
#         })

#     return character_profiles




import os
import base64
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# --------------------------------------------------
# PROJECT SETUP
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY missing in .env file")

client = OpenAI(api_key=api_key)

OUTPUT_DIR = PROJECT_ROOT / "storage" / "characters"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# CHARACTER PROFILE GENERATION
# --------------------------------------------------

def generate_characters(characters: list[str]) -> list[dict]:
    """
    Convert detected character names into character profiles.

    Each character gets a unique description that can later
    be used to generate an AI character image.
    """

    character_profiles = []

    for name in characters:

        character_profiles.append({
            "name": name,

            "role": "Story Character",

            "appearance": {
                "style": "2D animated character",
                "description": (
                    f"A visually distinctive animated character named {name}. "
                    "The appearance should match the story context."
                ),
            },

            "personality": [
                "Friendly",
                "Expressive",
                "Story-appropriate",
            ],

            "animation_style": "Smooth 2D animation",
        })

    return character_profiles


# --------------------------------------------------
# CHARACTER IMAGE GENERATION
# --------------------------------------------------

def generate_character_image(
    character_name: str,
    character_description: str,
) -> str:
    """
    Generate an AI image for a story character.

    The generated image is saved in:
    storage/characters/
    """

    prompt = (
        f"Create a full-body 2D animated story character named "
        f"{character_name}. "

        f"Character description: {character_description}. "

        "The character should be visually unique and clearly recognizable. "
        "Use a friendly high-quality animated movie style. "

        "Show the complete character from head to feet. "
        "Use a simple clean background. "

        "Do not include text, labels, captions, logos, or watermarks."
    )

    print(f"Generating character image for: {character_name}")

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
    )

    image_data = base64.b64decode(
        response.data[0].b64_json
    )

    safe_name = "".join(
        c for c in character_name.lower()
        if c.isalnum() or c in "_-"
    )

    if not safe_name:
        safe_name = "character"

    image_path = OUTPUT_DIR / f"{safe_name}_character.png"

    image_path.write_bytes(image_data)

    print(f"Character image saved: {image_path}")

    return str(image_path)


# --------------------------------------------------
# GENERATE ALL CHARACTER ASSETS
# --------------------------------------------------

def generate_character_assets(
    character_profiles: list[dict],
) -> list[dict]:
    """
    Generate an image for every character profile.

    Returns the character profiles with image paths attached.
    """

    generated_characters = []

    for character in character_profiles:

        name = character["name"]

        appearance = character.get("appearance", {})

        description = appearance.get(
            "description",
            f"Animated character named {name}"
        )

        image_path = generate_character_image(
            name,
            description,
        )

        generated_character = {
            **character,
            "image_path": image_path,
        }

        generated_characters.append(
            generated_character
        )

    return generated_characters