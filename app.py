from flask import Flask, render_template, request, send_file, jsonify
import requests
import io
from tools.remove import remove_background  # Import fungsi remove BG
import os  # To access environment variables

app = Flask(__name__)

OCR_API_URL = "https://freetools-pazaftr46-umar-syafiqs-projects.vercel.app"  # Replace with your actual OCR API URL

@app.route("/")
def home():
    return render_template("upload.html")

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    file = request.files["image"]
    output_image = remove_background(file.read())
    return send_file(io.BytesIO(output_image), mimetype="image/png")

@app.route("/ocr", methods=["POST"])
def ocr():
    file = request.files["image"]
    files = {"image": (file.filename, file.read(), file.content_type)}
    
    response = requests.post(OCR_API_URL, files=files)
    if response.status_code == 200:
        return render_template("ocr.html", text=response.json()["text"])
    return jsonify({"error": "OCR API failed"}), 500

if __name__ == "__main__":
    # Use the PORT environment variable, Render will provide it during deployment
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT isn't set
    app.run(debug=True, host="0.0.0.0", port=port)
