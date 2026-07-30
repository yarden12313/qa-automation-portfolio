# Given this raw tax data:
# records = [
#     {"user": "alice", "income": 85000, "tax_paid": 17000},
#     {"user": "bob",   "income": 120000, "tax_paid": 28000},
#     {"user": "carol", "income": 60000, "tax_paid": 11000},
# ]

# Write a function that returns a new list where each record
# also includes an "effective_rate" field (tax_paid / income, rounded to 2 decimals)

def add_effective_rate(records):
    return [
            {
                **record, "effective_rate": round(record["tax_paid"] / record["income"], 2)
                if record["income"] != 0 else 0.0
            }
        for record in records]

if __name__ == "__main__":
    records = [
        {"user": "alice", "income": 85000, "tax_paid": 17000},
        {"user": "bob", "income": 120000, "tax_paid": 28000},
        {"user": "carol", "income": 60000, "tax_paid": 11000},
    ]
    result = add_effective_rate(records)
    for record in result:
        print(f"User: {record["user"]}")
        print(f"Income: {record['income']}")
        print(f"Tax paid: {record['tax_paid']}")
        print(f"Effective rate: {record['effective_rate']}")
        print("-----------------------------------------------")