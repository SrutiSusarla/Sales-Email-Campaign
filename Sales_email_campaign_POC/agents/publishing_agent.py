"""
Publishing Agent - Sends emails and tracks
"""

import json
from datetime import datetime
from utils.config import DATA_DIR

def send_email(email_data: dict, prospect: dict) -> dict:
    """Mock send - just logs to file"""
    
    result = {
        "prospect": prospect["company_name"],
        "to": prospect["contacts"][0]["email"],
        "subject": email_data["subject"],
        "sent_at": datetime.now().isoformat(),
        "status": "sent"
    }
    
    # Log to file
    log_file = f"{DATA_DIR}/sent_emails.json"
    try:
        with open(log_file, 'r') as f:
            logs = json.load(f)
    except:
        logs = []
    
    logs.append(result)
    
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)
    
    return result
