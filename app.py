from flask import Flask, render_template, request, send_file, jsonify
import requests
import io
from tools.remove import remove_background  # Import fungsi remove BG

app = Flask(__name__)

OCR_API_URL = "https://your-vercel-ocr.vercel.app/ocr"  # Ganti dengan URL API OCR di Vercel

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
    return jsonify({"error": "OCR API gagal"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
