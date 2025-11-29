import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class SummarizerAgent:
    def __init__(self, model: str = "gpt-4o"):
        self.model = model

    def summarize_chunk(self, text_chunk: str) -> dict:
        prompt = f"""
        Analyze this research paper text.
        Text: "{text_chunk[:10000]}" ... (truncated)
        
        Return JSON with:
        - "section_guess": (e.g., Intro, Methods)
        - "summary_points": [list of 3 key points]
        """
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a research assistant returning JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error: {e}")
            return {"section_guess": "Error", "summary_points": []}
