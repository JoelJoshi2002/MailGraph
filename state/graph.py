from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from agents.triage_agent import TriageAgent
from agents.extraction_agent import ExtractionAgent
from agents.drafting_agent import DraftingAgent

class WorkflowState(TypedDict):
    ticket_text: str
    pdf_text: str
    triage_data: Optional[dict]
    extraction_data: Optional[dict]
    final_draft: Optional[str]
    needs_human_help: bool
    human_input: Optional[str] 
    approved : bool

triage_agent = TriageAgent()
extraction_agent = ExtractionAgent()
drafting_agent = DraftingAgent()

# --- Nodes ---

def run_triage(state: WorkflowState):
    print("--> Node: Triaging Ticket")
    result = triage_agent.process_ticket(state["ticket_text"])
    return {"triage_data": result.model_dump()}

def run_extraction(state: WorkflowState):
    print("--> Node: Extracting Form Data")
    result = extraction_agent.extract_data(state["pdf_text"])
    data = result.model_dump()
    
    # NEW LOGIC: Trigger human review if amount > $100 (Policy Check)
    refund_amount = data.get("total_amount", 0)
    is_high_value = refund_amount > 10.0
    
    if is_high_value:
        print(f"--- ALERT: High Value Detected (${refund_amount}) ---")
    
    return {"extraction_data": data, "needs_human_help": is_high_value}

def run_human_review(state: WorkflowState):
    amount = state['extraction_data']['total_amount']
    print("\n[!!!] POLICY LIMIT REACHED [!!!]")
    print(f"Amount: ${amount} exceeds the $10 autonomous refund limit.")
    print("Options: \n1. Type 'Approve' to override. \n2. Type a partial discount (e.g., 'Offer 20% discount instead').")
    
    manager_decision = input("Manager Decision: ")
    return {"human_input": manager_decision, "needs_human_help": False}

def run_drafting(state: WorkflowState):
    print("--> Node: Drafting Response")
    # We pass the extraction data and the manager's decision to the agent
    context = state["extraction_data"].copy()
    if state.get("human_input"):
        context["manager_decision"] = state["human_input"]
        
    result = drafting_agent.write_draft(state["triage_data"], context)
    return {"final_draft": result.email_body, "approved": False}

def run_final_review(state: WorkflowState):
    print("\n" + "-"*30)
    print("--- FINAL REVIEW ---")
    print(f"Draft to Send:\n{state['final_draft']}")
    print("-" * 30)
    
    choice = input("Approve this email? (y/n): ").lower()
    if choice == 'y':
        return {"approved": True}
    else:
        # REAL WORLD LOGIC: Ask the human for correction instructions
        print("\n[!] REJECTION DETECTED")
        feedback = input("What is wrong with this draft? (e.g., 'Stop mentioning the manager' or 'Change tone'): ")
        
        # We overwrite human_input with this feedback so the next draft is better
        return {"approved": False, "human_input": feedback}
# --- Routing Logic ---

def route_after_extraction(state: WorkflowState):
    if state["needs_human_help"]:
        return "human_review"
    return "drafting"

def route_after_review(state: WorkflowState):
    # If approved, end. If not, go back to drafting to try again.
    return "end" if state["approved"] else "drafting"

# --- Build Graph ---

workflow = StateGraph(WorkflowState)

workflow.add_node("triage", run_triage)
workflow.add_node("extraction", run_extraction)
workflow.add_node("human_review", run_human_review)
workflow.add_node("drafting", run_drafting)
workflow.add_node("final_review", run_final_review)

workflow.set_entry_point("triage")
workflow.add_edge("triage", "extraction")

workflow.add_conditional_edges(
    "extraction",
    route_after_extraction,
    {"human_review": "human_review", "drafting": "drafting"}
)

workflow.add_edge("human_review", "drafting")
workflow.add_edge("drafting", "final_review")

workflow.add_conditional_edges(
    "final_review",
    route_after_review,
    {"end": END, "drafting": "drafting"}
)

app = workflow.compile()