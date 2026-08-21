if __name__ == "__main__":
    orders = [
        {"id": 1, "customer_id": 101, "total": 250},
        {"id": 2, "customer_id": 102, "total": 80},
        {"id": 3, "customer_id": 999, "total": 40},  # customer_id שלא קיים!
    ]

    customers = [
        {"id": 101, "name": "Alice"},
        {"id": 102, "name": "Bob"},
    ]
    customers_by_id = {c["id"]: c for c in customers}

    matched = [
        {**order, "customer_name": customers_by_id[order["customer_id"]]["name"]}
        for order in orders
        if order["customer_id"] in customers_by_id
    ]

    # [{"id": 1, "customer_id": 101, "total": 250, "customer_name": "Alice"},
    #  {"id": 2, "customer_id": 102, "total": 80, "customer_name": "Bob"}]
    # order 3 מודר כי customer_id=999 לא קיים