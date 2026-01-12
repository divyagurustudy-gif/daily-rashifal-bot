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
GMAIL_PASS = os.getenv('GMAIL_PASS')

def get_access_token():
    url = "https://oauth2.googleapis.com/token"
    data = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'refresh_token': REFRESH_TOKEN, 'grant_type': 'refresh_token'}
    r = requests.post(url, data=data)
    return r.json().get('access_token')

def send_confirmation_email(today):
    try:
        subject = f"✅ Rashifal Updated: {today}"
        body = f"Hello Admin,\n\nAaj ka rashifal ({today}) successfully update ho gaya hai.\n\nBlog Link: https://www.blogger.com/go/post?blogID={BLOG_ID}&postID={POST_ID}"
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = GMAIL_USER
        msg['To'] = GMAIL_USER
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, [GMAIL_USER], msg.as_string())
        server.quit()
        print("📧 Confirmation Email Sent!")
    except Exception as e:
        print(f"❌ Mail Error: {e}")

def notify(today):
    try:
        url = "https://onesignal.com/api/v1/notifications"
        headers = {"Authorization": f"Basic {ONESIGNAL_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "app_id": ONESIGNAL_APP_ID,
            "included_segments": ["All"],
            "headings": {"en": "आज का राशिफल अपडेट हो गया है! 🌟"},
            "contents": {"en": f"Check your horoscope for {today} now!"},
            "url": "https://divyagurustudy.blogspot.com"
        }
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        print(f"🔔 OneSignal Response: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"❌ Notification Error: {e}")

def update_post(content, today):
    token = get_access_token()
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/{POST_ID}"
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    # Premium HTML Styling
    styled_content = f"""
    <div style="font-family: 'Arial', sans-serif; color: #333; line-height: 1.8; border: 2px solid #f1f1f1; border-radius: 15px; overflow: hidden;">
        <div style="background: linear-gradient(to right, #ff4b1f, #ff9068); color: white; padding: 25px; text-align: center;">
            <h1 style="margin: 0;">🌟 दिव्य गुरु स्टडी 🌟</h1>
            <p style="margin: 5px 0 0;">दैनिक राशिफल - {today}</p>
        </div>
        <div style="padding: 20px; background-color: #ffffff;">
            {content}
        </div>
        <div style="background: #333; color: white; padding: 15px; text-align: center; font-size: 14px;">
            <p>Divya Guru Study © 2024 | Rozana updates ke liye bane rahein</p>
        </div>
    </div>
    """
    
    payload = {"title": f"Dainik Rashifal: {today} | आज का राशिफल", "content": styled_content}
    res = requests.put(url, headers=headers, data=json.dumps(payload))
    return res.status_code == 200

if __name__ == "__main__":
    today = date.today().strftime("%d %B %Y")
    
    # Detailed AI Prompt
    detailed_prompt = f"Write a very detailed daily horoscope in Hindi for today {today}. Cover all 12 signs from Mesh to Meen. For each sign, write 80 words including Career, Health, Love, 'Shubh Rang' and 'Shubh Ank'. Use <h3> for zodiac names and <p> for text."

    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "user", "content": detailed_prompt}]
        )
        
        if response:
            if update_post(response, today):
                print("✅ Blogger Updated!")
                notify(today) # Isse OneSignal notification banegi
                send_confirmation_email(today) # Isse aapko mail aayega
            else:
                print("❌ Blogger Update Failed.")
        else:
            print("❌ AI content generation failed.")
    except Exception as e:
        print(f"❌ System Error: {e}")
