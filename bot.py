import os, g4f, json, requests, smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta, timezone

# --- SECRETS SE DATA LENA ---
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
BLOG_ID = os.getenv('BLOG_ID')
POST_ID = os.getenv('POST_ID')
ONESIGNAL_APP_ID = os.getenv('ONESIGNAL_APP_ID')
ONESIGNAL_API_KEY = os.getenv('ONESIGNAL_API_KEY')
GMAIL_USER = "divyagurustudy@gmail.com"
GMAIL_To = "devoloperworld@gmail.com"
GMAIL_PASS = os.getenv('GMAIL_PASS')

def get_access_token():
    url = "https://oauth2.googleapis.com/token"
    data = {
        'client_id': CLIENT_ID, 
        'client_secret': CLIENT_SECRET, 
        'refresh_token': REFRESH_TOKEN, 
        'grant_type': 'refresh_token'
    }
    r = requests.post(url, data=data)
    return r.json().get('access_token')

def send_confirmation_email(today):
    try:
        subject = f"✅ Post Updated: {today}"
        body = f"Hello Admin,\n\nAaj ka rashifal ({today}) successfully update ho gaya hai.\n\nLink: https://www.blogger.com/go/post?blogID={BLOG_ID}&postID={POST_ID}"
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = GMAIL_USER
        msg['To'] = GMAIL_To
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, [GMAIL_To], msg.as_string())
        server.quit()
        print("📧 Email Sent!")
    except Exception as e:
        print(f"❌ Mail Error: {e}")

def notify(today):
    try:
        url = "https://onesignal.com/api/v1/notifications"
        headers = {
            "Authorization": f"Basic {ONESIGNAL_API_KEY}", 
            "Content-Type": "application/json; charset=utf-8"
        }
        payload = {
            "app_id": ONESIGNAL_APP_ID,
            "included_segments": ["All"],
            "headings": {"en": "आज का राशिफल अपडेट हो गया है! 🌟"},
            "contents": {"en": f"जानिए आज का अपना भाग्य - {today}"},
            "url": "https://divyagurustudy.blogspot.com" # Click karne par yahan jayega
        }
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        print(f"🔔 OneSignal: {r.status_code}")
    except Exception as e:
        print(f"❌ Notification Error: {e}")

def update_post(ai_content, today):
    token = get_access_token()
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/{POST_ID}"
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    # App-Friendly Clean Styling
    styled_content = f"""
    <div style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #222; line-height: 1.6; border: 1px solid #eee; border-radius: 10px; overflow: hidden; max-width: 100%; margin: 0 auto; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
        <div style="background: #fdfdfd; padding: 20px; text-align: center; border-bottom: 3px solid #ff4b1f;">
            <h2 style="margin: 0; color: #ff4b1f; font-size: 24px;">✨ आज का राशिफल ✨</h2>
            <p style="margin: 5px 0 0; color: #666; font-size: 14px;">दिनांक: {today}</p>
        </div>
        <div style="padding: 15px; background-color: #ffffff;">
            {ai_content}
        </div>
        <div style="background: #fafafa; color: #999; padding: 10px; text-align: center; font-size: 11px;">
            <p>Horoscope data updated daily</p>
        </div>
    </div>
    """
    
    payload = {
        "title": f"Dainik Rashifal: {today}", 
        "content": styled_content,
        "labels": ["daily rashifal"]
    }
    
    res = requests.put(url, headers=headers, data=json.dumps(payload))
    return res.status_code == 200

if __name__ == "__main__":
    # --- IST TIMEZONE FIX (Important) ---
    # GitHub UTC use karta hai (IST se 5:30 ghante peeche)
    ist = timezone(timedelta(hours=5, minutes=30))
    today_ist = datetime.now(ist)
    today = today_ist.strftime("%d %b %Y")
    
    print(f"🕒 Current Indian Time (IST): {today}")

    detailed_prompt = f"""Write a detailed daily horoscope in Hindi for {today}.
    Provide for all 12 signs (Mesh to Meen). 
    For each sign:
    - Write 80-100 words (Career, Health, Love).
    - Add 'Shubh Rang' and 'Shubh Ank'.
    - Use <h3> for zodiac names and <p> for descriptions.
    - Important: Do not mention any website name like 'Divya Guru Study' in the content."""

    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "user", "content": detailed_prompt}]
        )
        
        if response:
            if update_post(response, today):
                print(f"✅ Blog Updated for {today}!")
                notify(today)
                send_confirmation_email(today)
            else:
                print("❌ Update Failed.")
        else:
            print("❌ AI Generation Failed.")
    except Exception as e:
        print(f"❌ Error: {e}")
