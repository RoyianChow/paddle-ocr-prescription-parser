
import re

from schemas.prescription_schema import create_empty_prescription_result
from extraction.validators import validate_prescription_result


def clean_line(line):
    return str(line).strip()


def get_label_value(lines, label):
    """
    Finds values like:
    Patient: John Doe
    DOB:1990-01-15
    Quantity:20
    """

    pattern = re.compile(rf"^{re.escape(label)}\s*:\s*(.+)$", re.IGNORECASE)

    for line in lines:
        match = pattern.match(line)

        if match:
            return match.group(1).strip()

    return None


def parse_medication_value(value):
    """
    Basic medication parser.

    Example:
    Amoxicillin 500 mg

    Returns:
    name = Amoxicillin
    strength = 500 mg
    """

    if not value:
        return None, None

    strength_pattern = re.compile(
        r"\b\d+(?:\.\d+)?\s*(mg|mcg|g|ml|mL|units?|iu|IU|%)\b",
        re.IGNORECASE
    )

    match = strength_pattern.search(value)

    if not match:
        return value.strip(), None

    name = value[:match.start()].strip(" -,:")
    strength = value[match.start():match.end()].strip()

    return name or None, strength or None


def parse_ocr_lines(ocr_lines, average_confidence=None):
    cleaned_lines = [clean_line(line) for line in ocr_lines if clean_line(line)]
    raw_text = "\n".join(cleaned_lines)

    result = create_empty_prescription_result(
        raw_text=raw_text,
        average_confidence=average_confidence
    )

    result["patient"]["name"] = get_label_value(cleaned_lines, "Patient")
    result["patient"]["dateOfBirth"] = get_label_value(cleaned_lines, "DOB")

    result["prescriber"]["name"] = get_label_value(cleaned_lines, "Prescriber")
    result["prescriber"]["clinic"] = get_label_value(cleaned_lines, "Clinic")
    result["prescriber"]["phone"] = get_label_value(cleaned_lines, "Phone")

    medication_value = get_label_value(cleaned_lines, "Medication")
    medication_name, medication_strength = parse_medication_value(medication_value)

    result["medication"]["name"] = medication_name
    result["medication"]["strength"] = medication_strength
    result["medication"]["directions"] = get_label_value(cleaned_lines, "Directions")
    result["medication"]["quantity"] = get_label_value(cleaned_lines, "Quantity")
    result["medication"]["refills"] = get_label_value(cleaned_lines, "Refills")

    result["pharmacyReview"] = validate_prescription_result(result)

    return result
