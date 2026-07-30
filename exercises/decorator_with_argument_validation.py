# Write a decorator validate_positive that:
# - Checks all arguments passed to the function
# - Raises ValueError if any argument is negative
# - Lets the function run normally if all args are positive

def validate_positive(func):
    def inner(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError(f"Argument must be positive, got {arg}")
        result = func(*args, **kwargs)
        return result
    return inner

# Apply it to:
@validate_positive
def calculate_refund(tax_paid, tax_owed):
    return tax_paid - tax_owed

calculate_refund(200, 50)
calculate_refund(-50, 200)