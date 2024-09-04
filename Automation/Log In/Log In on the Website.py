# --- Libraries ---
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Data Retrieval Layer ---
def read_password_from_file(file_path):
    """Reads the password from a file and handles possible errors."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, 'r') as file:
        password = file.readline().strip()
    if not password:
        raise ValueError("The password file is empty.")
    return password

# --- Browser Setup Layer ---
def setup_browser():
    """Sets up and returns the browser."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    browser = webdriver.Chrome(options=options)
    browser.get('https://x.com/i/flow/login')
    return browser

# --- Business Logic Layer ---
def login(browser, user, password):
    """Performs the login on the website."""
    wait = WebDriverWait(browser, 10)

    try:
        # Wait and enter the username
        input_username = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='text']")))
        input_username.send_keys(user)

        # Wait and click the "Next" button
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next')]")))
        next_button.click()

        # Wait and enter the password
        input_password = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
        input_password.send_keys(password)

        # Wait and click the "Log in" button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Log in')]")))
        login_button.click()
        
        # Optional: Wait for a specific time to let the login process complete
        time.sleep(10)
        
    except Exception as exc:
        print(f"An error occurred during login: {exc}")
        raise

# --- Main Application / Orchestration Layer ---
def main():
    user = 'Your X User'
    password_file_path = 'Your Path/Log In/Passwordt.txt'

    try:
        password = read_password_from_file(password_file_path)
        browser = setup_browser()
        login(browser, user, password)
    except Exception as exc:
        print(f"An error occurred: {exc}")
    finally:
        try:
            # Close the browser automatically after 5 seconds
            time.sleep(5)
            browser.quit()
        except Exception as exc:
            print(f"An error occurred while closing the browser: {exc}")

# --- Entry Point ---
if __name__ == "__main__":
    main()