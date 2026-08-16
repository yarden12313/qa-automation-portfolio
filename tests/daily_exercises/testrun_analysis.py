from collections import Counter
import json

def slow_tests(results:list, threshold:int):
    for result in results:
        if result["duration_ms"] > threshold:
            yield result

if __name__ == "__main__":
    test_status = Counter()
    test_results = [
        {"test": "test_login", "status": "PASS", "duration_ms": 120},
        {"test": "test_signup", "status": "FAIL", "duration_ms": 340},
        {"test": "test_logout", "status": "PASS", "duration_ms": 90},
        {"test": "test_payment", "status": "FAIL", "duration_ms": 500},
        {"test": "test_search", "status": "PASS", "duration_ms": 200},
        {"test": "test_upload", "status": "SKIP", "duration_ms": 0},
    ]
    for i, test in enumerate(test_results):
        test_status[test["status"]] += 1
        print(f"Test #{i + 1}: {test['test']} - {test['status']}")
    print(json.dumps(dict(test_status)))
    result_index = next(i for i, value in enumerate(test_results) if value["status"] == "FAIL")
    print(json.dumps(test_results[result_index]))
    print(json.dumps(list(test["test"] for test in test_results if test["duration_ms"] > 150)))
    print(json.dumps(list(slow_tests(test_results, 100))))
