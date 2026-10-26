
import math
import uuid
import textwrap
from pathlib import Path

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont


# --------------------------------------------------
# Configuration
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "storage" / "videos"
ASSETS_DIR = ROOT / "frontend" / "public" / "assets"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

WIDTH = 1280
HEIGHT = 720
FPS = 24
SECONDS_PER_SCENE = 3

SCENE_ASSETS = {
    1: ASSETS_DIR / "scenes" / "scene1" / "maya_walk.png",
    2: ASSETS_DIR / "scenes" / "scene2" / "maya_discover.png",
    3: ASSETS_DIR / "scenes" / "scene3" / "maya_reaction.png",
}

FALLBACK_MAYA_PATH = ASSETS_DIR / "maya.png"


# --------------------------------------------------
# Fonts
# --------------------------------------------------

def get_font(size):
    candidates = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ]

    for font_path in candidates:
        try:
            return ImageFont.truetype(font_path, size)
        except OSError:
            pass

    return ImageFont.load_default()


TITLE_FONT = get_font(34)
TEXT_FONT = get_font(25)
SMALL_FONT = get_font(19)


# --------------------------------------------------
# Basic backgrounds
# --------------------------------------------------

def draw_default_background(draw):
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill="#9BDCF5")
    draw.rectangle((0, 430, WIDTH, HEIGHT), fill="#76B96B")


def draw_forest(draw, frame_index=0):
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill="#9BDCF5")
    draw.ellipse((1000, 55, 1110, 165), fill="#FFD966")
    draw.rectangle((0, 350, WIDTH, HEIGHT), fill="#80B96C")

    for i in range(9):
        x = i * 155 - 20
        sway = int(4 * math.sin(frame_index / 8 + i))

        draw.rectangle(
            (x + 48 + sway, 270, x + 70 + sway, 485),
            fill="#795438",
        )

        draw.ellipse(
            (x, 175, x + 145, 350),
            fill="#368653",
        )

        draw.ellipse(
            (x + 18, 205, x + 125, 325),
            fill="#48A35B",
        )

    draw.polygon(
        [(450, 720), (830, 720), (710, 410), (570, 410)],
        fill="#CDB58A",
    )


def draw_city(draw, frame_index=0):
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill="#9BDCF5")
    draw.rectangle((0, 500, WIDTH, HEIGHT), fill="#777D85")

    buildings = [
        (30, 240, 190, 500),
        (210, 160, 370, 500),
        (390, 290, 540, 500),
        (760, 190, 920, 500),
        (940, 120, 1110, 500),
        (1130, 250, 1260, 500),
    ]

    for x1, y1, x2, y2 in buildings:
        draw.rectangle(
            (x1, y1, x2, y2),
            fill="#7387A1",
        )

        for x in range(x1 + 18, x2 - 10, 35):
            for y in range(y1 + 20, y2 - 25, 45):
                draw.rectangle(
                    (x, y, x + 15, y + 22),
                    fill="#FFE7A3",
                )

    draw.line((0, 610, WIDTH, 610), fill="white", width=5)


def draw_beach(draw, frame_index=0):
    draw.rectangle((0, 0, WIDTH, 400), fill="#80D7F4")
    draw.rectangle((0, 400, WIDTH, 545), fill="#35B8C5")
    draw.rectangle((0, 545, WIDTH, HEIGHT), fill="#F1D49A")

    for i in range(4):
        y = 425 + i * 30
        offset = int(15 * math.sin(frame_index / 8 + i))

        draw.arc(
            (100 + offset, y, 1180 + offset, y + 35),
            180,
            350,
            fill="white",
            width=4,
        )

    draw.ellipse((990, 55, 1100, 165), fill="#FFD966")


