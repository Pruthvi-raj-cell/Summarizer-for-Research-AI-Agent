import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load env variables to get GOOGLE_API_KEY
load_dotenv()

class SummarizerAgent:
    def __init__(self, model: str = "gemini-1.5-flash"):
        # Configure the Google API
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            # If the class is initialized but key is missing
            raise ValueError("GOOGLE_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def summarize_chunk(self, text_chunk: str) -> dict:
        """
        Summarizes a chunk using Google Gemini.
        """
        prompt = f"""
        You are an expert academic researcher. 
        Analyze the following text chunk from a research paper.
        
        Text Chunk:
        "{text_chunk}"
        
        Task:
        1. Identify the likely section (e.g., Introduction, Methods, Results).
        2. Summarize key info in 3-5 bullet points.
        3. Extract specific numerical findings.
        
        Output strict JSON format only:
        {{
            "section_guess": "Name of section",
            "summary_points": ["point 1", "point 2"],
            "key_findings": ["finding 1"],
            "confidence_score": 0.8
        }}
        """

        try:
            # Generate content
            response = self.model.generate_content(prompt)
            text_response = response.text.strip()
            
            # Clean up markdown formatting if Gemini adds it (e.g. ```json ... ```)
            if text_response.startswith("```"):
                text_response = text_response.replace("```json", "").replace("```", "")
            
            return json.loads(text_response)
            
        except Exception as e:
            print(f"Error summarizing chunk: {e}")
            return {
                "section_guess": "Error",
                "summary_points": [f"Error processing chunk"],
                "key_findings": [],
                "confidence_score": 0.0
            }