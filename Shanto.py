import time
import requests
from stem import Signal
from stem.control import Controller

# socks5h ব্যবহার করার ফলে DNS Leak Warning আর আসবে না
PROXIES = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def get_current_ip():
    """মোবাইলে সঠিক ও দ্রুত IP এবং লোকেশন যাচাই করার ফাংশন"""
    try:
        # httpbin বা ipinfo মোবাইল কানেকশনে ভালো রেসপন্স দেয়
        res = requests.get('https://ipinfo.io/json', proxies=PROXIES, timeout=15)
        if res.status_code == 200:
            data = res.json()
            return f"IP: {data.get('ip')} | Country: {data.get('country')} | City: {data.get('city')}"
        return "IP ডাটা পেতে ব্যর্থ হয়েছে।"
    except Exception as e:
        return f"কানেকশন সমস্যা: {e}"

def change_ip():
    """Tor Controller-এ সিগন্যাল পাঠিয়ে আইপি চেঞ্জ করা"""
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            print("--> [✔] নতুন IP এর অনুরোধ পাঠানো হয়েছে!")
    except Exception as e:
        print(f"[✘] IP পরিবর্তন করতে সমস্যা: {e}")

if __name__ == "__Shanto__":
    print("==========================================")
    print("   Mobile Tor IP Changer (DNS Safe)       ")
    print("==========================================\n")
    
    while True:
        print("বর্তমান নেটওয়ার্ক তথ্য:")
        print(get_current_ip())
        
        # আইপি রোটেশন টাইমার (১৫ সেকেন্ড রাখা ভালো যাতে টোর নতুন সার্কিট তৈরি করতে পারে)
        print("\n১৫ সেকেন্ড পর আইপি পরিবর্তন হবে...")
        time.sleep(15)
        
        print("নতুন IP নেওয়ার চেষ্টা করা হচ্ছে...")
        change_ip()
        
        # মোবাইলে নতুন টোর সার্কিট তৈরি হতে ৫ সেকেন্ড সময় প্রয়োজন
        time.sleep(5)
        print("-" * 45)
                                           
