from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://example.com")
driver.quit()  # always close at the end

# By ID (fastest, most reliable)
element = driver.find_element(By.ID, "email-input")

# By CSS selector (most flexible)
element = driver.find_element(By.CSS_SELECTOR, "#email-input")
element = driver.find_element(By.CSS_SELECTOR, ".submit-btn")
element = driver.find_element(By.CSS_SELECTOR, "input[type='email']")

# By XPath (use when nothing else works)
element = driver.find_element(By.XPATH, "//button[text()='Submit']")

# By text content (readable, good for buttons/links)
element = driver.find_element(By.LINK_TEXT, "Sign In")

# Find MULTIPLE elements — returns a list
items = driver.find_elements(By.CSS_SELECTOR, ".transaction-row")

# Type into a field
driver.find_element(By.ID, "email").send_keys("test@example.com")

# Clear a field first, then type
driver.find_element(By.ID, "email").clear()
driver.find_element(By.ID, "email").send_keys("new@example.com")

# Click a button
driver.find_element(By.ID, "submit-btn").click()

# Press keyboard key
driver.find_element(By.ID, "search").send_keys("income", Keys.RETURN)

# Get text content of an element
text = driver.find_element(By.ID, "result-message").text

# Get attribute value
value = driver.find_element(By.ID, "email").get_attribute("value")
placeholder = driver.find_element(By.ID, "email").get_attribute("placeholder")

# Check if element is displayed / enabled
is_visible = driver.find_element(By.ID, "submit-btn").is_displayed()
is_enabled = driver.find_element(By.ID, "submit-btn").is_enabled()

# NEVER use time.sleep() in production tests — use explicit waits
wait = WebDriverWait(driver, timeout=10)

# Wait until element is visible
element = wait.until(
    EC.visibility_of_element_located((By.ID, "result-message"))
)

# Wait until element is clickable
button = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".submit-btn"))
)

# Wait until text appears on page
wait.until(
    EC.text_to_be_present_in_element((By.ID, "status"), "Success")
)

# Wait until element disappears (e.g. loading spinner)
wait.until(
    EC.invisibility_of_element_located((By.ID, "loading-spinner"))
)

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")   # run without opening a browser window
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)            # fallback wait for all find_element calls
    yield driver
    driver.quit()                        # teardown — always runs even if test fails

def test_login(driver):
    driver.get("https://app.example.com/login")
    driver.find_element(By.ID, "email").send_keys("test@example.com")
    driver.find_element(By.ID, "password").send_keys("secret123")
    driver.find_element(By.ID, "submit").click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("/dashboard"))
    assert "/dashboard" in driver.current_url

def test_tax_filing_flow(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://app.getapril.com/file")

    # Fill in income
    driver.find_element(By.ID, "annual-income").send_keys("85000")

    # Select filing status from dropdown
    from selenium.webdriver.support.ui import Select
    Select(driver.find_element(By.ID, "filing-status")).select_by_visible_text("Single")

    # Submit
    driver.find_element(By.ID, "calculate-btn").click()

    # Assert result appears
    result = wait.until(EC.visibility_of_element_located((By.ID, "tax-result")))
    assert result.text != ""
    assert "$" in result.text