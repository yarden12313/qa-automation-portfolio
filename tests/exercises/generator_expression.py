# Convert this list comprehension to a generator expression
# List comprehension — builds full list in memory
# high_risk = ([v["id"] for v in vulnerabilities if v["cvss"] > 7.0])

# Convert to a generator expression
# Hint: change [] to ()

# Then: what's the difference in behavior?
# When would you use a generator instead of a list?