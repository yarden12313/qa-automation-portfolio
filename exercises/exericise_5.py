# Given the same records list from Exercise 2,
# write a function that returns users who overpaid their taxes
# (effective rate > 0.25) sorted by income descending

def overpaid_users(records):
    result = [
        record for record in records
        if record.get("effective_rate",
           round(record["tax_paid"] / record["income"], 2)) > 0.25
    ]
    return sorted(result, key=lambda x: x["income"], reverse=True)

if __name__ == "__main__":
    records = [
        {"user": "alice", "income": 8500,  "tax_paid": 17000},
        {"user": "bob",   "income": 12000, "tax_paid": 28000},
        {"user": "carol", "income": 6000,  "tax_paid": 11000},
    ]
    # Add effective rates first using your function from Exercise 2
    records = [{**r, "effective_rate": round(r["tax_paid"] / r["income"], 2)} for r in records]

    results = overpaid_users(records)
    for r in results:
        print(f"User: {r['user']} | Income: {r['income']} | Rate: {r['effective_rate']}")