def draw_mountain(draw, frame_index=0):
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill="#A8DFF5")

    draw.polygon(
        [(0, 440), (260, 100), (520, 440)],
        fill="#8AA9B5",
    )
    draw.polygon(
        [(300, 450), (670, 70), (1010, 450)],
        fill="#6F929F",
    )
    draw.polygon(
        [(760, 450), (1050, 160), (1280, 450)],
        fill="#91ACB5",
    )

    draw.polygon(
        [(260, 100), (210, 170), (285, 150), (320, 180)],
        fill="white",
    )
    draw.polygon(
        [(670, 70), (605, 145), (680, 125), (740, 155)],
        fill="white",
    )

    draw.rectangle((0, 450, WIDTH, HEIGHT), fill="#75AA72")


# --------------------------------------------------
# Additional backgrounds
# --------------------------------------------------

def draw_village(draw):
    draw_default_background(draw)

    # Village path
    draw.polygon(
        [(470, 720), (820, 720), (700, 420), (590, 420)],
        fill="#D7BD91",
    )

    # Village houses
    houses = [
        (100, 330),
        (330, 360),
        (850, 345),
        (1050, 310),
    ]

    for x, y in houses:
        draw.rectangle(
            (x, y, x + 145, y + 145),
            fill="#E8C58A",
            outline="#805334",
            width=3,
        )

        draw.polygon(
            [
                (x - 15, y),
                (x + 72, y - 75),
                (x + 160, y),
            ],
            fill="#A64B35",
        )

        draw.rectangle(
            (x + 55, y + 75, x + 90, y + 145),
            fill="#805334",
        )

        draw.rectangle(
            (x + 15, y + 30, x + 45, y + 60),
            fill="#A9E2F5",
        )


def draw_river(draw, frame_index=0):
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill="#9BDCF5")
    draw.rectangle((0, 350, WIDTH, HEIGHT), fill="#79B96C")

    # Curved-looking river using polygons
    draw.polygon(
        [
            (430, 720),
            (850, 720),
            (740, 520),
            (880, 400),
            (580, 400),
            (660, 540),
        ],
        fill="#298FC2",
    )

    for i in range(7):
        y = 460 + i * 35
        offset = int(15 * math.sin(frame_index / 5 + i))

        draw.line(
            (610 + offset, y, 780 + offset, y + 5),
            fill="#B6E8FF",
            width=4,
        )


def draw_school(draw):
    draw_default_background()

    draw.rectangle(
        (350, 240, 930, 530),
        fill="#F0D39A",
        outline="#8B6A45",
        width=4,
    )

    draw.polygon(
        [(320, 240), (640, 120), (960, 240)],
        fill="#B84D42",
    )

    draw.rectangle(
        (590, 390, 690, 530),
        fill="#805334",
    )

    for x in [410, 500, 735, 825]:
        draw.rectangle(
            (x, 290, x + 55, 350),
            fill="#A9E2F5",
            outline="#FFFFFF",
            width=3,
        )

    draw.rectangle(
        (500, 180, 780, 220),
        fill="#FFFFFF",
        outline="#8B6A45",
        width=2,
    )
    draw.text(
        (535, 185),
        "SCHOOL",
        font=TEXT_FONT,
        fill="#24364B",
    )


def draw_house(draw):
    draw_default_background()

    draw.rectangle(
        (350, 280, 900, 600),
        fill="#F2D0A0",
        outline="#805334",
        width=4,
    )

    draw.polygon(
        [(300, 285), (625, 100), (950, 285)],
        fill="#B84D42",
    )

    draw.rectangle(
        (560, 420, 690, 600),
        fill="#805334",
    )

    for x in [410, 740]:
        draw.rectangle(
            (x, 340, x + 100, 425),
            fill="#A9E2F5",
            outline="#FFFFFF",
            width=4,
        )


def draw_garden(draw, frame_index=0):
    draw_default_background()

    for i in range(8):
        x = 100 + i * 150
        y = 400 + int(5 * math.sin(frame_index / 6 + i))

        draw.line(
            (x, y, x, y + 100),
            fill="#277A3B",
            width=5,
        )

        draw.ellipse(
            (x - 25, y - 25, x + 5, y + 5),
            fill="#FF83AD",
        )
        draw.ellipse(
            (x - 5, y - 30, x + 25, y),
            fill="#FFD966",
        )
        draw.ellipse(
            (x - 20, y - 5, x + 10, y + 25),
            fill="#A88BEE",
        )


