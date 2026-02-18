import os
from datetime import datetime

class FileHandler:
    def __init__(self, base_dir="."):
        self.input_tickets_dir = os.path.join(base_dir, "data", "input_tickets")
        self.forms_dir = os.path.join(base_dir, "data", "forms")
        self.drafts_dir = os.path.join(base_dir, "outputs", "drafts")
        self._initialize_directories()

    def _initialize_directories(self):
        """Creates the necessary directory structure if it doesn't exist."""
        directories = [self.input_tickets_dir, self.forms_dir, self.drafts_dir]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            
    def save_draft(self, ticket_id: str, content: str) -> str:
        """Saves the final agent draft for human review."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"draft_{ticket_id}_{timestamp}.txt"
        filepath = os.path.join(self.drafts_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
        return filepath