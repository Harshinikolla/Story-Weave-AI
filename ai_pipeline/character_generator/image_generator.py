
import os
import base64
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY missing in .env file")

client = OpenAI(api_key=api_key)

OUTPUT_DIR = PROJECT_ROOT / "storage" / "characters"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_character_image(
    character_name: str,
    character_description: str,
) -> str:
    prompt = (
        f"Create a full-body digital illustration of {character_name}. "
        f"Character description: {character_description}. "
        "Show the entire person from head to feet, with a clean "
        "background, suitable for an animated story video."
    )

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
    )

    image_data = base64.b64decode(response.data[0].b64_json)

    safe_name = "".join(
        c for c in character_name.lower()
        if c.isalnum() or c in "_-"
    ) or "character"

    image_path = OUTPUT_DIR / f"{safe_name}_character.png"
    image_path.write_bytes(image_data)

    return str(image_path)