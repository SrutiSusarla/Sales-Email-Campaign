"""
Orchestrator - Simple workflow coordinator
"""

from agents.research_agent import enrich_prospect
from agents.content_agent import generate_email
from agents.publishing_agent import send_email
import json
import os

SESSION_DIR = "sessions"
os.makedirs(SESSION_DIR, exist_ok=True)

def save_session(prospect_id: str, data: dict):
    """Save session state to file"""
    with open(f"{SESSION_DIR}/{prospect_id}.json", 'w') as f:
        json.dump(data, f, indent=2)

def load_session(prospect_id: str):
    """Load session state from file"""
    try:
        with open(f"{SESSION_DIR}/{prospect_id}.json", 'r') as f:
            return json.load(f)
    except:
        return None

def run_campaign(prospect_id: str, prospect: dict, approved: bool = False):
    """
    Run campaign workflow with state persistence
    
    Args:
        prospect_id: Unique ID for session
        prospect: Prospect data
        approved: If True, send email
    
    Returns:
        Campaign result
    """
    
    # Try to load existing session
    session = load_session(prospect_id)
    
    if session and approved:
        # Resume: Send email
        result = send_email(session['email'], session['enriched_data'])
        session['status'] = 'sent'
        session['result'] = result
        save_session(prospect_id, session)
        return session
    
    # First run: Enrich and generate
    enriched = enrich_prospect(prospect)
    email = generate_email(enriched)
    
    session = {
        "status": "pending_approval",
        "enriched_data": enriched,
        "email": email
    }
    
    save_session(prospect_id, session)
    return session
