from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome WebDriver using webdriver-manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Open the E-Library System
    driver.get("http://localhost:8000/index.html")
    print("✅ Browser opened and page loaded.")

    # Wait until the page loads completely
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

    # Search for a book
    search_box = driver.find_element(By.ID, "search")
    search_box.send_keys("JavaScript Basics")

    search_button = driver.find_element(By.XPATH, "//button[contains(text(),'Search')]")
    search_button.click()
    print("🔎 Search button clicked.")

    # Wait for search results to appear
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "book-list")))

    # Capture book list content
    book_list_element = driver.find_element(By.ID, "book-list")
    print("📄 Book List Content:\n", book_list_element.text)

    # Verify if the book appears
    assert "JavaScript Basics" in book_list_element.text, "❌ Book not found in search results!"
    print("✅ Book found in search results.")

    # Take a screenshot for proof
    screenshot_path = "test_result.png"
    driver.save_screenshot(screenshot_path)
    print(f"📸 Screenshot saved: {screenshot_path}")

except Exception as e:
    print("❌ Test Failed:", str(e))

finally:
    # Close the browser
    driver.quit()
    print("🚪 Browser closed.")
