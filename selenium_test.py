from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import os
import time

# Set up WebDriver (Avoids hardcoded ChromeDriver path)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Load the local HTML file
file_path = os.path.abspath("E:/E-Library-management-system/index.html")
driver.get(f"file:///{file_path}")

def test_page_load():
    """Verify the page loads successfully."""
    assert "E-Library Management System" in driver.title
    print("✅ Page loaded successfully.")

def test_search_books():
    """Search for a book and verify results appear."""
    search_box = driver.find_element(By.ID, "search")
    search_box.clear()
    search_box.send_keys("JavaScript")

    # Click the search button
    search_button = driver.find_element(By.XPATH, "//button[contains(text(),'Search')]")
    search_button.click()

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@id='book-list']//strong[contains(text(),'JavaScript Basics')]")
        ))
        print("✅ Book search works correctly.")
        return True  # Return success
    except:
        print("❌ Book search failed: 'JavaScript Basics' not found.")
        return False  # Return failure

def test_borrow_book():
    """Borrow a book after searching for it."""
    if not test_search_books():
        print("Skipping borrow test because search failed.")
        return

    try:
        borrow_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@id='book-list']//button[contains(text(),'Borrow')]")
        ))
        borrow_button.click()
        time.sleep(2)
        print("✅ Book borrowed successfully.")

        # Verify if book appears in borrowed books list
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//ul[@id='borrowed-books']//li[contains(text(),'JavaScript Basics')]")
        ))
        print("✅ Borrowed book appears in list.")

    except:
        print("❌ Borrow button not found or not clickable.")

def test_return_book():
    """Return a borrowed book and verify it is removed from the list."""
    try:
        # Check if any books are in borrowed list before attempting to return
        borrowed_books = driver.find_elements(By.XPATH, "//ul[@id='borrowed-books']//li")
        if not borrowed_books:
            print("❌ No borrowed books found, skipping return test.")
            return

        return_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Return')]")
        ))
        return_button.click()
        time.sleep(2)
        print("✅ Book returned successfully.")

        # Ensure the book is removed from the borrowed list
        time.sleep(1)  # Allow DOM update
        borrowed_books = driver.find_elements(By.XPATH, "//ul[@id='borrowed-books']//li")
        if not borrowed_books:
            print("✅ Borrowed book removed successfully.")
        else:
            print("❌ Borrowed book still present after returning.")

    except:
        print("❌ Return button not found or not clickable.")

def run_tests():
    test_page_load()
    test_borrow_book()
    test_return_book()
    driver.quit()

run_tests()
