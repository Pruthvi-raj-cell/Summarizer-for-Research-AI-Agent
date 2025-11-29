import json
import os
from datetime import datetime

class MemoryManager:
    def __init__(self, db_path: str = "data/memories.json"):
        self.db_path = db_path
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        # Initialize empty DB if not exists
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w") as f:
                json.dump([], f)

    def load_memory(self):
        """Loads all past paper memories."""
        try:
            with open(self.db_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def save_memory(self, memories):
        """Saves the updated list to JSON."""
        with open(self.db_path, "w") as f:
            json.dump(memories, f, indent=4)

    def add_paper(self, title: str, summary: str, filename: str):
        """Adds a new paper to memory."""
        memories = self.load_memory()
        
        # Avoid duplicates based on title
        for mem in memories:
            if mem['title'].lower() == title.lower():
                print(f"🧠 Memory: I remember reading '{title}' already.")
                return

        new_entry = {
            "title": title,
            "filename": filename,
            "summary": summary,
            "date_processed": datetime.now().isoformat()
        }
        
        memories.append(new_entry)
        self.save_memory(memories)
        print(f"🧠 Memory: Stored '{title}' in long-term memory.")

    def get_similar_papers(self, current_title: str):
        """
        Simple check to see if we have this paper.
        (Future upgrade: use embeddings for semantic search)
        """
        memories = self.load_memory()
        found = [m for m in memories if m['title'].lower() == current_title.lower()]
        return found[0] if found else None
