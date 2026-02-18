from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class DraftOutput(BaseModel):
    email_body: str = Field(description="The final email text to send to the customer")
    is_missing_info: bool = Field(description="True if the extraction data was missing a name, amount, or date. False otherwise.")

class DraftingAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile", 
            temperature=0.3 # Slightly higher temperature for natural writing
        ).with_structured_output(DraftOutput)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a senior customer support specialist. 
            
            Analyze the Data and the 'human_input'.
            
            ### CRITICAL INSTRUCTIONS:
            1. **ITERATIVE FEEDBACK**: If the 'human_input' contains feedback on a previous draft (e.g., 'Stop mentioning codes' or 'Be more friendly'), follow that instruction strictly to REWRITE the email.
            2. **CODE TRANSLATION**: Do not mention internal manager codes (like '1', '2', or 'A') to the customer. Translate those into human actions:
               - If '1' or 'Approve' -> Confirm the full refund/cancellation.
               - If '2' or 'Discount' -> Offer the specific discount mentioned.
            3. **GAPS**: If you are still missing the customer's name, prioritize asking for it politely.
            
            Tone: Professional, empathetic, and concise. Never tell the customer about our internal "Manager Decisions" or "unclear codes"."""),
            ("human", "Triage Data: {triage}\nExtracted Data: {extraction}")
        ])
        self.chain = self.prompt | self.llm

    def write_draft(self, triage_data: dict, extraction_data: dict) -> DraftOutput:
        return self.chain.invoke({
            "triage": str(triage_data), 
            "extraction": str(extraction_data)
        })