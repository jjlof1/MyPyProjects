# --- Libraries ---
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.drawing.image import Image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import warnings
import os
import logging
from datetime import datetime

warnings.filterwarnings('ignore', category=FutureWarning)

# --- File Handler Layer ---
def read_data(file_path):
    return pd.read_csv(file_path)

def save_excel_report(wb, output_file):
    wb.save(output_file)
    print(f"Report generated: {output_file}")

def create_log(log_file, email_status, files_sent):
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')
    logging.info(f"Files sent: {files_sent}")
    logging.info(f"Email status: {email_status}")

# --- Data Processing Layer ---
def clean_data(data):
    data = data.drop_duplicates()
    numeric_columns = data.select_dtypes(include=['number']).columns
    data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].mean())
    return data

def calculate_total_sales(data):
    data['Total Amount'] = data['Quantity'] * data['Price per Unit']
    return data

def filter_sales(data, threshold):
    return data[data['Total Amount'] > threshold]

# --- Presentation Layer ---
def generate_pie_chart(filtered_data, chart_image):
    plt.figure(figsize=(8, 8))
    filtered_data.groupby('Product Category')['Total Amount'].sum().plot(kind='pie', autopct='%1.1f%%', colors=plt.cm.Paired.colors)
    plt.title('Total Sales Per Product Category')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(chart_image)
    plt.close()

def create_excel_report(filtered_data, chart_image, output_file):
    wb = Workbook()
    ws = wb.active
    ws.title = "Sales filtered"

    for r in dataframe_to_rows(filtered_data, index=False, header=True):
        ws.append(r)

    if os.path.exists(chart_image):
        img = Image(chart_image)
        ws.add_image(img, 'K1')

    save_excel_report(wb, output_file)

# --- Email Function ---
def send_email(subject, body, to, files):
    from_email = "Your email"
    password = "Your email password"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    for file in files:
        if not os.path.exists(file):
            print(f"File {file} not found")
            return f"Failed: {file} not found"

        try:
            print(f"Attaching file: {file}")
            with open(file, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(file)}")
                msg.attach(part)
        except Exception as e:
            print(f"Error attaching file {file}: {str(e)}")
            return f"Failed: Error attaching file {file}: {str(e)}"

    try:
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to, text)
        server.quit()
        print("Email sent successfully")
        return "Success"
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {str(e)}")
        return f"Failed: SMTP error: {str(e)}"
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return f"Failed: {str(e)}"

# --- Main Application ---
def main():
    file_path = "Path where the CSV file is located/Retail_Sales_Dataset.csv"
    output_file = "Path where the XLSX file with the database and the chart will be created/Report_sales.xlsx"
    chart_image = "Path where the chart image will be created/Create_sales_per_product_pie.png"
    log_file = "Path where the log will be created/email_log.txt"
    
    # --- Reading and processing data ---
    data = read_data(file_path)
    data = clean_data(data)
    data = calculate_total_sales(data)
    filtered_data = filter_sales(data, 100)
    
    # --- Generate and save chart ---
    generate_pie_chart(filtered_data, chart_image)
    
    # --- Generate and save the report ---
    create_excel_report(filtered_data, chart_image, output_file)
    
    # --- Send Email ---
    files_to_send = [output_file, chart_image]
    subject = "Subject text"
    body = "Body text"
    email_status = send_email(subject, body, "Email where the documents will be sent", files_to_send)
    
    # --- Create log ---
    create_log(log_file, email_status, files_to_send)

# --- Entry Point ---
if __name__ == "__main__":
    main()