import pytest

EXTRACTIONS = [
    {"doc_id": "DOC-101", "obligation_type": "payment", "confidence": 0.92, "false_positive_risk": "low"},
    {"doc_id": "DOC-102", "obligation_type": "termination", "confidence": 0.61, "false_positive_risk": "high"},
    {"doc_id": "DOC-103", "obligation_type": "payment", "confidence": 0.45, "false_positive_risk": "high"},
    {"doc_id": "DOC-104", "obligation_type": "renewal", "confidence": 0.88, "false_positive_risk": "low"},
    {"doc_id": "DOC-105", "obligation_type": "termination", "confidence": 0.95, "false_positive_risk": "low"},
]

def release_gate(extractions: list, min_confidence=0.7) -> dict:
    # list of doc_ids where confidence >= min_confidence AND false_positive_risk is "low"
    safe_to_release = [ext["doc_id"] for ext in extractions if ext["confidence"] >= min_confidence and ext["false_positive_risk"] == "low"]

    # list of doc_ids that DON'T meet the safe criteria (this is your "bring to the founder/dev meeting" list)
    needs_review = [ext["doc_id"] for ext in extractions if not (ext["confidence"] >= min_confidence and ext["false_positive_risk"] == "low")]

    # dict mapping obligation_type to average confidence
    avg_confidence_by_type = {}
    for ext in extractions:
        if ext["obligation_type"] in avg_confidence_by_type:
            avg_confidence_by_type[ext["obligation_type"]].append(ext["confidence"])
        else:
            avg_confidence_by_type[ext["obligation_type"]] = [ext["confidence"]]
    return {"safe_to_release": safe_to_release,
            "needs_review": needs_review,
            "avg_confidence_by_type": {key:sum(value)/len(value) for key, value in avg_confidence_by_type.items()}}

def explain_decision(doc: dict, min_confidence: float = 0.7) -> str:
    low_confidence = doc["confidence"] < min_confidence
    high_risk = doc["false_positive_risk"] == "high"

    if not low_confidence and not high_risk:
        return f"{doc['doc_id']}: SAFE - high confidence, low FP risk"
    if low_confidence and high_risk:
        return f"{doc['doc_id']}: REVIEW NEEDED - low confidence, high FP risk"
    if low_confidence:
        return f"{doc['doc_id']}: REVIEW NEEDED - low confidence"
    return f"{doc['doc_id']}: REVIEW NEEDED - high FP risk"

def test_release_decision():
    decision = release_gate(EXTRACTIONS)
    assert decision["safe_to_release"] == ["DOC-101", "DOC-104", "DOC-105"]
    assert decision["needs_review"] == ["DOC-102","DOC-103"]
    assert decision["avg_confidence_by_type"] == {
        "payment": 0.685,
        "termination": 0.78,
        "renewal": 0.88
    }

@pytest.mark.parametrize("i,expected", [(0, ": SAFE - high confidence, low FP risk"),
                                        (1, ": REVIEW NEEDED - low confidence, high FP risk"),
                                        (2, ": REVIEW NEEDED - low confidence, high FP risk"),
                                        (3, ": SAFE - high confidence, low FP risk"),
                                        (4, ": SAFE - high confidence, low FP risk")])
def test_explain_decision(i, expected):
    assert explain_decision(EXTRACTIONS[i]) == EXTRACTIONS[i]["doc_id"]+expected