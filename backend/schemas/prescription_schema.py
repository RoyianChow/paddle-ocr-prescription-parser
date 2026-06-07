def create_empty_prescription_result(raw_text="", average_confidence=None):
    """
    Base AgentRx prescription OCR output.

    Important:
    - This is extraction only.
    - It never approves a prescription.
    - Human review is always required.
    """

    return {
        "patient": {
            "name": None,
            "dateOfBirth": None,
            "phone": None,
            "address": None
        },
        "prescriber": {
            "name": None,
            "clinic": None,
            "phone": None,
            "fax": None,
            "licenseNumber": None,
            "address": None
        },
        "medication": {
            "name": None,
            "strength": None,
            "form": None,
            "quantity": None,
            "directions": None,
            "refills": None,
            "daysSupply": None
        },
        "pharmacyReview": {
            "needsHumanReview": True,
            "missingFields": [],
            "lowConfidenceFields": [],
            "warnings": [
                "OCR extraction only. Human review required before any pharmacy action."
            ]
        },
        "ocr": {
            "rawText": raw_text,
            "averageConfidence": average_confidence,
            "engine": "PaddleOCR"
        }
    }
