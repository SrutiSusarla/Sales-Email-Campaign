# Sales Email Campaign System

**Reach out to any list of companies with personalized, AI-generated emails**

---

## What is This?

An AI-powered system that helps you create and send personalized emails to any list of companies or organizations. Instead of manually researching each organization and writing individual emails, this system does it automatically using artificial intelligence.

**Example**: Upload a list of 100 companies → AI researches each one → AI writes personalized emails → You review and send.

---

## Who is This For?

- **Sales Teams** - Reach potential customers
- **Recruiters** - Contact companies for hiring partnerships
- **Event Organizers** - Invite companies to conferences or events
- **Nonprofits** - Reach out to potential sponsors or partners
- **Consultants** - Pitch services to target companies
- **Researchers** - Contact organizations for surveys or studies
- **Anyone** - Who needs to reach out to multiple companies with personalized messages

**No technical knowledge required** - Simple web interface, just upload and click.

---

## How It Works

### Simple 3-Step Process

```
1. Import Companies → 2. AI Research → 3. AI Writes Emails → 4. You Review → 5. Send
```

**Step 1: Import Companies**
- Upload a CSV file with company names
- System accepts: company name, industry, location, budget

**Step 2: AI Research**
- AI finds decision-makers (CEOs, CTOs, VPs, relevant contacts)
- AI gathers contact information (emails, phone numbers)
- AI finds recent company news and activities

**Step 3: AI Writes Emails**
- AI creates personalized email for each company
- References their recent activities
- Professional tone, clear call-to-action

**Step 4: Review & Approve**
- You review each email
- Edit if needed
- Approve or regenerate

**Step 5: Send**
- System sends approved emails
- Tracks delivery status

---

## The Dashboard

### Vertical Navigation (Left Sidebar)

**📊 Overview**
- See campaign progress at a glance
- Total companies, emails sent, success rate
- Next actions to take

**🔍 Data Enrichment**
- Upload your company list
- Start AI research
- View found contacts and company details

**✉️ Content Generation**
- Generate personalized emails
- Review and edit each email
- Approve or regenerate

**📧 Email Publishing**
- Send approved emails
- Track delivery status
- View sent emails

**❓ Help & FAQ**
- How-to guides
- Common questions
- Troubleshooting

### Key Features

✅ **Step-by-step guidance** - System tells you what to do next  
✅ **Progress tracking** - Always see how far you've come  
✅ **No data loss** - Everything saved automatically  
✅ **Pause & resume** - Stop anytime, continue later  
✅ **Error recovery** - One failure doesn't stop everything  

---

## The AI Agents

### 1. Research Agent 🔍
**What it does**: Finds information about companies

**Finds**:
- Decision-makers (names, titles, emails)
- Company information (website, description)
- Recent news (funding, product launches, partnerships)

**How**: Uses Google Gemini AI to search and analyze company data

---

### 2. Content Agent ✍️
**What it does**: Writes personalized emails

**Creates**:
- Compelling subject lines
- Personalized email body
- References recent company activities
- Professional call-to-action

**How**: Uses Google Gemini AI to generate human-like, personalized content

---

### 3. Publishing Agent 📧
**What it does**: Sends emails and tracks results

**Handles**:
- Email delivery
- Tracking sent status
- Error handling
- Delivery confirmation

**How**: Integrates with email services (AWS SES or SMTP)

---

## Tech Stack

### Frontend
- **Streamlit** - Web interface (Python-based)
- Simple, clean, no coding required to use

### Backend
- **Python** - Main programming language
- **SQLite** - Database (stores all your data)
- **Pandas** - CSV file processing

### AI/LLM
- **Google Gemini API** - AI for research and content generation
- Free tier available for testing

### Email
- **AWS SES** or **SMTP** - Email sending
- Configurable based on your needs

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key (free)
- Email service credentials (optional for testing)

### Quick Start

**1. Download the Code**
```bash
# Clone or download from repository
cd "C:\Users\sruti\Desktop\Sales email campaign\Sales_email_campaign_POC"
```

**2. Install Dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure Environment**
```bash
# Copy example environment file
copy .env.example .env

# Edit .env file with your API keys
notepad .env
```

Add your credentials:
```
GOOGLE_API_KEY=your_gemini_api_key_here
EMAIL_SENDER=your-email@example.com
```

**4. Run the Application**
```bash
streamlit run app.py
```

**5. Open in Browser**
- Automatically opens at: `http://localhost:8501`
- If not, manually open the URL shown in terminal

---

## Getting API Keys

### Google Gemini API Key (Required)
1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Paste in `.env` file

**Cost**: Free tier available (60 requests/minute)

### Email Service (Optional for Testing)
- **AWS SES**: https://aws.amazon.com/ses/
- **Gmail SMTP**: Use your Gmail account
- **Other SMTP**: Any email service with SMTP support

