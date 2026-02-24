"""
Content Agent - Generates personalized emails
"""

from utils.gemini_client import GeminiClient
from utils.config import EMAIL_TARGET_WORD_COUNT, GOOGLE_API_KEY

def generate_email(enriched_data: dict) -> dict:
    """Generate email using Gemini"""
    
    company_name = enriched_data.get('company_name', 'Company')
    industry = enriched_data.get('industry', 'Business')
    
    print(f"[CONTENT] Generating email for: {company_name}")
    
    # Get first contact or use generic
    contacts = enriched_data.get('contacts', [])
    if contacts:
        contact_name = contacts[0].get('name', 'Decision Maker')
        contact_title = contacts[0].get('title', 'Executive')
        print(f"[CONTENT] Target contact: {contact_name}, {contact_title}")
    else:
        contact_name = 'Decision Maker'
        contact_title = 'Executive'
        print(f"[CONTENT] No contacts found, using generic")
    
    # Get recent news or use generic
    recent_news = enriched_data.get('recent_news', [])
    news_item = recent_news[0] if recent_news else f"{company_name} is active in {industry}"
    
    prompt = f"""Generate a B2B sales email:

Company: {company_name}
Industry: {industry}
Contact: {contact_name}, {contact_title}
Recent: {news_item}

Requirements:
- 100-150 words
- Professional tone
- Reference their recent activity
- Clear call-to-action
- Subject line (3 words max, lowercase)

Format:
Subject: [subject]
Body: [email body]
"""
    
    try:
        print(f"[CONTENT] Calling Gemini API for email generation...")
        client = GeminiClient(GOOGLE_API_KEY)
        response = client.generate_email(prompt)
        print(f"[CONTENT] Email generated successfully")
        
        # Parse response
        lines = response.split('\n')
        subject = lines[0].replace('Subject:', '').strip()
        body = '\n'.join(lines[1:]).strip()
        
        return {
            "subject": subject,
            "body": body,
            "word_count": len(body.split())
        }
    except Exception as e:
        print(f"[CONTENT] Error: {str(e)}")
        # Fallback email
        return {
            "subject": f"{company_name.lower()} partnership",
            "body": f"Hi {contact_name},\n\nI noticed {company_name}'s work in {industry}. Would love to discuss potential collaboration.\n\nBest regards",
            "word_count": 20,
            "error": str(e)
        }
