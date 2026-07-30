records = [("alice", 85000, 17000),
           ("bob",   120000, 28000),
           ("carol", 60000,  11000)]

# Without enumerate — no index
for name, income, tax_paid in records:
    print(f"{name}: {income}")

# With enumerate — adds index i
for i, (name, income, tax_paid) in enumerate(records):
    print(f"Row {i}: {name} - {income}")
# Row 0: alice - 85000
# Row 1: bob - 120000
# Row 2: carol - 11000

# Start index from 1 instead of 0
for i, (name, income, tax_paid) in enumerate(records, start=1):
    print(f"Row {i}: {name}")
# Row 1: alice
# Row 2: bob
# Row 3: carol