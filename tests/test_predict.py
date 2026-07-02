from sentiment_intelligence.predict import predict

def test_predict_shape():
    out = predict("I love this")
    assert "sentiment" in out and "confidence" in out
