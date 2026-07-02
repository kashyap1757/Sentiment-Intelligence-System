from sentiment_intelligence.preprocessing import clean_text

def test_clean_text_basic():
    assert clean_text("Hello!!! WORLD") == "hello world"
