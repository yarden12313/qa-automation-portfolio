# Write a decorator called log_call that:
# - Prints the function name before it runs
# - Prints the result after it runs
# - Returns the result normally

def log_call(func):
    def inner(*args, **kwargs):
        print("Calling: " + func.__name__)
        result = func(*args, **kwargs)
        print("Result: " + str(result))
        return result
    return inner

# Apply it to this function:
@log_call
def calculate_tax(income, rate):
    return round(income * rate, 2)

# Expected output when calculate_tax(85000, 0.20) is called:
# Calling: calculate_tax
# Result: 17000.0

calculate_tax(85000, 0.20)