def draw_background(draw, setting, frame_index, scene_number, scene_text=""):
    setting = str(setting).lower()
    scene_text = str(scene_text).lower()

    # If setting was not detected, try detecting it from the scene text.
    combined = f"{setting} {scene_text}"

    if "forest" in combined or "woods" in combined or "woodland" in combined:
        draw_forest(draw, frame_index)

    elif "city" in combined or "street" in combined:
        draw_city(draw, frame_index)

    elif any(word in combined for word in ["beach", "ocean", "seaside", "sea"]):
        draw_beach(draw, frame_index)

    elif any(word in combined for word in ["mountain", "mountains"]):
        draw_mountain(draw, frame_index)

    elif "village" in combined:
        draw_village(draw)

    elif "river" in combined:
        draw_river(draw, frame_index)

    elif any(word in combined for word in ["school", "classroom"]):
        draw_school(draw)

    elif any(word in combined for word in ["house", "home", "castle"]):
        draw_house(draw)

    elif any(word in combined for word in ["garden", "park"]):
        draw_garden(draw, frame_index)

    else:
        draw_default_background()

    # Draw a magical tree only when the story mentions one.
    if any(
        phrase in scene_text
        for phrase in [
            "glowing tree",
            "magical tree",
            "enchanted tree",
        ]
    ):
        draw_glowing_tree(draw, frame_index)


# --------------------------------------------------
# Magical tree animation
# --------------------------------------------------

def draw_glowing_tree(draw, frame_index):
    tree_x = 900
    tree_y = 330

    pulse = int(8 + 5 * math.sin(frame_index / 5))

    draw.ellipse(
        (
            tree_x - 100 - pulse,
            tree_y - 160 - pulse,
            tree_x + 120 + pulse,
            tree_y + 100 + pulse,
        ),
        fill="#B5F6CB",
    )

    draw.rectangle(
        (tree_x - 18, tree_y + 20, tree_x + 22, tree_y + 180),
        fill="#805334",
    )

    draw.ellipse(
        (tree_x - 105, tree_y - 105, tree_x + 100, tree_y + 80),
        fill="#39B96D",
    )

    draw.ellipse(
        (tree_x - 65, tree_y - 150, tree_x + 80, tree_y + 35),
        fill="#69E89A",
    )

    for i in range(12):
        angle = frame_index * 0.10 + i * (math.pi / 6)
        radius = 80 + 18 * math.sin(frame_index / 6 + i)

        x = int(tree_x + math.cos(angle) * radius)
        y = int(tree_y - 40 + math.sin(angle) * radius)

        size = 3 + (i % 3)

        draw.ellipse(
            (x - size, y - size, x + size, y + size),
            fill="#FFF4A3",
        )


# --------------------------------------------------
# Character loading
# --------------------------------------------------

def load_maya(scene_number=1):
    maya_path = SCENE_ASSETS.get(
        scene_number,
        FALLBACK_MAYA_PATH,
    )

    if not maya_path.exists():
        maya_path = FALLBACK_MAYA_PATH

    if not maya_path.exists():
        print("WARNING: Maya image not found:", maya_path)
        return None

    try:
        with Image.open(maya_path) as image:
            return image.convert("RGBA")
    except Exception as error:
        print("Could not load Maya image:", error)
        return None


# --------------------------------------------------
# Character movement
# --------------------------------------------------

