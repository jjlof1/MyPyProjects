# --- Libraries ---
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- File Handler Layer ---
def read_data_from_excel(excel_file):
    """Reads data from the specified Excel file."""
    return pd.read_excel(excel_file)

def save_log(log_file, message):
    """Appends a message to the log file."""
    with open(log_file, 'a') as f:
        f.write(f"{message}\n")

# --- Browser Setup Layer ---
def setup_browser():
    """Sets up and returns the browser."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# --- Data Processing Layer ---
def map_sexo(sexo):
    """Maps the gender to the corresponding XPATH."""
    return {
        'Mujer': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div/span/div/div[2]/label/div/div[2]/div/span',
        'Hombre': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div/span/div/div[1]/label/div/div[2]/div/span',
        'Prefiero no decirlo': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div/span/div/div[3]/label/div/div[2]/div/span'
    }.get(sexo, '')

def map_rubro(rubro):
    """Maps the profession to the corresponding XPATH."""
    return {
        'Doctor': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[2]/div[3]',
        'Profesor': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[2]/div[4]',
        'Abogado': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[2]/div[5]',
        'Médico': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[2]/div[6]'
    }.get(rubro, '')

# --- Form Automation Layer ---
def wait_and_fill(driver, xpath, value):
    """Waits for the element to be present and fills it with the given value."""
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath))).send_keys(value)

def wait_and_click(driver, xpath):
    """Waits for the element to be clickable and clicks it."""
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

def fill_form(driver, form_url, row):
    """Fills the Google form with the provided data."""
    driver.get(form_url)

    wait_and_fill(driver, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input', row['ID'])
    wait_and_fill(driver, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input', row['Nombre completo'])
    wait_and_click(driver, map_sexo(row['Sexo']))
    wait_and_fill(driver, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input', row['Dirección'])
    wait_and_fill(driver, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input', row['Teléfono'])
    wait_and_fill(driver, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div/div[1]/input', row['Correo electrónico'])
    wait_and_click(driver, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div[1]/div[1]/span')
    wait_and_click(driver, map_rubro(row['Rubro']))
    wait_and_click(driver, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

# --- Main Application / Orchestration Layer ---
def main():
    excel_file = 'Your Path/List clients.xlsx'
    form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSe9tvQvXKXo2DnBUwuLgdSoqObFskR4WNFNXQFyVNZ1sVdDmw/viewform?usp=sf_link'
    log_file = 'form_fill_log.txt'

    # Reading data
    data = read_data_from_excel(excel_file)

    # Setting up browser
    driver = setup_browser()

    # Processing and filling forms
    for _, row in data.iterrows():
        try:
            fill_form(driver, form_url, row)
            save_log(log_file, f"Form filled successfully for ID: {row['ID']}")
        except Exception as e:
            save_log(log_file, f"Error filling form for ID: {row['ID']}: {e}")

    # Closing browser
    driver.quit()

# --- Entry Point ---
if __name__ == "__main__":
    main()