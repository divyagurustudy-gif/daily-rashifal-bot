import g4f
import smtplib
import os
from email.mime.text import MIMEText
from datetime import date

# --- CONFIGURATION ---
# Inhe aap badal sakte hain
BLOGGER_EMAIL = "divyagurustudy.2000@blogger.com" 
MY_GMAIL = "divyagurustudy@gmail.com" 

# GitHub Secrets se password uthane ke liye
MY_APP_PASSWORD = os.getenv('MY_APP_PASSWORD') 

def get_detailed_rashifal():
    try:
        today = date.today().strftime("%d %B %Y")
        print(f"🔄 Aaj ({today}) ka Premium Rashifal likh raha hoon...")

        # AI ko vistar se likhne ka instruction
        prompt = (
            f"Aaj {today} ka dainik rashifal Hindi mein vistar se likho. "
            "Har rashi (Mesh se Meen) ke liye 4-5 line likho jisme Career, Health, aur Love life shamil ho. "
            "Style Thakur Prasad aur Dainik Bhaskar jaisa rakho. "
            "Har rashi ka naam Bold Heading mein hona chahiye."
        )

        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        if response:
            # Bakwas symbols hatana aur formatting set karna
            clean = response.replace('**', '').replace('###', '').replace('---', '').replace('#', '')
            return clean, today
        return None, None
    except Exception as e:
        print(f"⚠️ AI Error: {e}")
        return None, None

def post_to_blogger(content, today_date):
    try:
        subject = f"आज का राशिफल: {today_date} | Daily Horoscope"

        # Premium Professional News Design
        html_template = """
        <div style="font-family: 'Helvetica', Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #eeeeee; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">
            
            <div style="background: linear-gradient(135deg, #ff4b2b 0%, #ff416c 100%); padding: 25px; text-align: center; color: white;">
                <h1 style="margin: 0; font-size: 24px; letter-spacing: 1px;">दिव्य गुरु स्टडी - राशिफल</h1>
                <p style="margin: 5px 0 0; font-size: 16px; opacity: 0.9;">दिनांक: [DATE]</p>
            </div>

            <div style="padding: 20px; line-height: 1.8; color: #333; font-size: 16px;">
                <div style="background-color: #fff5f5; border-left: 4px solid #ff416c; padding: 10px 15px; margin-bottom: 20px; color: #b71c1c; font-weight: bold;">
                    आज का भाग्यफल: जानिए अपनी राशि का हाल
                </div>
                
                [CONTENT]
            </div>

            <div style="background-color: #f8f9fa; padding: 20px; text-align: center; border-top: 1px solid #eeeeee;">
                <p style="margin: 0; font-weight: bold; color: #333;">Divya Guru Study</p>
                <p style="margin: 5px 0 15px; font-size: 12px; color: #777;">Rozana update ke liye hamare sath jude rahein.</p>
                <a href="https://divyagurustudy.blogspot.com" style="display: inline-block; text-decoration: none; background: #ff416c; color: white; padding: 10px 25px; border-radius: 50px; font-size: 14px; font-weight: bold; box-shadow: 0 4px 10px rgba(255, 65, 108, 0.3);">Read More on Website</a>
            </div>
        </div>
        """
        
        # Text ko HTML friendly banana
        formatted_content = content.replace('\n', '<br>')
        
        final_html = html_template.replace("[DATE]", today_date)
        final_html = final_html.replace("[CONTENT]", formatted_content)

        msg = MIMEText(final_html, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = MY_GMAIL
        msg['To'] = BLOGGER_EMAIL

        print("🚀 GitHub se Blogger par post bhej raha hoon...")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(MY_GMAIL, MY_APP_PASSWORD)
        server.sendmail(MY_GMAIL, BLOGGER_EMAIL, msg.as_string())
        server.quit()
        print("✅ SUCCESS: Blog post live ho gaya!")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if not MY_APP_PASSWORD:
        print("❌ ERROR: Password nahi mila! GitHub Secrets check karein.")
    else:
        text, d_date = get_detailed_rashifal()
        if text:
            post_to_blogger(text, d_date)
        else:
            print("❌ Error: AI ne content generate nahi kiya.")
