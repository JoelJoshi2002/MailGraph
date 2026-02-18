from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class FormExtraction(BaseModel):
    customer_name: str = Field(description="The full name of the customer. Output 'Unknown' if not found.")
    document_date: str = Field(description="The date on the document. Output 'Unknown' if not found.")
    total_amount: float = Field(description="The total numerical value/invoice amount. Use 0.00 if not found.")
    form_type: str = Field(description="Type of form (e.g., Invoice, Receipt).")

class ExtractionAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile", 
            temperature=0
        ).with_structured_output(FormExtraction)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert data entry assistant. Extract the exact requested fields. Convert currency strings to raw floats."),
            ("human", "{pdf_text}")
        ])
        
        self.chain = self.prompt | self.llm

    def extract_data(self, pdf_text: str) -> FormExtraction:
        return self.chain.invoke({"pdf_text": pdf_text})