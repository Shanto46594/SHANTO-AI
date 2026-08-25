import time
import requests
from stem import Signal
from stem.control import Controller

# Tor SOCKS5h Proxy সেটআপ (DNS Leak প্রতিরোধের জন্য socks5h ব্যবহার করা হয়েছে)
PROXIES = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def get_current_ip():
    """Tor Proxy দিয়ে বর্তমান IP Address এবং লোকেশন দেখার ফাংশন"""
    try:
        # IP info API (আগের ipify-এর চেয়ে এটি ভালো রেসপন্স দেয়)
        res = requests.get('https://ipinfo.io/json', proxies=PROXIES, timeout=15)
        if res.status_code == 200:
            data = res.json()
            return f"IP: {data.get('ip')} | Country: {data.get('country')}"
        return "IP চেক করতে সমস্যা হয়েছে।"
    except Exception as e:
        return f"কানেকশন পাওয়া যাচ্ছে না (Tor চালু আছে তো?): {e}"

def change_ip():
    """Tor Controller-কে NEWNYM সিগন্যাল পাঠিয়ে IP পরিবর্তন করা"""
    try:
        # ControlPort 9051-এ সংযোগ নেওয়া
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()  # কোন পাসওয়ার্ড ছাড়াই অথেনটিকেশন (CookieAuthentication 0 হলে)
            controller.signal(Signal.NEWNYM)
            print("--> সিগন্যাল পাঠানো হয়েছে! নতুন IP তৈরি হচ্ছে...")
    except Exception as e:
        print(f"IP পরিবর্তনের সিগন্যাল ব্যর্থ হয়েছে: {e}")

if __name__ == "__SHANTO__":
    print("====================================")
    print("      Tor Auto IP Changer Started   ")
    print("====================================\n")
    
    while True:
        print("বর্তমান নেটওয়ার্ক তথ্য:")
        print(get_current_ip())
        
        # IP রোটেশন সময় (১০ সেকেন্ড)
        print("\n১০ সেকেন্ড অপেক্ষা করা হচ্ছে...")
        time.sleep(10)
        
        print("IP পরিবর্তন করা হচ্ছে...")
        change_ip()
        
        # Tor Circuit নতুন IP সেট করার জন্য ৩ সেকেন্ড অতিরিক্ত সময় দেওয়া
        time.sleep(3)
        print("-" * 40)
    
