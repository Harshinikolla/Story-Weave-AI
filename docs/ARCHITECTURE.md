# StoryWeave AI Architecture

## Current MVP flow

Story text
→ FastAPI API
→ Story Analyzer
→ Scene Generator
→ Storyboard Generator
→ Procedural Video Renderer
→ MP4 in `storage/videos/`
→ React video player

## Future AI flow

Story
→ Story Analyzer
→ Character / Setting / Event extraction
→ Scene Generator
→ Storyboard Generator
→ Character Generation
→ Background Generation
→ Animation Generation
→ Audio Generation
→ Video Renderer
→ Final Animated Story

The current implementation intentionally keeps the AI-specific generators as extension points.
