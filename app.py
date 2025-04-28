from flask import Flask, request, send_file, render_template, jsonify
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download_video():
    url = request.form.get("url")
    if not url:
        return jsonify({"error": "URL is required!"}), 400

    ydl_opts = {
        "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
        "format": "best",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
