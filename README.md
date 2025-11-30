# 🤖 LinkedIn Auto-Posting Bot (Groq + LangChain + GitHub Actions)

An automated LinkedIn posting system that generates high-quality AI/Tech/Data posts every day using:

- **Groq LLM (Llama 3.3 70B)**
- **LangChain**
- **Indian & Global Tech News Feeds**
- **LinkedIn API (REST Posts)**
- **Random posting schedule between 7 AM – 12 PM IST**
- **Email alerts for success & failure**
- **GitHub Actions automation**
- **Toggle ON/OFF via `.env`**

This project was built end-to-end to automatically create and publish insightful posts for **Ashish**, a data engineer in India.  
It is fully customizable and production-ready.

---

## 🚀 Features

### ✅ **1. Automated Daily Posting**
Posts once every day at a **random time between 7 AM – 12 PM IST**.

### ✅ **2. Uses Real AI/Tech News**
Pulls fresh daily updates from:
- TechCrunch AI
- MIT Tech Review AI
- The Verge AI
- Indian tech feeds (YourStory, Inc42, IndianStartupNews)
- Indian hardware & semiconductor news
- And more…

### ✅ **3. Smart Content Generation**
Groq + LangChain generate:
- 120–180 word polished LinkedIn posts  
- No repeated openings (“Imagine…”, “What if I told you…”)
- Professional, simple English  
- 1–3 meaningful hashtags  
- Maximum 2 emojis  
- Clean formatting "no broken text"

### ✅ **4. Randomized Style Selection**
Every day selects one style:

- **AI / LLM News Insight**
- **Data Engineering Deep Dive**
- **Industry Trend Reflection**

### ✅ **5. Email Notifications**
Sends you an email when:
- ✔ Post succeeds  
- ❌ Something fails  

### ✅ **6. Toggle Auto-Posting**
Set in `.env`:
AUTO_POST_ENABLED=true
Set to:
AUTO_POST_ENABLED=false

And GitHub Actions will **skip posting**.

### ✅ **7. Fully Automated via GitHub Actions**
Your machine doesn’t need to stay ON.  
GitHub runs everything on the cloud.

---

## 📁 Project Structure
- LinkedIn_Daily_Post/
- │
- ├── post_with_groq.py        # Main automation script
- ├── news_fetcher.py          # Fetches AI/tech/news from India & global
- ├── daily_post.sh            # Local cron script (optional)
- ├── .github/
- │   └── workflows/
- │       └── daily_post.yml   # GitHub Actions workflow
- ├── .env                     # Secrets (LOCAL ONLY)
- └── README.md                # This file

---

## 🔧 Environment Variables

Create a `.env` file:
- GROQ_API_KEY=your_key
- LINKEDIN_ACCESS_TOKEN=your_token
- LINKEDIN_AUTHOR_URN=urn:li:person:xxxx
- EMAIL_FROM=your_email@gmail.com
- EMAIL_TO=your_email@gmail.com
- EMAIL_PASSWORD=app_specific_password
- SMTP_SERVER=smtp.gmail.com
- SMTP_PORT=587
- AUTO_POST_ENABLED=true

---

## 📰 News Fetching (Indian + Global)

`news_fetcher.py` pulls news from:

### **AI & LLM Feeds**
- TechCrunch AI  
- MIT Tech Review AI  
- The Verge AI  
- Google AI Blog RSS  
- OpenAI developer news (converted RSS)  

### **Indian Tech Feeds**
- YourStory
- Inc42
- IndianStartupNews
- The Hindu Science/Tech
- Times of India – Tech  
- Economic Times Technology  

### **Indian Hardware & Semiconductor**
- ElectronicsB2B  
- Semiconductor India News  
- IndiaAI.gov.in  
- Ministry of Electronics (MeitY)

All content is cleaned, deduplicated, summarized, and passed to Groq as context.

---

## 🤖 How the AI Generates Posts

The system uses an optimized prompt that ensures:

- Quality writing  
- No repeated opening phrases  
- Clear paragraphs (2–3 lines each)  
- Context-grounded insights  
- No fabricated facts  
- Realistic expert tone  

---

## 🎯 Posting Styles

Random daily selection:

1. **News-based AI/LLM Insight**  
2. **Data Engineering Deep Dive**  
3. **Industry or Career Reflection**  

Adds variety to your profile.

---

## ☁ GitHub Actions Automation

Your workflow file (`.github/workflows/daily_post.yml`) runs:

- Every day  
- Between **7 AM–12 PM IST**  
- With random delays  
- On GitHub cloud runners  

You don’t need to keep laptop ON.

---

## 🛑 How to Disable Auto-Posting

Just set:
AUTO_POST_ENABLED=false

GitHub Actions will detect it and exit safely.

---

## 📬 Email Alerts

You get notified for:

- **SUCCESS** → Post published  
- **FAILURE** → Exception with full traceback  

Works using Gmail SMTP or any SMTP provider.

---

## 🧪 Local Testing

Run:
python post_with_groq.py

For instant test:
MAX_DELAY_SECONDS=0
AUTO_POST_ENABLED=true

---

## 🤝 Contributing

Want to expand?
- Add more feed categories  
- Add topic-focused prompts  
- Add analytics  
- Add a vector DB for history tracking  

PRs welcome.

---

## 📄 License

MIT License — free to modify & use.

---

## ❤️ Built By

**Ashish Kumar Gupta**  
Data Engineer • India  

Fully automated, Cloud-powered, LLM-generated daily LinkedIn content engine 🚀
