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

    # 1. AI Content Generation
    try:
        print("🤖 AI se Rashifal mangwa raha hoon...")
        
        # Yahan humne model aur messages ko ekdum saaf tarike se likha hai
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "user", "content": f"Aaj {today} ka dainik rashifal Hindi mein vistar se likho."}]
        )
        
        if not response:
            print("❌ Error: AI response is empty.")
            sys.exit(1)
            
        content = str(response).replace('\n', '<br>')
        print("✅ AI ne Rashifal likh diya hai.")

    except Exception as e:
        print(f"❌ AI Critical Error: {str(e)}")
        sys.exit(1)

    # 2. Email Sending
    try:
        print(f"📧 Sending to: {BLOGGER_EMAIL}")
        
        if not MY_APP_PASSWORD:
            print("❌ Error: GMAIL_PASS Secret is missing!")
            sys.exit(1)

        # Premium Design Template
        html_content = f"""
        <div style="font-family: Arial; border: 2px solid #e53935; padding: 20px; border-radius: 10px;">
            <h1 style="color: #e53935; text-align: center;">दैनिक राशिफल: {today}</h1>
            <hr>
            <div style="font-size: 16px; line-height: 1.8;">
                {content}
            </div>
            <hr>
            <p style="text-align: center; color: gray;">Divya Guru Study</p>
        </div>
        """

        msg = MIMEText(html_content, 'html', 'utf-8')
        msg['Subject'] = f"आज का राशिफल: {today}"
        msg['From'] = MY_GMAIL
        msg['To'] = BLOGGER_EMAIL

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30)
        server.login(MY_GMAIL, MY_APP_PASSWORD)
        server.sendmail(MY_GMAIL, [BLOGGER_EMAIL], msg.as_string())
        server.quit()
        
        print("🚀 SUCCESS: Email Sent to Blogger!")

    except Exception as e:
        print(f"❌ Email Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    start_process()
