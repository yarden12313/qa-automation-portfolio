a = [1, 2, 3]
b = [4, 5, 6]

# Option 1 — + operator (most readable)
combined = a + b                   # [1, 2, 3, 4, 5, 6]

# Option 2 — extend (modifies a in place)
a.extend(b)                        # a is now [1, 2, 3, 4, 5, 6]

# Option 3 — unpacking (works for 3+ lists too)
combined = [*a, *b]                # [1, 2, 3, 4, 5, 6]
combined = [*a, *b, *[7, 8, 9]]   # works for any number of lists

# Most common in interview: just use +
users = active_users + inactive_users

pairs = [(1, "alice"), (2, "bob"), (3, "carol")]

# Option 1 — unpack directly in the for loop (cleanest)
for user_id, name in pairs:
    print(f"{user_id}: {name}")

# Option 2 — index access (less readable, avoid if possible)
for pair in pairs:
    print(f"{pair[0]}: {pair[1]}")

# Option 3 — enumerate (when you also need the position)
for i, (user_id, name) in enumerate(pairs):
    print(f"Row {i}: {user_id} - {name}")

# Real-world example — tax records as tuples
records = [("alice", 85000, 17000), ("bob", 120000, 28000)]
for name, income, tax_paid in records:
    rate = round(tax_paid / income, 2)
    print(f"{name}: effective rate {rate}")

keys   = ["alice", "bob", "carol"]
values = [85000,   120000, 60000]

# zip() pairs them up, dict() turns pairs into a dict
result = dict(zip(keys, values))
# {"alice": 85000, "bob": 120000, "carol": 60000}

# More realistic — two lists of records merged by position
user_ids = ["u1",    "u2",    "u3"]
incomes  = [85000,   120000,  60000]

combined = [{"user_id": uid, "income": inc}
            for uid, inc in zip(user_ids, incomes)]
# [{"user_id": "u1", "income": 85000}, ...]

# zip stops at the SHORTER list — be careful
a = [1, 2, 3, 4]
b = ["a", "b"]
print(list(zip(a, b)))  # [(1, "a"), (2, "b")] — 3 and 4 are dropped

# If you want to keep all elements, use zip_longest
from itertools import zip_longest
print(list(zip_longest(a, b, fillvalue=None)))
# [(1, "a"), (2, "b"), (3, None), (4, None)]