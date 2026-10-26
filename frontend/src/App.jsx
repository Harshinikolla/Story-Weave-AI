import { useState } from "react";

const API = "http://127.0.0.1:8000";

export default function App() {
  const [story, setStory] = useState(
    "A young girl named Maya walks through a quiet forest. She discovers a glowing tree and smiles with wonder."
  );
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function generateAnimation() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API}/api/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ story })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Generation failed");
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">AI STORY → ANIMATION</p>
        <h1>StoryWeave AI</h1>
        <p className="subtitle">
          Turn a written story into scenes, a storyboard, and a simple animated video.
        </p>
      </section>

      <section className="card">
        <label htmlFor="story">Your story</label>
        <textarea
          id="story"
          value={story}
          onChange={(e) => setStory(e.target.value)}
          placeholder="Write a short story..."
        />

        <button onClick={generateAnimation} disabled={loading || !story.trim()}>
          {loading ? "Creating animation..." : "Create Animation"}
        </button>

        {error && <p className="error">{error}</p>}
      </section>

      {result && (
        <section className="card result">
          <h2>Generated Animation</h2>
          <video
  key={result.video_url}
  controls
  src={`${API}${result.video_url}`}
  onError={() => setError("Video could not be loaded. Please generate again.")}
/>
          <a href={`${API}${result.video_url}`} target="_blank" rel="noreferrer">
            Open video
          </a>

          <h3>Scenes</h3>
          <div className="scenes">
            {result.scenes.map((scene) => (
              <article key={scene.scene_number}>
                <strong>Scene {scene.scene_number}</strong>
                <p>{scene.text}</p>
                <small>{scene.visual_description}</small>
              </article>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}
