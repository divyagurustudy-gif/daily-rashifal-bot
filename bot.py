import g4f
import smtplib
import os
from email.mime.text import MIMEText
from datetime import date

# --- CONFIG ---
BLOGGER_EMAIL = "divyagurustudy.2000@blogger.com" 
MY_GMAIL = "divyagurustudy@gmail.com" 
MY_APP_PASSWORD = os.getenv('GMAIL_PASS') 

def post_to_blogger(content, today_date):
    try:
        subject = f"आज का राशिफल: {today_date}"
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = MY_GMAIL
        msg['To'] = BLOGGER_EMAIL

        print(f"📧 Sending email from {MY_GMAIL} to {BLOGGER_EMAIL}...")
        
        # Connection with Timeout
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30)
        server.login(MY_GMAIL, MY_APP_PASSWORD)
        server.sendmail(MY_GMAIL, [BLOGGER_EMAIL], msg.as_string())
        server.quit()
        
        print("✅ Email successfully sent to SMTP server!")
        return True
    except Exception as e:
        print(f"❌ SMTP Error: {str(e)}")
        return False

if __name__ == "__main__":
    today = date.today().strftime("%d %B %Y")
    # Yahan hum check kar rahe hain ki kya AI response de raha hai
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "user", "content": "Aaj ka rashifal likho Hindi mein short mein."}],
        )
        if response:
            post_to_blogger(response, today)
        else:
            print("❌ AI response empty.")
    except Exception as e:
        print(f"❌ AI Error: {e}")
