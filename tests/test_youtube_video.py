import pytest
from actions.youtube_video import _extract_video_id

def test_extract_video_id_standard_url():
    assert _extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"

def test_extract_video_id_short_url():
    assert _extract_video_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

def test_extract_video_id_embed_url():
    assert _extract_video_id("https://www.youtube.com/embed/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

def test_extract_video_id_v_url():
    assert _extract_video_id("https://www.youtube.com/v/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

def test_extract_video_id_shorts_url():
    assert _extract_video_id("https://www.youtube.com/shorts/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

def test_extract_video_id_with_parameters():
    assert _extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=43s") == "dQw4w9WgXcQ"
    assert _extract_video_id("https://youtu.be/dQw4w9WgXcQ?t=10") == "dQw4w9WgXcQ"

def test_extract_video_id_invalid_url():
    assert _extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXc") is None
    assert _extract_video_id("https://www.youtube.com/watch") is None
    assert _extract_video_id("invalid_url") is None
    assert _extract_video_id("") is None

def test_extract_video_id_with_underscores_and_dashes():
    assert _extract_video_id("https://www.youtube.com/watch?v=A-b_cDeFgHi") == "A-b_cDeFgHi"
