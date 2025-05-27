from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

BACKEND_URL = "http://backend:5000/api/message"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Frontend Message App</title>
</head>
<body>
    <h1>Latest Message from Database</h1>
    <p>{{ message }}</p>

    <h2>Send a New Message</h2>
    <form method="POST">
        <input type="text" name="content" required>
        <button type="submit">Send</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("content")
        try:
            response = requests.post(BACKEND_URL, json={"content": content})
        except Exception as e:
            return f"Error sending message: {e}"

    try:
        response = requests.get(BACKEND_URL)
        message = response.json().get("message", "No message found.")
    except Exception as e:
        message = f"Error fetching message: {e}"

    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)


