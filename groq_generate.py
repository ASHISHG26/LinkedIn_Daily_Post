import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",  # you can switch to another Groq model if you want
    temperature=0.8
)   

prompt = ChatPromptTemplate.from_template("""
You are writing a LinkedIn post for a data engineer early in his career.

Constraints:
- Topic: latest trends or insights in AI / modern data / LLMs.
- Tone: simple, professional, slightly conversational.
- Length: 120-200 words.
- Add 2-3 relevant hashtags at the end (e.g. #AI #DataEngineering #LLM).
- No more than 2 emojis.
- Write as if the author is sharing a learning or insight, not doing marketing.

Return ONLY the LinkedIn post text, nothing else.
""")

def generate_linkedin_post() -> str:
    messages = prompt.format_messages()
    res = llm.invoke(messages)
    return res.content.strip()

if __name__ == "__main__":
    text = generate_linkedin_post()
    print("Generated post:\n")
    print(text)