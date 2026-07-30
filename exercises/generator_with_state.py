scores = [9.8, 7.5, 5.3, 9.1, 2.1]

# Write a generator running_total(scores)
# that yields the cumulative sum after each score
# Expected output: 9.8, 17.3, 22.6, 31.7, 33.8

def running_total(scores):
    total = 0
    for score in scores:
        total += score
        yield round(total, 1)

print(list(running_total(scores)))