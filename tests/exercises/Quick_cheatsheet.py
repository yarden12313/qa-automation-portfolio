# Generator
# A generator uses yield to produce values lazily one at a time — memory efficient for large datasets,
# because it never builds the full list in memory.

def my_gen(items):
    for item in items:
        yield item         # pauses here, resumes on next()

# yield
# yield pauses the function and sends a value to the caller — unlike return,
# the function remembers its state and resumes from the same point next time it's called.

def countdown(n):
    while n > 0:
        yield n    # pause, send n
        n -= 1     # resume here next time

# Decorator
# A decorator wraps a function to add behavior — logging, validation, timing — without modifying the original.
# @decorator is shorthand for func = decorator(func).

def my_decorator(func):
    def wrapper(*args, **kwargs):
        # before
        result = func(*args, **kwargs)
        # after
        return result
    return wrapper

@my_decorator
def my_function():
    pass

# List comprehension vs generator expression
list_comp = [x**2 for x in range(10)]    # [] — builds full list in memory
gen_expr  = (x**2 for x in range(10))    # () — lazy, one at a time

# Lambda — anonymous one-line function
double = lambda x: x * 2
print(double(5))  # 10
# You've already used this: sorted(list, key=lambda x: x["field"])

# *args and **kwargs — flexible function arguments
# *args, **kwargs is the pattern that makes decorators universal.
# It means your decorator works on any function regardless of its signature
def my_func(*args, **kwargs):
    print(args)    # tuple of positional args
    print(kwargs)  # dict of keyword args

my_func(1, 2, 3, name="alice", age=30)
# (1, 2, 3)
# {'name': 'alice', 'age': 30}

# Context manager
# A context manager handles setup and teardown automatically using __enter__ and __exit__ —
# the with keyword guarantees cleanup runs even if an exception occurs.
# WITHOUT context manager — risky
f = open("file.txt")
data = f.read()
f.close()  # what if read() crashes? file never closes → memory leak

# WITH context manager — safe, always cleans up
with open("file.txt") as f:
    data = f.read()
# file closes automatically here, even if an exception occurred

# A context manager needs two methods:
class DatabaseConnection:
    def __enter__(self):
        print("Opening connection")
        self.conn = connect_to_db()
        return self.conn      # this is what "as" receives

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing connection")
        self.conn.close()     # always runs, even if exception occurred
        return False          # False = don't suppress exceptions

# Usage
with DatabaseConnection() as conn:
    conn.execute("SELECT * FROM users")
# connection closes automatically here

from contextlib import contextmanager

@contextmanager
def managed_db():
    print("Setup: opening connection")
    conn = connect_to_db()
    try:
        yield conn            # code inside "with" block runs here
    finally:
        print("Teardown: closing connection")
        conn.close()          # always runs

with managed_db() as conn:
    conn.execute("SELECT * FROM users")

# Property decorator
class TaxRecord:
    def __init__(self, income, tax_paid):
        self._income = income
        self._tax_paid = tax_paid

    @property
    def effective_rate(self):           # call as record.effective_rate, not record.effective_rate()
        return round(self._tax_paid / self._income, 2)

record = TaxRecord(85000, 17000)
print(record.effective_rate)  # 0.2

# One small style upgrade for the interview — use json.dumps for cleaner output:
import json
from collections import Counter

vulnerabilities_collection = get_vulnerabilities(vulnerabilities)
labels = [
    "CRITICAL vulns sorted by cvss:",
    "Unpatched vulns sorted by cvss:",
    "Host → max cvss:",
    "Count per severity:",
]
for label, result in zip(labels, vulnerabilities_collection):
    print(f"\n{label}")
    print(json.dumps(result, indent=2) if isinstance(result, (list, dict)) else result)

# Always raise ValueError(...) not raise Exception(ValueError, ...)
# Never mutate the input — use a local variable for calculations
# Don't put conditions inside parametrized tests — use specific test data instead
# calculate_exposure_score(vuln) == pytest.approx(expected, rel=1e-1)
# avoid naming your variable sum — it shadows Python's built-in sum() function. Use total instead
# *args, **kwargs is the pattern that makes decorators universal.
# It means your decorator works on any function regardless of its signature
# notice the f-string — got {arg} tells the caller exactly which value failed.
# Small thing, but interviewers notice descriptive error messages.
# "func is the original function passed to the decorator.
# inner is the wrapper function that adds behavior around it.
# return inner hands back the wrapper as a replacement for the original function — so from that point on,
# every call to calculate_refund actually calls inner."
# "*args, **kwargs makes the decorator universal —
# it forwards any arguments through to the original function without the decorator needing to know what
# those arguments are.
# If I wrote inner(tax_paid, tax_owed) explicitly, the decorator would only work on functions with exactly
# those two parameters."
# "They're identical — @validate_positive is just syntactic sugar
# for calculate_refund = validate_positive(calculate_refund). The @ syntax runs at definition time and replaces the function with the decorated version. Same result, cleaner to read."
# Syntactic sugar is the exact term to use for A3 —
# interviewers love hearing it because it shows you understand what @ actually does under the hood,
# not just how to use it.


# @pytest.fixture
# Wraps my_fixture so pytest knows to inject its return value
# into any test function that lists it as a parameter.
# Without it, pytest treats it as a regular function.

# @pytest.mark.parametrize("x,y", [(1,2),(3,4)])
# Wraps test_something so it runs TWICE —
# once with x=1,y=2 and once with x=3,y=4.
# Generates separate test cases from one function.

# @mock_aws
# Wraps test_s3 so that all boto3 calls inside it
# go to fake in-memory AWS instead of real AWS.
# Sets up the fake environment before the test,
# tears it down after — exactly like __enter__/__exit__.
#
# my_framework/
# ├── conftest.py          # shared fixtures, session setup
# ├── tests/               # test files grouped by feature
# ├── pages/               # Page Object Model for UI
# ├── api/                 # API client wrappers
# ├── utils/               # helpers, data generators
# └── config/              # environment configs (dev, staging, prod)

# CI/CD pipeline — be able to describe it clearly
# "PR opens → unit tests run (fast, under 2 min) → merge to main →
# integration tests → nightly E2E and performance tests.
# Tests are parallelized with pytest-xdist, results output as JUnit XML for the pipeline dashboard."

# "POM separates UI selectors from test logic. When the UI changes I fix one class, not every test. Tests read like plain English — no CSS selectors in sight."
class LoginPage:
    def __init__(self, page):
        self.page = page

    def login(self, email: str, password: str):
        self.page.get_by_label("Email").fill(email)
        self.page.get_by_label("Password").fill(password)
        self.page.get_by_role("button", name="Login").click()

# Test never touches selectors:
def test_login(page):
    login = LoginPage(page)
    login.login("test@example.com", "password")
    expect(page).to_have_url("/dashboard")