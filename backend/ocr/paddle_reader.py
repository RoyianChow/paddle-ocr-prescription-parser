from pathlib import Path
from paddleocr import PaddleOCR


_ocr_model = None


def get_ocr_model():
    global _ocr_model

    if _ocr_model is None:
        _ocr_model = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            engine="paddle",
        )

    return _ocr_model


def read_prescription_image(image_path):
    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    ocr = get_ocr_model()
    result = ocr.predict(str(image_path))

    lines = []
    scores = []

    for page_result in result:
        data = page_result.json if hasattr(page_result, "json") else {}

        if callable(data):
            data = page_result.json()

        res = data.get("res", data)

        texts = res.get("rec_texts", [])
        confidences = res.get("rec_scores", [])

        for text, confidence in zip(texts, confidences):
            lines.append(str(text).strip())
            scores.append(float(confidence))

    average_confidence = (
        sum(scores) / len(scores)
        if scores
        else None
    )

    return {
        "lines": lines,
        "scores": scores,
        "average_confidence": average_confidence
    }
