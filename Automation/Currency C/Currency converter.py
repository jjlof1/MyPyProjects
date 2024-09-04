# --- Libraries ---
import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook

# --- Data Retrieval Layer ---
def fetch_usd_to_mxn(url):
    """Fetch the USD to MXN conversion rate from the provided URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        return response.content
    except requests.exceptions.RequestException as exc:
        print(f"Error accessing the webpage: {exc}")
        return None

# --- Data Parsing Layer ---
def parse_usd_value(html_content):
    """Parse the HTML content to extract the USD value."""
    soup = BeautifulSoup(html_content, 'html.parser')
    usd_element = soup.select_one('p.sc-e08d6cef-1.fwpLse')  # Replace with the correct CSS selector
    
    if usd_element:
        try:
            # Convert the value to a floating-point number
            return float(usd_element.text.split(' ')[0].strip('$').replace(',', '.'))
        except ValueError:
            print("Error converting the USD value to float.")
            return None
    else:
        print("The USD value couldn't be found on the page.")
        return None

# --- Data Persistence Layer ---
def update_excel_file(workbook_path, sheet_name, cell, value):
    """Update the specified cell in the Excel sheet with the new value."""
    try:
        workbook = load_workbook(workbook_path)
        worksheet = workbook[sheet_name]
        worksheet[cell] = value
        workbook.save(workbook_path)
        print("The value has been successfully updated in the file.")
    except Exception as exc:
        print(f"An error occurred while updating the Excel file: {exc}")

# --- Main Application / Orchestration Layer ---
def main():
    url = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=MXN'
    workbook_path = 'Your Path/USD to MXN Peso Converter Today.xlsx'
    sheet_name = 'CC'
    cell = 'C12'
    
    html_content = fetch_usd_to_mxn(url)
    
    if html_content:
        usd_value = parse_usd_value(html_content)
        if usd_value is not None:
            update_excel_file(workbook_path, sheet_name, cell, usd_value)

# --- Entry Point ---
if __name__ == "__main__":
    main()