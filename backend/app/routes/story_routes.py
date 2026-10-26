from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ai_pipeline.story_analyzer.analyzer import analyze_story
from ai_pipeline.character_generator.generator import generate_characters
from ai_pipeline.background_generator.generator import generate_backgrounds
from ai_pipeline.scene_generator.generator import generate_scenes
from ai_pipeline.storyboard_generator.generator import generate_storyboard
from ai_pipeline.animation_generator.generator import generate_animation_plan

from ai_pipeline.audio_generator.generator import (
    generate_audio_plan,
    generate_narration_audio,
)

from video_renderer.render import render_story_video
from backend.app.services.video_audio import merge_audio_with_video


router = APIRouter()


class StoryRequest(BaseModel):
    story: str = Field(min_length=10, max_length=10000)


@router.post("/generate")
def generate(request: StoryRequest):

    story = request.story.strip()

    if not story:
        raise HTTPException(
            status_code=400,
            detail="Story cannot be empty."
        )

    # -------------------------------------------------
    # 1. Analyze story
    # -------------------------------------------------

    analysis = analyze_story(story)

    # -------------------------------------------------
    # 2. Generate characters
    # -------------------------------------------------

    characters = generate_characters(
        analysis.get("characters", [])
    )

    # -------------------------------------------------
    # 3. Generate backgrounds
    # -------------------------------------------------

    backgrounds = generate_backgrounds(
        analysis.get("settings", [])
    )

    # -------------------------------------------------
    # 4. Generate scenes
    # -------------------------------------------------

    scenes = generate_scenes(
        story,
        analysis
    )

    # -------------------------------------------------
    # 5. Generate storyboard
    # -------------------------------------------------

    storyboard = generate_storyboard(
        scenes
    )

    # -------------------------------------------------
    # 6. Generate animation plan
    # -------------------------------------------------

    animation_plan = generate_animation_plan(
        storyboard,
        characters
    )

    # -------------------------------------------------
    # 7. Generate audio plan
    # -------------------------------------------------

    audio_plan = generate_audio_plan(
        storyboard
    )

    # -------------------------------------------------
    # 8. Render video
    # -------------------------------------------------

    video_filename = render_story_video(
        story,
        storyboard
    )

    video_path = (
        Path("storage")
        / "videos"
        / video_filename
    )

    # -------------------------------------------------
    # 9. Generate narration audio
    # -------------------------------------------------

    unique_id = uuid4().hex[:10]

    audio_filename = (
        f"narration_{unique_id}.mp3"
    )

    audio_path = generate_narration_audio(
        story,
        audio_filename
    )

    # -------------------------------------------------
    # 10. Merge video + narration
    # -------------------------------------------------

    final_video_filename = (
        f"story_with_audio_{unique_id}.mp4"
    )

    final_video_path = (
        Path("storage")
        / "videos"
        / final_video_filename
    )

    merge_audio_with_video(
        str(video_path),
        audio_path,
        str(final_video_path)
    )

    # -------------------------------------------------
    # 11. Return result
    # -------------------------------------------------

    return {
        "message": "Animation generated successfully.",

        "video_url": (
            f"/videos/{final_video_filename}"
        ),

        "audio_url": (
            f"/audio/{audio_filename}"
        ),

        "analysis": analysis,

        "characters": characters,

        "backgrounds": backgrounds,

        "scenes": storyboard,

        "animation_plan": animation_plan,

        "audio_plan": audio_plan,
    }


@router.post("/analyze")
def analyze(request: StoryRequest):

    return analyze_story(
        request.story
    )