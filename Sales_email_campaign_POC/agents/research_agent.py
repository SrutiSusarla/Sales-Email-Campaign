"""
Research Agent - Enriches prospect data using LLM
"""

from utils.gemini_client import GeminiClient
from utils.config import GOOGLE_API_KEY

def enrich_prospect(prospect: dict) -> dict:
    """
    Enriches prospect with company info, contacts, news using LLM
    """
    
    company_name = prospect.get("company_name", "Unknown")
    industry = prospect.get("industry", "Unknown")
    location = prospect.get("location", "Unknown")
    
    print(f"[RESEARCH] Starting research for: {company_name}")
    print(f"[RESEARCH] Industry: {industry}, Location: {location}")
    
    # Optimized prompt for Gemini to find real contacts
    prompt = f"""You are a B2B research assistant. Research this company and find real, actionable contact information.

Company: {company_name}
Industry: {industry}
Location: {location}

Find and provide:

1. DECISION MAKERS (3-5 key contacts):
   - Full name
   - Exact job title (CEO, CTO, VP Sales, etc.)
   - Email address (use common patterns: firstname.lastname@company.com)
   - Phone number if available

2. COMPANY INFORMATION:
   - Brief description (what they do)
   - Company website

3. RECENT NEWS (2-3 items from last 6 months):
   - Funding, product launches, partnerships

Return ONLY valid JSON in this exact format:
{{
  "contacts": [
    {{"name": "John Smith", "title": "CEO", "email": "john.smith@company.com", "linkedin": "https://linkedin.com/in/johnsmith", "phone": "+1-555-0100"}}
  ],
  "company_info": {{
    "description": "Brief description here",
    "website": "https://company.com",
    "linkedin": "https://linkedin.com/company/companyname"
  }},
  "recent_news": [
    "Recent activity here"
  ]
}}

IMPORTANT: If any information is not found, use "Not Available" instead of leaving it empty."""
    
    try:
        print(f"[RESEARCH] Calling Gemini API...")
        client = GeminiClient(GOOGLE_API_KEY)
        response = client.generate_email(prompt)
        print(f"[RESEARCH] Received response from Gemini")
        
        # Parse JSON response
        import json
        
        # Clean response
        response = response.strip()
        if response.startswith("```json"):
            response = response.replace("```json", "").replace("```", "").strip()
        elif response.startswith("```"):
            response = response.replace("```", "").strip()
        
        print(f"[RESEARCH] Parsing JSON response...")
        enriched = json.loads(response)
        print(f"[RESEARCH] Found {len(enriched.get('contacts', []))} contacts")
        
        return {
            "company_name": company_name,
            "industry": industry,
            "location": location,
            "contacts": enriched.get("contacts", []),
            "company_info": enriched.get("company_info", {}),
            "recent_news": enriched.get("recent_news", []),
            "quality_score": len(enriched.get("contacts", [])) * 20
        }
    
    except Exception as e:
        print(f"[RESEARCH] Error: {str(e)}")
        # Fallback with minimal data
        return {
            "company_name": company_name,
            "industry": industry,
            "location": location,
            "contacts": [],
            "company_info": {
                "description": f"{company_name} operates in {industry}",
                "website": ""
            },
            "recent_news": [],
            "quality_score": 0,
            "error": str(e)
        }
