from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()


# Define the exact JSON structure the agent must output
class TicketTriage(BaseModel):
    category: str = Field(description="The general category of the issue (e.g., Order, Refund, Technical Support, Inquiry)")
    urgency: str = Field(description="Rate the urgency. Must be a string value between '1' (Low) and '5' (Critical)")
    sentiment: str = Field(description="The customer's emotional state (e.g., Angry, Frustrated, Neutral, Happy)")
    summary: str = Field(description="A strict 1-sentence summary of the core problem")

class TriageAgent:
    def __init__(self):
        # Using Llama 3.3 70B for high-quality reasoning and fast inference
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile", 
            temperature=0
        ).with_structured_output(TicketTriage)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert customer support triage specialist. Analyze the ticket and extract the required fields accurately."),
            ("human", "{ticket_text}")
        ])
        
        self.chain = self.prompt | self.llm

    def process_ticket(self, ticket_text: str) -> TicketTriage:
        return self.chain.invoke({"ticket_text": ticket_text})