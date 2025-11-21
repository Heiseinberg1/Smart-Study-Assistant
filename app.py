import streamlit as st
from dotenv import load_dotenv
import json
import os
from google import genai

from agents.summarizer import SummarizerAgent
from agents.quiz import QuizAgent
from agents.explainer import ExplainerAgent

from tools.memory import remember, recall
from tools.runner import run_python
from tools.pdfreader import extract_pdf_text
        
load_dotenv()
API_KEY = os.getenv("GOOGLE_AI_API_KEY")
client = genai.Client(api_key=API_KEY)


DATA_FILE = "data/user_data.json"

if not os.path.exists("data"):
    os.makedirs("data")
def load_user_data():
    if not os.path.exists(DATA_FILE):
        return {"chat_history": [], "pdf_text": ""}
    with open(DATA_FILE, "r") as f:
        return json.load(f)
def save_user_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
user_data = load_user_data()

st.set_page_config(page_title="Smart Study Assistant", layout="wide")
st.title("Smart Study Assistant 📚🤖")
st.write("Your Personalized Tutor")


with st.sidebar:
    st.header("⚙ Select Mode")

    mode = st.radio(
        "Choose an agent:",
        ["Chat Mode", "Explainer Agent", "Quiz Agent", "Summarizer Agent"]
    )

    st.divider()

    st.header("📄 Upload PDF")
    pdf = st.file_uploader("Upload PDF file", type="pdf")

    if pdf:
        pdf_text = extract_pdf_text(pdf)
        user_data["pdf_text"] = pdf_text
        save_user_data(user_data)
        st.success("PDF uploaded and processed!")

    if st.button("Clear Chat History"):
        user_data["chat_history"] = []
        save_user_data(user_data)
        st.success("Chat history cleared!")
        
for msg in user_data["chat_history"]:
    st.chat_message(msg["role"]).write(msg["content"])


user_input = st.chat_input("Ask me something...")

if user_input:

    # show the user's message
    st.chat_message("user").write(user_input)
    user_data["chat_history"].append({"role": "user", "content": user_input})

    # ---------------------
    # SELECTED AGENT MODE
    # ---------------------

    if mode == "Explainer Agent":
        agent = ExplainerAgent(client)
        response = agent.explain(user_input)

    elif mode == "Quiz Agent":
        agent = QuizAgent(client)
        response = agent.generate_quiz(user_input)

    elif mode == "Summarizer Agent":
        agent = SummarizerAgent(client)
        response = agent.summarize(user_input)

    else:  
        # Chat Mode (uses PDF + history)
        context = ""

        if user_data["pdf_text"]:
            context += f"PDF Knowledge:\n{user_data['pdf_text']}\n\n"

        for m in user_data["chat_history"]:
            context += f"{m['role']}: {m['content']}\n"

        context += f"User: {user_input}\nAssistant:"

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=context
        ).text

    st.chat_message("assistant").write(response)
    user_data["chat_history"].append({"role": "assistant", "content": response})

    save_user_data(user_data)
    