from google import genai
from dotenv import load_dotenv
import os     
load_dotenv()
API_KEY= os.getenv("GOOGLE_AI_API_KEY")
client = genai.Client(api_key=API_KEY)

class SummarizerAgent:
    def summarize(self, text):
        prompt = f"""Summarize the following text:{text}
        Include:oneline TL;DR, 5 bullet points, Detailed 200-word summary"""
        response = client.models.generate_content(
            model = "gemini-2.0-flash",
            contents=prompt
        )
        return response.text