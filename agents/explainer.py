from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GOOGLE_AI_API_KEY")
client = genai.Client(api_key=API_KEY)

class ExplainerAgent:
    def explain(self, topic):
        prompt = f"""You are an expert ECE + AI tutor. Explain the topic:{topic}
        Include:definations, real-world intuitions, 3 short practice questions"""
        response = client.models.generate_content(
            model = "gemini-2.0-flash",
            contents=prompt
        )
        return response.text