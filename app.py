from flask import Flask, request, send_file, send_from_directory
import os
import uuid
from topsis import topsis
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/style.css")
def style():
    return send_from_directory(BASE_DIR, "style.css")

@app.route("/script.js")
def script():
    return send_from_directory(BASE_DIR, "script.js")

@app.route("/calculate", methods=["POST"])
def calculate():
    if "file" not in request.files:
        return "No file uploaded."

    file = request.files["file"]
    weights = request.form.get("weights")
    impacts = request.form.get("impacts")
    email = request.form.get("email")

    if file.filename == "":
        return "No selected file."

    unique_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_FOLDER, unique_id + "_" + file.filename)
    output_path = os.path.join(UPLOAD_FOLDER, unique_id + "_result.csv")

    file.save(input_path)

    try:
        topsis(input_path, weights, impacts, output_path)
    except SystemExit:
        return "Error occurred during TOPSIS calculation."
    
    sender_email = os.getenv("EMAIL_USER")
    app_password = os.getenv("EMAIL_PASSWORD")

    try:
        msg = EmailMessage()
        msg["Subject"] = "TOPSIS Result"
        msg["From"] = sender_email
        msg["To"] = email
        msg.set_content("Please find attached your TOPSIS result file.")

        with open(output_path, "rb") as f:
            file_data = f.read()
            msg.add_attachment(
                file_data,
                maintype="application",
                subtype="octet-stream",
                filename="TOPSIS_Result.csv"
            )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)

        return "Result successfully sent to your email!"

    except Exception as e:
        return f"Email sending failed: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
