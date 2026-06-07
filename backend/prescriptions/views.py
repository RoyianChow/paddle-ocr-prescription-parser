import json
import uuid
from pathlib import Path

from django.shortcuts import render

from extraction.parser import parse_ocr_lines
from ocr.paddle_reader import read_prescription_image


UPLOAD_DIR = Path("temp_uploads") / "django"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_CONTENT_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


def upload_prescription(request):
    if request.method == "GET":
        return render(request, "prescriptions/upload.html")

    uploaded_file = request.FILES.get("file")

    if uploaded_file is None:
        return render(
            request,
            "prescriptions/upload.html",
            {"error": "Please upload a prescription image."},
            status=400,
        )

    if uploaded_file.content_type not in ALLOWED_CONTENT_TYPES:
        return render(
            request,
            "prescriptions/upload.html",
            {"error": "Only JPG, PNG, and WEBP images are supported."},
            status=400,
        )

    suffix = ALLOWED_CONTENT_TYPES[uploaded_file.content_type]
    saved_path = UPLOAD_DIR / f"{uuid.uuid4()}{suffix}"

    try:
        with saved_path.open("wb") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        ocr_result = read_prescription_image(saved_path)

        result = parse_ocr_lines(
            ocr_lines=ocr_result["lines"],
            average_confidence=ocr_result["average_confidence"],
        )

        result["pharmacyReview"]["needsHumanReview"] = True
        result["pharmacyReview"]["warnings"].append(
            "Django review portal result is for extraction/review only. It is not approval to dispense."
        )

        return render(
            request,
            "prescriptions/result.html",
            {
                "result": result,
                "result_json": json.dumps(result, indent=2),
            },
        )

    except Exception as error:
        return render(
            request,
            "prescriptions/upload.html",
            {"error": f"OCR processing failed: {str(error)}"},
            status=500,
        )

    finally:
        if saved_path.exists():
            saved_path.unlink()
