import json
from pathlib import Path

from ocr.paddle_reader import read_prescription_image
from extraction.parser import parse_ocr_lines


IMAGE_PATH = Path(__file__).resolve().parents[1] / "samples" / "sample_prescription.jpg"


def main():
    print(f"Running OCR on: {IMAGE_PATH}")

    ocr_result = read_prescription_image(IMAGE_PATH)

    print("\n--- RAW OCR LINES ---")
    for line, score in zip(ocr_result["lines"], ocr_result["scores"]):
        print(f"{line} | confidence: {score:.2f}")

    final_json = parse_ocr_lines(
        ocr_lines=ocr_result["lines"],
        average_confidence=ocr_result["average_confidence"]
    )

    print("\n--- STRUCTURED PRESCRIPTION JSON ---")
    print(json.dumps(final_json, indent=2))

    print("\n--- SAFETY STATUS ---")
    print("Human review required: True")
    print("Prescription status: NOT APPROVED")


if __name__ == "__main__":
    main()
