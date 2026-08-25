import time
import requests
from stem import Signal
from stem.control import Controller

# Tor SOCKS5 Proxy সেটআপ (Tor-এর ডিফল্ট পোর্ট 9050 বা 9150)
PROXIES = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}

def get_current_ip():
    """টোর প্রক্সি দিয়ে বর্তমানে কোন IP টি ব্যবহৃত হচ্ছে তা চেক করা"""
    try:
        response = requests.get('https://api.ipify.org', proxies=PROXIES, timeout=10)
        return response.text
    except Exception as e:
        return f"কানেকশন এরর (Tor সার্ভিস চালু আছে তো?): {e}"

def change_ip():
    """Tor Controller-কে সিগন্যাল পাঠিয়ে নতুন IP নেওয়া"""
    try:
        # Tor Control Port (ডিফল্ট 9051)
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password="")  # আপনার torrc ফাইলে পাসওয়ার্ড দেওয়া থাকলে এখানে বসাবেন
            controller.signal(Signal.NEWNYM)
            print("--> নতুন IP সফলভাবে নেওয়া হয়েছে!")
    except Exception as e:
        print(f"IP পরিবর্তন করতে সমস্যা হয়েছে: {e}")

if __name__ == "__main__":
    print("=== Auto IP Changer Started ===")
    
    # প্রতি ১০ সেকেন্ড পরপর আইপি টেস্ট ও পরিবর্তন করার লুপ
    while True:
        current_ip = get_current_ip()
        print(f"বর্তমান IP Address: {current_ip}")
        
        # ১০ সেকেন্ড অপেক্ষা
        time.sleep(10)
        
        # আইপি পরিবর্তনের অনুরোধ
        print("IP পরিবর্তন করা হচ্ছে...")
        change_ip()
      
