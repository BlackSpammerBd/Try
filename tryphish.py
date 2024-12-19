from flask import Flask, render_template_string, request
import threading
import requests
import os

app = Flask(__name__)

# টেলিগ্রাম বটের টোকেন এবং চ্যাট আইডি
BOT_TOKEN = "7721371260:AAGMALbPA8aAlZP9jrGxar25DM_nqbhsomI"
CHAT_ID = "6904067155"

# HTML টেমপ্লেট (ফর্ম)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Course Registration</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f3f4f6;
            margin: 0;
            padding: 20px;
        }
        form {
            background: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            margin: auto;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <h1 style="text-align: center;">Course Registration Form</h1>
    <form method="POST" enctype="multipart/form-data">
        <label for="name">Name:</label><br>
        <input type="text" id="name" name="name" required><br><br>

        <label for="phone">Phone Number:</label><br>
        <input type="text" id="phone" name="phone" required><br><br>

        <label for="email">Email Address:</label><br>
        <input type="email" id="email" name="email" required><br><br>

        <label for="facebook_link">Facebook Profile Link:</label><br>
        <input type="url" id="facebook_link" name="facebook_link" required><br><br>

        <label for="photo">Upload Photo:</label><br>
        <input type="file" id="photo" name="photo" accept="image/*"><br><br>

        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

# TinyURL তৈরি করার ফাংশন
def generate_tinyurl(url):
    api_url = f"http://tinyurl.com/api-create.php?url={url}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.text
    return None
    

# টেলিগ্রামে বার্তা পাঠানোর ফাংশন
def send_message_to_telegram(data):
    # বার্তা তৈরি করা
    message = (
        f"New Course Registration:\n\n"
        f"Name: {data['name']}\n"
        f"Phone: {data['phone']}\n"
        f"Email: {data['email']}\n"
        f"Facebook Profile: {data['facebook_link']}"
    )
    
    # বার্তা পাঠানো
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)
    
    # ফটো পাঠানো (যদি ফাইল সঠিকভাবে সংরক্ষিত হয়)
    if data['photo']:
        photo_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        files = {'photo': open(data['photo'], 'rb')}  # ফাইল খুলুন এবং পাঠান
        payload = {"chat_id": CHAT_ID}
        requests.post(photo_url, data=payload, files=files)
@app.route("/", methods=["GET", "POST"])
def registration_form():
    if request.method == "POST":
        # ফর্ম থেকে ডেটা সংগ্রহ
        form_data = {
            "photo": request.files['photo'],  # ছবি আপলোড ফাইল
            "name": request.form.get("name"),
            "phone": request.form.get("phone"),
            "email": request.form.get("email"),
            "facebook_link": request.form.get("facebook_link"),
        }

        # ফটো ফাইল সেভ করা
        photo_filename = os.path.join("uploads", form_data['photo'].filename)
        form_data['photo'].save(photo_filename)

        # টেলিগ্রামে বার্তা পাঠানো
        send_message_to_telegram(form_data)

        return "<h1>Thank you! Your form has been submitted successfully.</h1>"

    return render_template_string(HTML_TEMPLATE)

def run_server():
    app.run(debug=False, port=5000, use_reloader=False)

# Main function to start Flask and generate TinyURL
if __name__ == "__main__":
    # সার্ভার চালু করা আলাদা থ্রেডে
    threading.Thread(target=run_server).start()

    # ngrok URL (এটি আপনার ngrok কমান্ডের সাথে সঠিকভাবে প্রতিস্থাপন করুন)
    ngrok_url = "http://127.0.0.1:5000"  # এটি পরিবর্তন করুন যদি ngrok URL আলাদা হয়
    tiny_url = generate_tinyurl(ngrok_url)

    if tiny_url:
        print(f"Your TinyURL is: {tiny_url}")
    else:
        print("Failed to generate TinyURL. Please try again.")
