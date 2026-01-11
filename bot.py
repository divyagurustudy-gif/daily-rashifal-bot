import g4f
import smtplib
import os
import sys
from email.mime.text import MIMEText
from datetime import date

# --- CONFIG ---
BLOGGER_EMAIL = "divyagurustudy.2000@blogger.com" 
MY_GMAIL = "divyagurustudy@gmail.com" 
MY_APP_PASSWORD = os.getenv('GMAIL_PASS') 

def start_process():
    today = date.today().strftime("%d %B %Y")
    print(f"--- Process Started for {today} ---")

    # 1. AI se Content mangwana
    try:
        print("🤖 AI se Rashifal mangwa raha hoon...")
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Aaj {today} ka dainik rashifal Hindi mein vistar se likho."}],
        )
        
        if not response or len(response) < 100:
            print("❌ Error: AI ne sahi response nahi diya.")
            sys.exit(1) # Isse GitHub par Red Cross dikhega
        
        content = response.replace('\n', '<br>')
        print("✅ AI ne Rashifal likh diya hai.")

    except Exception as e:
        print(f"❌ AI Critical Error: {str(e)}")
        sys.exit(1)

    # 2. Email Bhejna
    try:
        print(f"📧 Email bhejne ki koshish: {MY_GMAIL} -> {BLOGGER_EMAIL}")
        
        if not MY_APP_PASSWORD:
            print("❌ Error: GMAIL_PASS Secret nahi mila!")
            sys.exit(1)

        msg = MIMEText(f"<h2>Rashifal {today}</h2><br>{content}", 'html', 'utf-8')
        msg['Subject'] = f"आज का राशिफल: {today}"
        msg['From'] = MY_GMAIL
        msg['To'] = BLOGGER_EMAIL

        # SMTP Connection
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30)
        server.login(MY_GMAIL, MY_APP_PASSWORD)
        server.sendmail(MY_GMAIL, [BLOGGER_EMAIL], msg.as_string())
        server.quit()
        
        print("🚀 SUCCESS: Email Sent! Sent folder check karein.")

    except smtplib.SMTPAuthenticationError:
        print("❌ Error: Gmail App Password galat hai.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Email Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    start_process()
