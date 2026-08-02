import pytest

documents = [
    {"doc_id": "DOC-001", "type": "contract",  "pages": 45, "status": "processed",  "extracted_obligations": 12},
    {"doc_id": "DOC-002", "type": "policy",    "pages": 8,  "status": "processed",  "extracted_obligations": 3},
    {"doc_id": "DOC-003", "type": "contract",  "pages": 120,"status": "failed",     "extracted_obligations": 0},
    {"doc_id": "DOC-004", "type": "compliance","pages": 30, "status": "processed",  "extracted_obligations": 7},
    {"doc_id": "DOC-005", "type": "contract",  "pages": 15, "status": "processing", "extracted_obligations": 0},
    {"doc_id": "DOC-006", "type": "policy",    "pages": 22, "status": "failed",     "extracted_obligations": 0},
]

def analyze_documents(documents:list) -> dict:
    success_rate = round(sum(1 for d in documents if d["status"] == "processed") / len(documents) * 100, 1) if documents else 0.0
    obligations_by_type = {}
    for d in documents:
        if d["type"] not in obligations_by_type:
            obligations_by_type[d["type"]] = d["extracted_obligations"]
        else:
            obligations_by_type[d["type"]] += d["extracted_obligations"]
    failed_docs = [d["doc_id"] for d in documents if d["status"] == "failed"]
    processed = [d for d in documents if d["status"] == "processed"]
    avg_pages_processed = round(sum(d["pages"] for d in processed) / len(processed), 1) if processed else 0.0
    return {
        "success_rate": f"{success_rate}%",
        "obligations_by_type": obligations_by_type,
        "failed_docs": failed_docs,
        "avg_pages_processed": avg_pages_processed,
    }

def large_pending_docs(documents:list, min_pages:int):
    for d in documents:
        if d["status"] != "processed" and d["pages"] >= min_pages:
            yield d

def test_success_rate():
    assert analyze_documents(documents)["success_rate"] == "50.0%"

def test_empty_list():
    assert analyze_documents([]) == {'avg_pages_processed': 0.0,
                                     'failed_docs': [],
                                     'obligations_by_type': {},
                                     'success_rate': "0.0%"}

@pytest.mark.parametrize("min_pages, doc_count",[(10,3), (50, 1), (200, 0)])
def test_large_pending_docs(min_pages:int, doc_count:int):
    assert sum(1 for _ in large_pending_docs(documents, min_pages)) == doc_count