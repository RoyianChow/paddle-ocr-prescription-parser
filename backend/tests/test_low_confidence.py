import json

from extraction.parser import parse_ocr_lines


def main():
    sample_ocr_lines = [
        "AGENTRX SAMPLE PRESCRIPTION",
        "Patient: John Doe",
        "DOB:1990-01-15",
        "Prescriber: Dr. Sarah Smith",
        "Clinic: Example Medical Clinic",
        "Phone: 416-555-1234",
        "Medication: Amoxicillin 500 mg",
        "Directions: Take 1 capsule by mouth twice daily",
        "Quantity:20",
        "Refills:0",
    ]

    result = parse_ocr_lines(
        ocr_lines=sample_ocr_lines,
        average_confidence=0.62,
    )

    print(json.dumps(result, indent=2))

    low_confidence_fields = result["pharmacyReview"]["lowConfidenceFields"]
    warnings = result["pharmacyReview"]["warnings"]

    assert result["pharmacyReview"]["needsHumanReview"] is True
    assert "ocr.averageConfidence" in low_confidence_fields
    assert any("OCR confidence is low" in warning for warning in warnings)

    print("\nPASS: Low-confidence safety test passed.")


if __name__ == "__main__":
    main()
