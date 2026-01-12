import os, g4f, json, requests, smtplib
from email.mime.text import MIMEText
from datetime import date

# --- SECRETS SE DATA LENA ---
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
BLOG_ID = os.getenv('BLOG_ID')
POST_ID = os.getenv('POST_ID')
ONESIGNAL_APP_ID = os.getenv('ONESIGNAL_APP_ID')
ONESIGNAL_API_KEY = os.getenv('ONESIGNAL_API_KEY')
GMAIL_USER = "divyagurustudy@gmail.com"
GMAIL_PASS = os.getenv('GMAIL_PASS') # Aapka 16-digit App Password

def get_access_token():
    url = "https://oauth2.googleapis.com/token"
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': REFRESH_TOKEN,
        'grant_type': 'refresh_token'
    }
    return requests.post(url, data=data).json().get('access_token')

def send_confirmation_email(today):
    """Aapko personal email bhejne ke liye"""
    try:
        subject = f"✅ Rashifal Updated: {today}"
        body = f"Hello Admin,\n\nAaj ka rashifal ({today}) successfully update ho gaya hai aur users ko notification bhej di gayi hai.\n\nLink: https://divyagurustudy.blogspot.com"
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = GMAIL_USER
        msg['To'] = GMAIL_USER # Aapko khud hi mail aayega

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, [GMAIL_USER], msg.as_string())
        server.quit()
        print("📧 Confirmation Email Sent!")
    except Exception as e:
        print(f"❌ Mail Error: {e}")

def update_post(content, today):
    token = get_access_token()
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/{POST_ID}"
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {
        "title": f"Dainik Rashifal: {today}",
        "content": f"<div style='font-family:Arial; line-height:1.6;'>{content}</div>"
    }
    res = requests.put(url, headers=headers, data=json.dumps(payload))
    return res.status_code == 200

def notify(today):
    url = "https://onesignal.com/api/v1/notifications"
    headers = {"Authorization": f"Basic {ONESIGNAL_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "included_segments": ["Subscribed Users"],
        "headings": {"en": "आज का राशिफल अपडेट हो गया है! 🌟"},
        "contents": {"en": f"Check your horoscope for {today} now!"},
        "url": "https://divyagurustudy.blogspot.com"
    }
    requests.post(url, headers=headers, data=json.dumps(payload))

if __name__ == "__main__":
    today = date.today().strftime("%d-%m-%Y")
    try:
        # AI content generation
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "user", "content": f"Write {today} daily horoscope in Hindi with zodiac icons for all 12 signs."}]
        )
        
        if response and update_post(response, today):
            print("✅ Blogger Post Updated!")
            notify(today) # Push Notification
            send_confirmation_email(today) # Personal Email
        else:
            print("❌ Process Failed at Blogger Update.")
    except Exception as e:
        print(f"❌ System Error: {e}")
