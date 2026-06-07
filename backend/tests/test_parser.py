
import json

from extraction.parser import parse_ocr_lines


def main():
    sample_ocr_lines = [
        "AGENTRXSAMPLEPRESCRIPTION",
        "Patient: John Doe",
        "DOB:1990-01-15",
        "Prescriber: Dr. Sarah Smith",
        "Clinic: Example Medical Clinic",
        "Phone: 416-555-1234",
        "Medication: Amoxicillin 500 mg",
        "Directions: Take 1 capsule by mouth twice daily",
        "Quantity:20",
        "Refills:0",
        "FOR OCR TESTING ONLY - NOT A REAL PRESCRIPTION",
        "Human review required before dispensing"
    ]

    result = parse_ocr_lines(
        ocr_lines=sample_ocr_lines,
        average_confidence=0.9636
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
