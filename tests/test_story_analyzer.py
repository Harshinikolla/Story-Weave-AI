from ai_pipeline.story_analyzer.analyzer import analyze_story


def test_story_analysis():
    result = analyze_story("Maya walks through a forest. Maya sees a castle.")
    assert result["sentence_count"] == 2
    assert result["word_count"] > 0
