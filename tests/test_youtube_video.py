from actions.youtube_video import _is_valid_youtube_url


def test_is_valid_youtube_url_valid_urls():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert _is_valid_youtube_url(url) is True
    assert _is_valid_youtube_url("https://youtu.be/dQw4w9WgXcQ") is True
    assert _is_valid_youtube_url("youtube.com") is True
    assert _is_valid_youtube_url("youtu.be") is True


def test_is_valid_youtube_url_invalid_urls():
    assert _is_valid_youtube_url("https://vimeo.com/123456") is False
    assert _is_valid_youtube_url("https://www.google.com") is False
    assert _is_valid_youtube_url("just a string") is False


def test_is_valid_youtube_url_edge_cases():
    assert _is_valid_youtube_url("") is False
    assert _is_valid_youtube_url(None) is False