def draw_character(image, scene, frame_index):
    scene_number = int(scene.get("scene_number", 1))
    character = load_maya(scene_number)

    if character is None:
        return

    t = frame_index / FPS
    original_height = 250
    bounce = int(6 * math.sin(t * 8))

    action_text = str(scene.get("action", scene.get("text", ""))).lower()

    # Choose a simple movement based on the scene description.
    if any(word in action_text for word in ["run", "running", "ran", "chase"]):
        horizontal_offset = int(75 * math.sin(t * 4))
        scale = 1.0

    elif any(word in action_text for word in ["discover", "found", "finds", "find", "sees", "saw"]):
        horizontal_offset = int(45 + 25 * math.sin(t * 2))
        scale = 1.0 + 0.025 * math.sin(t * 3)

    elif any(word in action_text for word in ["sit", "sits", "sat", "rest"]):
        horizontal_offset = int(5 * math.sin(t * 2))
        scale = 0.95

    elif any(word in action_text for word in ["dance", "dances", "dancing"]):
        horizontal_offset = int(40 * math.sin(t * 5))
        scale = 1.0 + 0.04 * math.sin(t * 5)

    elif any(word in action_text for word in ["sleep", "sleeps", "sleeping"]):
        horizontal_offset = 0
        scale = 0.92

    else:
        horizontal_offset = int(35 * math.sin(t * 2.5))
        scale = 1.0

    character_height = max(1, int(original_height * scale))
    ratio = character_height / character.height
    character_width = max(1, int(character.width * ratio))

    character = character.resize(
        (character_width, character_height),
        Image.Resampling.LANCZOS,
    )

    if any(
        word in action_text
        for word in ["discover", "found", "finds", "find", "sees", "saw"]
    ):
        base_x = WIDTH // 2 - character_width // 2 - 150
    else:
        base_x = WIDTH // 2 - character_width // 2

    x = base_x + horizontal_offset
    y = HEIGHT - character_height - 25 + bounce

    x = max(0, min(x, WIDTH - character_width))
    y = max(0, min(y, HEIGHT - character_height))

    image.alpha_composite(character, (x, y))


# --------------------------------------------------
# Story text panel
# --------------------------------------------------

def draw_story_panel(draw, scene):
    text = str(scene.get("text", ""))
    scene_number = scene.get("scene_number", 1)
    setting = str(scene.get("setting", "Story scene"))

    draw.rounded_rectangle(
        (35, 25, WIDTH - 35, 125),
        radius=20,
        fill="#182638",
        outline="#FFFFFF",
        width=2,
    )

    draw.text(
        (60, 40),
        f"Scene {scene_number} - {setting}",
        font=TITLE_FONT,
        fill="#FFE28A",
    )

    short_text = textwrap.shorten(
        text,
        width=105,
        placeholder="...",
    )

    draw.text(
        (60, 85),
        short_text,
        font=SMALL_FONT,
        fill="white",
    )


# --------------------------------------------------
# Create one animation frame
# --------------------------------------------------

def create_frame(scene, frame_index):
    scene_number = int(scene.get("scene_number", 1))
    setting = scene.get("setting", "Story World")
    scene_text = scene.get("text", "")

    image = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (135, 206, 235, 255),
    )

    draw = ImageDraw.Draw(image)

    draw_background(
        draw,
        setting,
        frame_index,
        scene_number,
        scene_text,
    )

    draw_character(
        image,
        scene,
        frame_index,
    )

    draw = ImageDraw.Draw(image)
    draw_story_panel(draw, scene)

    return np.asarray(image.convert("RGB"))


# --------------------------------------------------
# Render complete story video
# --------------------------------------------------

def render_story_video(story, storyboard):
    if not storyboard:
        raise ValueError("No scenes available to render.")

    filename = f"story_{uuid.uuid4().hex[:10]}.mp4"
    output_path = OUTPUT_DIR / filename

    writer = imageio.get_writer(
        str(output_path),
        fps=FPS,
        codec="libx264",
        pixelformat="yuv420p",
        macro_block_size=1,
    )

    try:
        for scene in storyboard:
            scene_number = int(scene.get("scene_number", 1))

            duration = float(
                scene.get(
                    "duration_seconds",
                    SECONDS_PER_SCENE,
                )
            )

            total_frames = max(1, int(duration * FPS))

            print(
                f"Rendering scene {scene_number}: "
                f"{total_frames} frames"
            )

            for frame_index in range(total_frames):
                frame = create_frame(scene, frame_index)
                writer.append_data(frame)

    finally:
        writer.close()

    print(f"Video saved: {output_path}")

    return filename
