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
    return requests.post(url, data=data).json().get('access_token')

def update_post(content, today):
    token = get_access_token()
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/{POST_ID}"
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    # HTML Styling for a Premium Look
    styled_content = f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; max-width: 800px; margin: auto; padding: 10px; border: 1px solid #ddd; border-radius: 15px;">
        <div style="background: linear-gradient(135deg, #FF512F 0%, #DD2476 100%); color: white; padding: 20px; text-align: center; border-radius: 12px 12px 0 0;">
            <h1 style="margin: 0; font-size: 28px;">🌟 दिव्य गुरु स्टडी 🌟</h1>
            <p style="margin: 5px 0 0; font-size: 18px;">दैनिक राशिफल - {today}</p>
        </div>
        
        <div style="padding: 15px; background-color: #fffaf0;">
            {content}
        </div>
        
        <div style="background: #f8f9fa; padding: 15px; text-align: center; border-radius: 0 0 12px 12px; font-size: 14px; border-top: 1px solid #eee;">
            <p>धन्यवाद! रोज़ाना राशिफल के लिए हमारी वेबसाइट देखते रहें।</p>
            <strong>Divya Guru Study</strong>
        </div>
    </div>
    """
    
    payload = {
        "title": f"Dainik Rashifal: {today} | आज का राशिफल",
        "content": styled_content
    }
    res = requests.put(url, headers=headers, data=json.dumps(payload))
    return res.status_code == 200

# Baki functions (notify, email) same rahenge...

if __name__ == "__main__":
    today = date.today().strftime("%d %B %Y")
    
    # Powerful AI Prompt for Detailed Content
    detailed_prompt = f"""
    Write a detailed daily horoscope in Hindi for today ({today}). 
    Format instructions:
    1. Provide for all 12 zodiac signs from Mesh to Meen.
    2. For each sign, write at least 60-80 words covering health, career, and love.
    3. Include 'Shubh Rang' (Lucky Color) and 'Shubh Ank' (Lucky Number) for each sign.
    4. Use HTML tags like <h3> for zodiac names and <p> for descriptions.
    5. Add relevant emojis for each zodiac.
    6. Tone should be professional and astrological.
    """

    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "user", "content": detailed_prompt}]
        )
        
        if response and update_post(response, today):
            print("✅ Detailed Post Updated!")
            # notify(today) code here
            # send_confirmation_email(today) code here
    except Exception as e:
        print(f"❌ Error: {e}")
