import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to take a screenshot
def take_screenshot(driver, step_name):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_name = f"screenshots/{step_name}_{timestamp}.png"
    driver.save_screenshot(screenshot_name)
    print(f"📸 Screenshot saved: {screenshot_name}")

# Create screenshots folder
os.makedirs("screenshots", exist_ok=True)

# Set ChromeDriver path
chrome_driver_path = "C:\\Users\\abifi\\Downloads\\chromedriver-win64\\chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

try:
    # Open the e-library system
    driver.get("http://localhost:8000/index.html")
    print("✅ Browser opened and page loaded.")
    take_screenshot(driver, "page_loaded")

    # Wait until page loads
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

    # Locate Search Box
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search")))
    search_box.send_keys("JavaScript Basics")
    take_screenshot(driver, "search_filled")

    # Locate and Click Search Button
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Search')]"))
    )
    search_button.click()
    take_screenshot(driver, "search_clicked")

    # Wait for search results
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "book-list")))
    take_screenshot(driver, "search_results")

    # Extract and print book list
    book_list_element = driver.find_element(By.ID, "book-list")
    print("📄 Book List Content:\n", book_list_element.text)

    # Verify if book exists
    if "JavaScript Basics" in book_list_element.text:
        print("✅ Book found in search results.")
    else:
        print("❌ Book NOT found in search results!")

except Exception as e:
    print(f"🚨 An error occurred: {str(e)}")

finally:
    # Close the browser
    driver.quit()
    print("🚪 Browser closed.")
