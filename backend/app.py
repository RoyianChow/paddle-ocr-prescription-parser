import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from ocr.paddle_reader import read_prescription_image
from extraction.parser import parse_ocr_lines


app = FastAPI(
    title="AgentRx Prescription OCR API",
    description="OCR extraction API for pharmacist/admin review only. Never auto-approves prescriptions.",
    version="0.1.0",
)

UPLOAD_DIR = Path("temp_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_CONTENT_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "AgentRx Prescription OCR API",
        "humanReviewRequired": True,
        "prescriptionStatus": "NOT_APPROVED",
    }


@app.post("/ocr/prescription")
async def ocr_prescription(file: UploadFile = File(...)):
    """
    Upload a prescription image and return structured OCR JSON.

    Safety:
    - Does not approve prescriptions.
    - Does not dispense medication.
    - Always requires pharmacist/admin human review.
    """

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG, and WEBP image uploads are supported."
        )

    suffix = ALLOWED_CONTENT_TYPES[file.content_type]
    safe_filename = f"{uuid.uuid4()}{suffix}"
    saved_path = UPLOAD_DIR / safe_filename

    try:
        with saved_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        ocr_result = read_prescription_image(saved_path)

        structured_result = parse_ocr_lines(
            ocr_lines=ocr_result["lines"],
            average_confidence=ocr_result["average_confidence"],
        )

        structured_result["pharmacyReview"]["needsHumanReview"] = True
        structured_result["pharmacyReview"]["warnings"].append(
            "API result is for extraction/review only. It is not approval to dispense."
        )

        return JSONResponse(content=structured_result)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"OCR processing failed: {str(error)}"
        )

    finally:
        file.file.close()
        if saved_path.exists():
            saved_path.unlink()
