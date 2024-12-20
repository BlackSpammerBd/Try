import os
import subprocess
from flask import Flask, request
import telegram
from dotenv import load_dotenv
import requests

# .env ফাইল থেকে টোকেন এবং চ্যাট আইডি লোড করুন
load_dotenv()

TELEGRAM_TOKEN = os.getenv("7721371260:AAGMALbPA8aAlZP9jrGxar25DM_nqbhsomI")
CHAT_ID = os.getenv("6904067155")

bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Flask অ্যাপ তৈরি করুন
app = Flask(__name__)

# ফর্ম HTML সরাসরি কোডে অন্তর্ভুক্ত
form_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Registration</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f8ff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        form {
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            width: 300px;
        }
        h1 {
            font-size: 20px;
            margin-bottom: 10px;
            color: #333;
        }
        input, label {
            display: block;
            margin-bottom: 10px;
            width: 100%;
        }
        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <form method="POST" enctype="multipart/form-data">
        <h1>Student Registration</h1>
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>
        <label for="phone">Phone:</label>
        <input type="text" id="phone" name="phone" required>
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required>
        <label for="facebook_id">Facebook ID:</label>
        <input type="text" id="facebook_id" name="facebook_id" required>
        <label for="photo">Upload Photo:</label>
        <input type="file" id="photo" name="photo" accept="image/*">
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

# Ngrok URL তৈরি
def start_ngrok(port):
    """Ngrok দিয়ে পাবলিক URL তৈরি করুন"""
    ngrok_path = "ngrok"  # নিশ্চিত করুন ngrok ইনস্টল করা আছে এবং PATH এ যোগ করা হয়েছে
    subprocess.run([ngrok_path, "http", str(port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    response = requests.get("http://127.0.0.1:4040/api/tunnels")
    public_url = response.json()["tunnels"][0]["public_url"]
    return public_url

# ফর্ম পেজ
@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        # ডাটা সংগ্রহ
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        facebook_id = request.form["facebook_id"]
        photo = request.files["photo"]

        # ফটো সংরক্ষণ
        photo_path = os.path.join("uploads", photo.filename)
        os.makedirs("uploads", exist_ok=True)
        photo.save(photo_path)

        # Telegram-এ তথ্য পাঠান
        message = f"New Submission:\nName: {name}\nPhone: {phone}\nEmail: {email}\nFacebook ID: {facebook_id}"
        bot.send_message(chat_id=CHAT_ID, text=message)

        # ফটোও পাঠান
        with open(photo_path, "rb") as photo_file:
            bot.send_photo(chat_id=CHAT_ID, photo=photo_file)

        return "<h1>Thank you! Your form has been submitted successfully.</h1>"

    return form_html

if __name__ == "__main__":
    port = 5000  # Flask পোর্ট
    public_url = start_ngrok(port)  # Ngrok URL
    print(f"Public URL: {public_url}")
    app.run(port=port)
