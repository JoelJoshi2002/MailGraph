import os
from datasets import load_dataset
from tools.file_handler import FileHandler
from tools.parser import FormParser
from state.graph import app

def run_orchestrator():
    file_manager = FileHandler()
    pdf_parser = FormParser(forms_dir=file_manager.forms_dir)
    
    print("\n" + "="*50)
    print("--- Starting Agentic Workflow Orchestrator ---")
    print("="*50)

    # 1. Get the PDF Text (The Form)
    pdf_filename = "sample_form.pdf"
    try:
        pdf_text = pdf_parser.extract_text_from_pdf(pdf_filename)
        print(f"Loaded form: {pdf_filename}")
    except FileNotFoundError:
        print(f"Error: Could not find '{pdf_filename}' in {file_manager.forms_dir}")
        return

    # 2. Get a Support Ticket (The Request)
    print("Fetching a ticket from Hugging Face...")
    dataset = load_dataset(
        "bitext/Bitext-customer-support-llm-chatbot-training-dataset", 
        split="train", 
        streaming=True
    )
    
    # We will process just the first ticket to test the full pipeline
    ticket = next(iter(dataset))
    ticket_text = ticket.get('instruction', 'No instruction found')
    print(f"Ticket received: {ticket_text}\n")

    # 3. Initialize the LangGraph State
    initial_state = {
        "ticket_text": ticket_text,
        "pdf_text": pdf_text,
        "triage_data": None,
        "extraction_data": None,
        "final_draft": None,
        "needs_human_help": False
    }

    # 4. Run the Graph
    print("Executing Agent Graph...\n")
    # This single line triggers the Triage -> Extraction -> Drafting sequence
    final_state = app.invoke(initial_state)

    # 5. Output and Save
    print("\n" + "="*50)
    print("--- Workflow Completed ---")
    print("="*50)
    print(f"Final Email Draft:\n\n{final_state['final_draft']}")
    print(f"\nMissing Info Flag: {final_state['needs_human_help']}")
    
    # Save the output
    file_manager.save_draft(
        ticket_id="FULL_WORKFLOW_TEST_1", 
        content=f"Ticket: {ticket_text}\n\nDraft:\n{final_state['final_draft']}"
    )
    print("\nDraft saved to outputs/drafts/")

if __name__ == "__main__":
    run_orchestrator()