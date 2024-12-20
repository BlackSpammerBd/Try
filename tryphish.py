import os
from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# Telegram Bot Configurations
BOT_TOKEN = "7721371260:AAGMALbPA8aAlZP9jrGxar25DM_nqbhsomI"
CHAT_ID = "6904067155"

# HTML Template with CSS and JavaScript
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
            border: 1px solid #ff4d4d;
        }
        input:invalid:focus {
            outline: none;
            box-shadow: 0 0 5px #ff4d4d;
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
    <script>
        function validateForm() {
            const form = document.forms["studentForm"];
            const fields = ["name", "phone", "email", "facebook", "photo"];
            let valid = true;

            fields.forEach(field => {
                const input = form[field];
                if (!input.value) {
                    input.style.border = "2px solid #ff4d4d";
                    valid = false;
                } else {
                    input.style.border = "1px solid #dddddd";
                }
            });

            if (!valid) {
                alert("Please fill out all required fields.");
            }

            return valid;
        }
    </script>
</head>
<body>
    <div class="container">
        <h2>Submit Your Information</h2>
        <form name="studentForm" action="/submit" method="post" enctype="multipart/form-data" onsubmit="return validateForm()">
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

# Success Page Template with CSS
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
    return render_template_string(html_template)

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    phone = request.form["phone"]
    email = request.form["email"]
    facebook = request.form["facebook"]
    photo = request.files["photo"]

    # Save photo locally
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

    # Send photo to Telegram
    with open(photo_path, "rb") as file:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto",
            data={"chat_id": TELEGRAM_CHAT_ID},
            files={"photo": file}
        )

    # Return success page
    return render_template_string(success_template)

if __name__ == "__main__":
    app.run(debug=True)
