LOW_CONFIDENCE_THRESHOLD = 0.85

REQUIRED_FIELDS = [
    ("patient", "name"),
    ("patient", "dateOfBirth"),
    ("prescriber", "name"),
    ("prescriber", "phone"),
    ("medication", "name"),
    ("medication", "strength"),
    ("medication", "directions"),
    ("medication", "quantity"),
    ("medication", "refills"),
]


def get_nested_value(data, section, field):
    return data.get(section, {}).get(field)


def is_missing(value):
    return value is None or str(value).strip() == ""


def validate_prescription_result(data):
    missing_fields = []
    low_confidence_fields = []
    warnings = []

    for section, field in REQUIRED_FIELDS:
        value = get_nested_value(data, section, field)

        if is_missing(value):
            missing_fields.append(f"{section}.{field}")

    average_confidence = data.get("ocr", {}).get("averageConfidence")

    if average_confidence is None:
        low_confidence_fields.append("ocr.averageConfidence")
        warnings.append("OCR confidence is missing.")
    elif average_confidence < LOW_CONFIDENCE_THRESHOLD:
        low_confidence_fields.append("ocr.averageConfidence")
        warnings.append("OCR confidence is low. Review carefully.")

    if missing_fields:
        warnings.append("One or more required prescription fields are missing or unclear.")

    warnings.append("Do not approve, dispense, or finalize from OCR output alone.")
    warnings.append("Pharmacist/admin human review is required.")

    return {
        "needsHumanReview": True,
        "missingFields": missing_fields,
        "lowConfidenceFields": low_confidence_fields,
        "warnings": warnings
    }
