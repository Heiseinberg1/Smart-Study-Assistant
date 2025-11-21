from google import genai
from dotenv import load_dotenv
import os   
load_dotenv()
API_KEY = os.getenv("GOOGLE_AI_API_KEY")
client = genai.Client(api_key=API_KEY)

class QuizAgent:
    def generate_quiz(self, topic, num_questions=5):
        prompt = f"""Create a{num_questions}-questions quiz on the topic:{topic}
        Include:5 multiple-choice questions with 4 options each and indicate the correct answer."""
        response = client.models.generate_content(
            model = "gemini-2.0-flash",
            contents=prompt
        )
        return response.text