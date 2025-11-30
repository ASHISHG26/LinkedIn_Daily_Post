import os
import requests
import random
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from news_fetcher import fetch_ai_news  # <-- uses your separate file


# ========== Email Notifications ==========

def send_email(subject: str, body: str):
    email_from = os.getenv("EMAIL_FROM")
    email_to = os.getenv("EMAIL_TO")
    password = os.getenv("EMAIL_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))

    if not email_from or not email_to or not password:
        print("[Email] Missing email credentials in .env")
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = email_from
        msg["To"] = email_to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_from, password)
        server.sendmail(email_from, email_to, msg.as_string())
        server.quit()

        print("[Email] Notification sent.")
    except Exception as e:
        print("[Email] Failed to send notification:", str(e))


load_dotenv()

# ========== ENV Toggle for Auto-posting ==========
AUTOPOST_ENABLED = os.getenv("AUTOPOST_ENABLED", "true").lower() == "true"
if not AUTOPOST_ENABLED:
    print("[AutoPost] Posting disabled via .env (AUTOPOST_ENABLED=false). Exiting.")
    exit(0)
# ========== Groq: generate LinkedIn post text ==========

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0.8,
)

# Step 12: topic/style variations
STYLE_OPTIONS = [
    "News-based AI/LLM insight",
    "Data Engineering Deep Dive",
    "Industry / Career Reflection",
    "Cloud / DevOps / Automation",
]

post_prompt = ChatPromptTemplate.from_template("""
Write a LinkedIn post for Ashish, a data engineer early in his career in India.

Today's style profile: {style_label}

Use this style profile to shape the angle and tone:

- "News-based AI/LLM":
  Focus on one or two recent AI / LLM / GenAI developments from the news context.
  Briefly describe what happened and why it matters.
  Keep it timely and insight-driven, not just a generic definition.

- "Data Engineering Deep Dive":
  Use the news context as a light hook, then go deeper into a concrete
  data engineering concept or practice (pipelines, quality, cost optimisation,
  streaming, data modeling, etc.).
  Make it helpful for other data engineers with at least one practical takeaway.

- "Industry / Career Reflection":
  Use the news context only as background.
  Focus more on a personal or career-focused reflection:
  learning mindset, dealing with change, experimenting with new tools,
  or growing as an engineer in the AI era.

News context:
{news_context}

Objective:
- Create a post based on a current and relevant technology trend that aligns with the news context above.
- The model may naturally choose a theme from areas such as:
  - AI, LLMs, GenAI
  - Data Engineering or Data Analytics
  - Cloud, automation, or DevOps
  - Modern engineering tools, frameworks, or practices
  - Any meaningful shift happening in the tech industry

Style Guidelines:
- Use clear, simple English.
- Tone: professional, thoughtful, and informative — suitable for LinkedIn.
- Can be personal or neutral depending on what fits the message.
- Use short paragraphs (2–3 lines each).
- Do NOT Always start with repetitive generic hooks like:
  “As a data engineer…”, “Imagine…”, “What if I told you…”, “Recently I came across…”. But sometime you can use it to make it more engaging. have the creativity to use it in a way that is not repetitive. Assume the frequency of using it is less than 70%.

Content Requirements:
- Include 1–2 meaningful insights or observations that feel grounded in the news context.
- 120–180 words maximum.
- Use no more than 2 emojis.
- Add 1–3 relevant hashtags at the end.
- Yo can include markdown formatting, bullet points, or quotes — but mostly keep it simple plain paragraph text but sometime you can use it to make it more engaging.
- It should more look like written by Human not AI.


Output:
Return ONLY the LinkedIn post text, nothing else.
""")

def generate_linkedin_post(style_label: str) -> str:
    """
    style_label: one of the STYLE_OPTIONS, e.g.
        - "News-based AI/LLM insight"
        - "Data Engineering Deep Dive"
        - "Industry / Career Reflection"
        - "Cloud / DevOps / Automation"
    """

    # For news-focused styles, pull a bit more context.
    if "News-based" in style_label:
        news_context = fetch_ai_news(max_items=3)
    else:
        # Still pull a little news for inspiration, but lighter.
        news_context = fetch_ai_news(max_items=1)

    if not news_context:
        news_context = "No fresh news available today, but you can still write about ongoing trends and practical learnings."

    messages = post_prompt.format_messages(
        style_label=style_label,
        news_context=news_context,
    )
    res = llm.invoke(messages)
    return res.content.strip()


# ========== LinkedIn: publish post ==========

ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
AUTHOR_URN = os.getenv("LINKEDIN_AUTHOR_URN")  # urn:li:person:...

def post_to_linkedin(commentary: str):
    url = "https://api.linkedin.com/rest/posts"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "LinkedIn-Version": "202502",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    body = {
        "author": AUTHOR_URN,
        "commentary": commentary,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }

    resp = requests.post(url, headers=headers, json=body)
    print("Status:", resp.status_code)
    print("Body:", resp.text)


def main():
    # Step 12: randomly choose today's style
    style_label = random.choice(STYLE_OPTIONS)
    print(f"[Style] Today's style: {style_label}")

    post_text = generate_linkedin_post(style_label)

    # Debug info
    print("----- GENERATED TEXT -----")
    print(post_text)
    print("Length:", len(post_text))
    print("repr():", repr(post_text))
    print("----- END TEXT -----")

    print("\nPosting to LinkedIn...\n")
    # Safety: remove any weird null chars
    post_text = post_text.replace("\x00", "")
    post_to_linkedin(post_text)


if __name__ == "__main__":
    try:
        # Random delay before posting (cron will run between 7–12, or once daily;
        # this adds extra "randomness" within that window if you want)
        # For production: 5 * 60 * 60 (5 hours)
        # For testing: keep it small (e.g. 60 seconds)
        max_delay_seconds = 60  # adjust back to 5*60*60 when you're ready
        delay = random.randint(0, max_delay_seconds)

        target_time = datetime.now() + timedelta(seconds=delay)
        print(f"[Scheduler] Chosen delay: {delay} seconds")
        print(f"[Scheduler] Will post around: {target_time}")

        time.sleep(delay)

        # Run main post logic
        main()

        # Send success email
        send_email(
            subject="LinkedIn Auto-Post: SUCCESS",
            body=f"Your post has been successfully published at {datetime.now()}."
        )

    except Exception as e:
        import traceback
        error_text = traceback.format_exc()
        print("[Error] Something went wrong:", e)

        # Send failure email
        send_email(
            subject="LinkedIn Auto-Post: FAILED ❌",
            body=f"An error occurred:\n\n{error_text}"
        )