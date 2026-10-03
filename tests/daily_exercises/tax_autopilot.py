# Scenario: Black Ore-style — validating AI-extracted tax document fields
from dataclasses import dataclass
import pytest


# PART 1 — custom exception
class LowConfidenceExtractionError(Exception):
    pass

@dataclass
class ExtractedField:
    field_name: str
    extracted_value: str
    confidence: float

    # PART 2 — validation function
    @staticmethod
    def validate_extraction(field: ExtractedField, min_confidence: float = 0.85) -> bool:
        # Raises LowConfidenceExtractionError if confidence < min_confidence
        # Returns True otherwise
        if field.confidence < min_confidence:
            raise LowConfidenceExtractionError(f"Confidence {field.confidence} below threshold {min_confidence}")
        return True

    # PART 3 — class method alternative constructor
    # ExtractedField.from_ocr_line("ssn|123-45-6789|0.97")
    # parses a pipe-delimited OCR line into an ExtractedField
    @classmethod
    def from_ocr_line(cls, line:str)->ExtractedField:
        field_name, extracted_value, confidence = line.split('|')
        return cls(field_name, extracted_value, float(confidence))

    # PART 4 — process a whole tax document
    # def validate_document(fields: list, min_confidence: float = 0.85) -> dict:
    # Returns {"valid": [...field_names...], "flagged": [...field_names...]}
    # instead of raising on the first low-confidence field,
    # collect ALL flagged fields so a human can review them together
    @staticmethod
    def validate_document(fields: list, min_confidence: float = 0.85) -> dict:
        valid = []
        flagged = []
        for field in fields:
            try:
                ExtractedField.validate_extraction(field, min_confidence)
                valid.append(field.field_name)
            except LowConfidenceExtractionError:
                flagged.append(field.field_name)
        return {"valid": valid, "flagged": flagged}

# PART 5 — Pytest
# test for high confidence passing
def test_high_confidence_passing():
    field = ExtractedField.from_ocr_line("ssn|123-45-6789|0.97")
    assert ExtractedField.validate_extraction(field) is True

# test for low confidence raising
def test_low_confidence_flagging():
    field = ExtractedField.from_ocr_line("name|Don|0.75")
    with pytest.raises(LowConfidenceExtractionError):
        ExtractedField.validate_extraction(field)

# test for from_ocr_line parsing correctly
def test_from_ocr_line_parsing_correctly():
    field = ExtractedField.from_ocr_line("ssn|123-45-6789|0.97")
    assert field.field_name == "ssn"
    assert field.extracted_value == "123-45-6789"
    assert field.confidence == 0.97

# test for validate_document separating valid/flagged correctly across multiple fields
def test_validate_document():
    test_fields = [ExtractedField.from_ocr_line("ssn|123-45-6789|0.75"),
              ExtractedField.from_ocr_line("name|Don|0.97"),
              ExtractedField.from_ocr_line("address|Varburg|0.95")]
    result = ExtractedField.validate_document(test_fields, min_confidence=0.85)
    assert result == {"valid": ["name", "address"],  "flagged": ["ssn"]}