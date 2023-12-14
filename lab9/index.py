import gradio as gr
from ftplib import FTP
import smtplib, ssl
import os

from dotenv import load_dotenv
load_dotenv()


def file_upload_fnc(filename):
    ftp = FTP("138.68.98.108")
    ftp.login(user="yourusername", passwd="yourusername")
    filename_only = os.path.basename(filename)

    with open(filename, 'rb') as f:
        ftp.storbinary(f"STOR {filename_only}", f)
    ftp.quit()
    return f"http://138.68.98.108/{filename_only}"  # Assuming file accessible via this URL


def send_email_fnc(recipient, subject, body, file):
    port = 465  # For SSL
    password = os.getenv('PASSWORD') # Input your email password here

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(os.getenv('EMAIL'), password)

        file_url = file_upload_fnc(file)
        body_with_url = f"{body}\n\nFile URL: {file_url}"

        message = f"Subject: {subject}\n\n{body_with_url}"

        server.sendmail(os.getenv('EMAIL'), recipient, message)

# Configure the Gradio interface fields 
inputs = [
    gr.Textbox(label="Send email to", type="text"),
    gr.Textbox(label="Email Subject", type="text"),
    gr.Textbox(label="Email body", type="text"),
    gr.File(label="Upload File")
]


def mail_client_fnc(recipient, subject, body, file):
    send_email_fnc(recipient, subject, body, file)
    return "Email Sent Successfully!"


iface = gr.Interface(fn=mail_client_fnc, inputs=inputs, outputs="text", title="Mail Client")
iface.launch()