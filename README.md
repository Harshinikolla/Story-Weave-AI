# StoryWeave AI

StoryWeave AI is a narrative-to-animation project.

It converts a written story into:
1. Story analysis
2. Scene breakdown
3. Storyboard descriptions
4. A simple procedural animated MP4

This is the first runnable MVP. The AI asset and animation modules are intentionally structured as extension points for later phases.

## Project structure

```text
StoryWeave/
├── frontend/
├── backend/
├── ai_pipeline/
├── video_renderer/
├── storage/
├── tests/
├── docs/
├── .env.example
├── docker-compose.yml
└── README.md
```

## Requirements

- Python 3.11+ recommended
- Node.js 18+
- VS Code
- FFmpeg is handled by `imageio-ffmpeg` for the Python renderer.

## Backend setup

Open PowerShell in the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt

```

Backend:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## Frontend setup

Open a second PowerShell:

```powershell
cd frontend
npm install
npm run dev
```

Open:
- http://127.0.0.1:5173

## Generate a video
python -m uvicorn backend.app.main:app --reload
1. Start the backend.
2. Start the frontend.
3. Enter a story.
4. Click **Create Animation**.
5. The generated MP4 will be stored in `storage/videos/`.

## Important

The current renderer is a procedural 2D MVP. It creates a real animated MP4, but it does not yet use an image-generation model, text-to-speech model, lip-sync model, or full character animation model.

Those features are planned as later modules under `ai_pipeline/`.
