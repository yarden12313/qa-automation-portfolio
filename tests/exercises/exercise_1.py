# Given this list of transactions:
# transactions = [250, -30, 1500, -200, 80, -50, 3000]

# Write a function that returns:
# 1. Total balance
# 2. List of only the positive transactions (income)
# 3. List of only the negative transactions (expenses)
# 4. The largest single expense (most negative number)

def get_overview(transactions):
    positive_transactions = [t for t in transactions if t > 0]
    negative_transactions = [t for t in transactions if t < 0]
    balance = sum(transactions)
    largest_expense = min(negative_transactions) if negative_transactions else None
    return {"income": positive_transactions,
            "expenses": negative_transactions,
            "largest expense": largest_expense,
            "balance": balance}

if __name__ == "__main__":
    transactions = [250, -30, 1500, -200, 80, -50, 3000]
    result = get_overview(transactions)
    print(f"Balance: {result['balance']}")
    print(f"Income: {result['income']}")
    print(f"Expenses: {result['expenses']}")
    print(f"Largest Expense: {result['largest expense']}")