---

## Usage Guide

### Preparing Your CSV File

**Required Column**:
- `company_name` - Name of the company

**Optional Columns**:
- `industry` - Industry/sector (e.g., Healthcare, Technology)
- `location` - City or region (e.g., New York, California)
- `budget` - Deal size or budget (e.g., $50,000)

**Example CSV**:
```csv
company_name,industry,location,budget
Mayo Clinic,Healthcare,Rochester MN,500000
Tesla Inc,Technology,Austin TX,1000000
Walmart,Retail,Bentonville AR,750000
```

### Running Your First Campaign

1. **Start the application** - Run `streamlit run app.py`
2. **Go to Data Enrichment** - Click in sidebar
3. **Upload CSV** - Drag and drop your file
4. **Confirm Import** - Review and click "Confirm Import"
5. **Start Research** - Click "Start Research" button
6. **Wait for completion** - Progress bar shows status
7. **Go to Content Generation** - Click in sidebar
8. **Generate Emails** - Click "Generate All Emails"
9. **Review Emails** - Check each email, edit if needed
10. **Approve** - Click approve on emails you like
11. **Go to Email Publishing** - Click in sidebar
12. **Send** - Click "Send All Emails"
13. **Done!** - Emails are sent

---

## Features

### Current Features ✅
- CSV import with flexible column mapping
- AI-powered company research
- AI-generated personalized emails
- Human review and approval workflow
- Email editing before sending
- Progress tracking
- Error handling
- Data persistence (no data loss)

### Coming Soon 🚀
- Email response tracking
- A/B testing for subject lines
- Email templates library
- Scheduled sending
- Analytics dashboard
- Multi-user support

---

## Troubleshooting

### Application won't start
- Check Python version: `python --version` (need 3.8+)
- Reinstall dependencies: `pip install -r requirements.txt`

### API errors
- Check API key in `.env` file
- Verify API key is active
- Check rate limits (60 requests/minute for free tier)

### CSV upload fails
- Ensure CSV has `company_name` column
- Check file encoding (should be UTF-8)
- Remove special characters from company names

### Emails not sending
- Verify email credentials in `.env`
- Check email service is configured
- For testing, emails are saved but not actually sent

---

## Project Structure

```
Sales_email_campaign_POC/
│
├── app.py                    # Main application (start here)
├── requirements.txt          # Python dependencies
├── .env                      # Your API keys (create this)
│
├── agents/                   # AI agents
│   ├── orchestrator.py       # Workflow coordinator
│   ├── research_agent.py     # Company research
│   ├── content_agent.py      # Email generation
│   └── publishing_agent.py   # Email sending
│
├── utils/                    # Helper functions
│   ├── config.py             # Configuration
│   ├── gemini_client.py      # AI client
│   └── database.py           # Data storage
│
├── data/                     # Your data files
├── sessions/                 # Session storage
└── campaign.db               # Database (auto-created)
```

---

## Support & Documentation

### Documentation
- **Implementation Plan**: See `implementation plans_draft/` folder
- **Detailed Issues & Solutions**: `Issues_Raised_and_Mitigation.md`
- **Agent Functionality**: `Agent_complete_functionality.md`

### Getting Help
- Check the **Help** section in the application
- Review **FAQ** for common questions
- Check troubleshooting section above

---

## Important Notes

⚠️ **This is a Proof of Concept (POC)**
- Suitable for testing and small campaigns
- For production use, additional features needed:
  - Enhanced error handling
  - Rate limiting
  - Comprehensive logging
  - Security hardening
  - Scalability improvements

⚠️ **API Costs**
- Google Gemini: Free tier available
- Monitor usage to avoid unexpected charges
- Each company research = 1 API call
- Each email generation = 1 API call

⚠️ **Email Compliance**
- Ensure you have permission to email recipients
- Follow CAN-SPAM Act and GDPR regulations
- Include unsubscribe links (add manually for now)
- Use legitimate business email addresses

---

## License & Credits

**Project**: B2B Sales Email Campaign System  
**Purpose**: Proof of Concept for AI-powered email outreach automation  
**Status**: Active Development  

**Technologies Used**:
- Streamlit (UI framework)
- Google Gemini (AI/LLM)
- Python (Backend)
- SQLite (Database)

---

## Quick Reference

### Start Application
```bash
streamlit run app.py
```

### Stop Application
- Press `Ctrl + C` in terminal
- Or close terminal window

### Reset Database
```bash
# Delete database file to start fresh
del campaign.db
```

### Update Dependencies
```bash
pip install -r requirements.txt --upgrade
```

---

**Ready to reach out to your target companies? Start the application and upload your first company list!** 🚀
