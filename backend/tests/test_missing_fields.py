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
        "Medication: Amoxicillin",
        "Quantity:20"
    ]

    result = parse_ocr_lines(
        ocr_lines=sample_ocr_lines,
        average_confidence=0.91
    )

    print(json.dumps(result, indent=2))

    print("\n--- SAFETY CHECK ---")
    print("Human review required:", result["pharmacyReview"]["needsHumanReview"])
    print("Missing fields:", result["pharmacyReview"]["missingFields"])
    print("Warnings:", result["pharmacyReview"]["warnings"])


if __name__ == "__main__":
    main()
