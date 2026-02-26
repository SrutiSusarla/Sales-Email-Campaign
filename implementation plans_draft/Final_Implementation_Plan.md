# Sales Email Campaign System - Final Implementation Plan

**Version:** 3.0  
**Date:** February 27, 2026  
**Status:** Ready to Implement  
**Tech Stack:** 100% Free & Open Source

---

## Executive Summary

### What We're Building
B2B sales email campaign automation using AI agents that research companies, generate personalized emails, get human approval, send emails, and track leads through the entire sales funnel.

### Key Decisions Made
- ✅ **Frontend:** React + Vite (not Streamlit)
- ✅ **Backend:** FastAPI + Python
- ✅ **Database:** PostgreSQL (not DynamoDB)
- ✅ **LLM:** Ollama with Llama 3.1 (not Gemini)
- ✅ **Agents:** LangGraph (not custom)
- ✅ **Email:** Gmail SMTP (500/day free)
- ✅ **Hosting:** Docker local, Render production
- ✅ **Cost:** $0/month

---

## Final Architecture

```
┌─────────────────────────────────────────────┐
│   React + Vite Frontend (Vercel Free)       │
│   • Dashboard                               │
│   • Data Enrichment                         │
│   • Content Generation                      │
│   • Email Publishing                        │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│      FastAPI Backend (Render Free)          │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │   LangGraph Multi-Agent System      │   │
│  │                                     │   │
│  │  Research → Content → Approval →   │   │
│  │           Publishing                │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌──────────────┐        ┌──────────────┐
│  PostgreSQL  │        │   Ollama     │
│  (Render)    │        │  (Docker)    │
│              │        │              │
│ • Prospects  │        │ • Llama 3.1  │
│ • Enriched   │        │ • Unlimited  │
│ • Emails     │        │ • Local      │
│ • Analytics  │        │              │
└──────────────┘        └──────────────┘
```

---

## Tech Stack (100% Free)

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **Agent Framework:** LangGraph
- **Database:** PostgreSQL
- **Cache:** Redis
- **LLM:** Ollama (Llama 3.1)
- **Email:** Gmail SMTP

### Frontend
- **Framework:** React 18 + Vite
- **State:** Zustand + TanStack Query
- **Routing:** React Router
- **HTTP:** Axios

### Infrastructure
- **Local Dev:** Docker Compose
- **Production Backend:** Render (free tier)
- **Production Frontend:** Vercel (free tier)
- **Production DB:** Render PostgreSQL (free tier)

### Data Enrichment (Fallback Chain)
1. Hunter.io (free: 25/month)
2. Email pattern guessing (unlimited)
3. Web scraping (unlimited)
4. Ollama research (unlimited)

---

## Database Schema (PostgreSQL)

```sql
-- Prospects
CREATE TABLE prospects (
    id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    industry TEXT,
    location TEXT,
    budget NUMERIC,
    status TEXT DEFAULT 'uploaded',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Enriched Data
CREATE TABLE enriched_data (
    id SERIAL PRIMARY KEY,
    prospect_id INTEGER REFERENCES prospects(id) ON DELETE CASCADE,
    contacts JSONB,              -- [{name, title, email, phone}]
    company_info JSONB,          -- {website, description, employees}
    recent_news JSONB,           -- [news items]
    quality_score INTEGER,
    enrichment_cost NUMERIC(10,4),
    error TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Emails
CREATE TABLE emails (
    id SERIAL PRIMARY KEY,
    prospect_id INTEGER REFERENCES prospects(id) ON DELETE CASCADE,
    subject TEXT,
    body TEXT,
    word_count INTEGER,
    status TEXT DEFAULT 'draft',  -- draft, approved, sent
    quality_score INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Email Sends
CREATE TABLE email_sends (
    id SERIAL PRIMARY KEY,
    email_id INTEGER REFERENCES emails(id) ON DELETE CASCADE,
    sent_at TIMESTAMP DEFAULT NOW(),
    status TEXT,                  -- sent, failed, bounced, opened, clicked
    tracking_id UUID DEFAULT gen_random_uuid(),
    error TEXT
);

-- Compliance: Consent tracking
CREATE TABLE consent_log (
    id SERIAL PRIMARY KEY,
    prospect_id INTEGER REFERENCES prospects(id),
    email TEXT,
    consent_type TEXT,            -- explicit, legitimate_interest
    consent_date TIMESTAMP DEFAULT NOW(),
    ip_address INET,
    proof TEXT
);

-- Compliance: Unsubscribes
CREATE TABLE unsubscribes (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE,
    unsubscribed_at TIMESTAMP DEFAULT NOW(),
    reason TEXT
);

-- Audit Log
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    user_id TEXT,
    action TEXT,                  -- approved, sent, deleted, exported
    prospect_id INTEGER,
    timestamp TIMESTAMP DEFAULT NOW(),
    ip_address INET,
    details JSONB
);

-- Indexes
CREATE INDEX idx_prospects_status ON prospects(status);
CREATE INDEX idx_emails_status ON emails(status);
CREATE INDEX idx_email_sends_tracking ON email_sends(tracking_id);
CREATE INDEX idx_unsubscribes_email ON unsubscribes(email);
```

---

## Multi-Agent System (LangGraph)

### Agent Workflow

```
┌─────────────────────────────────────────────┐
│         ORCHESTRATOR (LangGraph)            │
└─────────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Research │→ │ Content  │→ │Publishing│
│  Agent   │  │  Agent   │  │  Agent   │
└──────────┘  └──────────┘  └──────────┘
                    │
            [Human Approval]
```

### State Definition

```python
class CampaignState(TypedDict):
    # Input
    prospect_id: int
    company_name: str
    industry: str
    location: str
    budget: float
    
    # Research Agent outputs
    enriched_data: dict
    contacts: list
    recent_news: list
    enrichment_quality: int
    
    # Content Agent outputs
    email_subject: str
    email_body: str
    email_quality: int
    
    # Human approval
    approval_status: str  # "pending", "approved", "rejected"
    
    # Publishing Agent outputs
    sent_status: str
    tracking_id: str
    
    # Error handling
    errors: list
    retry_count: int
```

### Agent Responsibilities

**1. Research Agent**
- Find contacts (Hunter.io → Pattern → Scraping)
- Get company info (Website scraping)
- Get recent news (Ollama research)
- Calculate quality score
- Save to database

**2. Content Agent**
- Build email prompt
- Generate email with Ollama
- Parse subject and body
- Validate quality (word count, personalization, CTA)
- Save to database

**3. Publishing Agent**
- Get contact email
- Send via Gmail SMTP
- Track delivery
- Handle bounces
- Save send status

**4. Orchestrator (LangGraph)**
- Route between agents
- Manage state persistence
- Pause for human approval
- Handle errors and retries
- Resume workflows

---

## Data Enrichment Strategy (Fallback Chain)

```python
def enrich_prospect(prospect):
    """Try multiple sources with fallback"""
    
    # Email finding (fallback chain)
    email = (
        try_hunter_io(prospect) or           # Free: 25/month
        try_email_pattern(prospect) or       # Free: unlimited
        try_web_scrape(prospect) or          # Free: unlimited
        None
    )
    
    # Company data (fallback chain)
    company_info = (
        try_web_scrape(prospect.website) or  # Free: unlimited
        try_linkedin_scrape(prospect) or     # Free: unlimited
        {}
    )
    
    # News/research (fallback chain)
    news = (
        try_ollama_research(prospect) or     # Free: unlimited
        try_web_search(prospect) or          # Free: unlimited
        []
    )
    
    return {
        'email': email,
        'company_info': company_info,
        'news': news
    }
```

---

## Docker Compose Setup

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:16-alpine
    container_name: campaign_db
    environment:
      POSTGRES_DB: campaign_db
      POSTGRES_USER: campaign_user
      POSTGRES_PASSWORD: campaign_pass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U campaign_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: campaign_redis
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Ollama (LLM)
  ollama:
    image: ollama/ollama:latest
    container_name: campaign_ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    entrypoint: ["/bin/sh", "-c"]
    command:
      - |
        ollama serve &
        sleep 5
        ollama pull llama3.1
        wait

  # FastAPI Backend
  backend:
    build: ./backend
    container_name: campaign_backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://campaign_user:campaign_pass@postgres:5432/campaign_db
      REDIS_URL: redis://redis:6379
      OLLAMA_URL: http://ollama:11434
      GMAIL_USER: ${GMAIL_USER}
      GMAIL_APP_PASSWORD: ${GMAIL_APP_PASSWORD}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      ollama:
        condition: service_started
    volumes:
      - ./backend:/app
      - ./campaign_checkpoints.db:/app/campaign_checkpoints.db
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # React Frontend
  frontend:
    build: ./frontend
    container_name: campaign_frontend
    ports:
      - "5173:5173"
    environment:
      VITE_API_URL: http://localhost:8000
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev -- --host

volumes:
  postgres_data:
  ollama_data:
```

---

## Project Structure

```
sales-email-campaign/
│
├── docker-compose.yml
├── .env
├── .gitignore
├── README.md
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py                    # FastAPI app
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── graph.py               # LangGraph workflow
│   │   │   ├── research_agent.py      # Research agent
│   │   │   ├── content_agent.py       # Content agent
│   │   │   └── publishing_agent.py    # Publishing agent
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── prospects.py           # Prospect endpoints
│   │   │   ├── campaigns.py           # Campaign endpoints
│   │   │   └── analytics.py           # Analytics endpoints
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── ollama_service.py      # Ollama integration
│   │   │   ├── email_service.py       # Gmail SMTP
│   │   │   └── enrichment_service.py  # Data enrichment
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py             # Pydantic models
│   │   └── core/
│   │       ├── __init__.py
│   │       ├── config.py              # Configuration
│   │       ├── database.py            # SQLAlchemy models
│   │       └── db_utils.py            # Database utilities
│   └── campaign_checkpoints.db        # LangGraph checkpoints
│
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── pages/
        │   ├── Dashboard.jsx          # Overview dashboard
        │   ├── Enrichment.jsx         # Data enrichment
        │   ├── Content.jsx            # Content generation
        │   └── Publishing.jsx         # Email publishing
        ├── components/
        │   ├── Sidebar.jsx            # Navigation
        │   ├── EmailPreview.jsx       # Email preview
        │   └── ProspectCard.jsx       # Prospect card
        ├── api/
        │   └── client.js              # Axios client
        └── stores/
            └── campaignStore.js       # Zustand store
```

---

## Implementation Timeline (14 Days)

### **Phase 0: Setup (Day 1)**
**Duration:** 4 hours  
**Priority:** CRITICAL

**Tasks:**
- [ ] Create project structure
- [ ] Setup Docker Compose
- [ ] Create .env file
- [ ] Start services (postgres, ollama, redis)
- [ ] Install backend dependencies
- [ ] Install frontend dependencies
- [ ] Test Ollama is working

**Deliverables:**
- All services running
- Ollama model downloaded
- Dependencies installed

---

### **Phase 1: Database Layer (Days 2-3)**
**Duration:** 2 days  
**Priority:** CRITICAL

**Day 2 Morning:**
- [ ] Create database schema (SQLAlchemy models)
- [ ] Create tables in PostgreSQL
- [ ] Test database connection

**Day 2 Afternoon:**
- [ ] Create database utilities (CRUD operations)
- [ ] Test add_prospect()
- [ ] Test save_enriched_data()
- [ ] Test save_email()

**Day 3:**
- [ ] Add indexes for performance
- [ ] Add compliance tables (consent, unsubscribes, audit)
- [ ] Test all database operations
- [ ] Write database documentation

**Deliverables:**
- Working database with all tables
- CRUD utilities tested
- 100% data persistence

---

### **Phase 2: Core Services (Days 3-4)**
**Duration:** 1.5 days  
**Priority:** HIGH

**Day 3 Afternoon:**
- [ ] Create Ollama service
- [ ] Test email generation
- [ ] Test company research

**Day 4 Morning:**
- [ ] Create Email service (Gmail SMTP)
- [ ] Test sending email to yourself
- [ ] Add tracking pixel logic

**Day 4 Afternoon:**
- [ ] Create enrichment service
- [ ] Implement Hunter.io integration
- [ ] Implement email pattern guessing
- [ ] Implement web scraping

**Deliverables:**
- Ollama generating emails
- Gmail SMTP sending emails
- Enrichment fallback chain working

---

### **Phase 3: AI Agents (Days 4-5)**
**Duration:** 1.5 days  
**Priority:** HIGH

**Day 4 Evening:**
- [ ] Create Research Agent
- [ ] Implement enrichment logic
- [ ] Test with 1 prospect

**Day 5 Morning:**
- [ ] Create Content Agent
- [ ] Implement email generation
- [ ] Implement quality validation
- [ ] Test with 1 prospect

**Day 5 Afternoon:**
- [ ] Create Publishing Agent
- [ ] Implement email sending
- [ ] Implement tracking
- [ ] Test with 1 prospect

**Deliverables:**
- 3 agents working independently
- Each agent tested
- Database integration working

---

### **Phase 4: LangGraph Integration (Days 6-7)**
**Duration:** 2 days  
**Priority:** HIGH

**Day 6:**
- [ ] Install LangGraph
- [ ] Define CampaignState
- [ ] Create workflow graph
- [ ] Add nodes (research, content, approval, publish)
- [ ] Add edges and routing
- [ ] Test basic workflow

**Day 7:**
- [ ] Add checkpointing (SQLite)
- [ ] Implement human approval pause
- [ ] Implement approve/reject endpoints
- [ ] Test pause/resume workflow
- [ ] Test error recovery

**Deliverables:**
- Complete workflow working
- Human approval working
- Checkpointing working
- Can resume from any point

---

### **Phase 5: API Layer (Days 7-8)**
**Duration:** 1.5 days  
**Priority:** HIGH

**Day 7 Afternoon:**
- [ ] Create FastAPI app
- [ ] Add CORS middleware
- [ ] Create health check endpoint

**Day 8:**
- [ ] Create prospect endpoints (upload, list, get)
- [ ] Create campaign endpoints (start, approve, reject)
- [ ] Create analytics endpoints
- [ ] Test all endpoints with Postman
- [ ] Write API documentation

**Deliverables:**
- FastAPI running
- All endpoints working
- API docs at /docs

---

### **Phase 6: Frontend (Days 9-11)**
**Duration:** 3 days  
**Priority:** MEDIUM

**Day 9:**
- [ ] Setup React + Vite
- [ ] Create routing
- [ ] Create Sidebar component
- [ ] Create basic layout

**Day 10:**
- [ ] Create Dashboard page (overview)
- [ ] Create Enrichment page (CSV upload)
- [ ] Create Content page (email review)
- [ ] Create Publishing page (send emails)

**Day 11:**
- [ ] Connect to API (Axios)
- [ ] Add state management (Zustand)
- [ ] Add loading states
- [ ] Add error handling
- [ ] Style with CSS

**Deliverables:**
- Working React app
- All pages functional
- Connected to backend
- Basic styling

---

### **Phase 7: Testing & Polish (Days 12-14)**
**Duration:** 3 days  
**Priority:** MEDIUM

**Day 12: End-to-End Testing**
- [ ] Upload CSV with 5 test companies
- [ ] Run enrichment on all
- [ ] Generate emails for all
- [ ] Approve 3, reject 2
- [ ] Send approved emails
- [ ] Verify emails received
- [ ] Check database state

**Day 13: Error Handling**
- [ ] Add try-catch blocks everywhere
- [ ] Add error messages in UI
- [ ] Add retry logic for failed operations
- [ ] Test failure scenarios
- [ ] Add logging

**Day 14: Documentation & Deployment**
- [ ] Write README.md
- [ ] Write setup instructions
- [ ] Document API endpoints
- [ ] Document database schema
- [ ] Create .env.example
- [ ] Test deployment on Render
- [ ] Test deployment on Vercel

**Deliverables:**
- Fully tested system
- Complete documentation
- Ready for production

---

## Quick Start Commands

### **Day 1: Setup**

```bash
# 1. Create project
mkdir sales-email-campaign
cd sales-email-campaign

# 2. Create structure
mkdir -p backend/app/{agents,api,services,models,core}
mkdir -p frontend/src/{pages,components,api,stores}

# 3. Create .env
cat > .env << 'EOF'
DATABASE_URL=postgresql://campaign_user:campaign_pass@localhost:5432/campaign_db
OLLAMA_URL=http://localhost:11434
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
HUNTER_API_KEY=your-hunter-key
REDIS_URL=redis://localhost:6379
EOF

# 4. Create docker-compose.yml (copy from above)

# 5. Start services
docker-compose up -d

# 6. Check Ollama is downloading model
docker-compose logs -f ollama

# 7. Test Ollama
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.1",
  "prompt": "Hello"
}'
```

### **Day 2: Database**

```bash
# 1. Create requirements.txt
cat > backend/requirements.txt << 'EOF'
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
redis==5.0.1
ollama==0.1.6
langgraph==0.0.20
langchain-community==0.0.20
beautifulsoup4==4.12.3
requests==2.31.0
pydantic==2.5.3
python-multipart==0.0.6
python-dotenv==1.0.0
EOF

# 2. Install dependencies
cd backend
pip install -r requirements.txt

# 3. Create database models (see database.py above)

# 4. Create tables
python -c "from app.core.database import Base, engine; Base.metadata.create_all(engine)"

# 5. Test database
python -c "from app.core.db_utils import DatabaseService; db = DatabaseService(); print(db.add_prospect('Test', 'Tech', 'NYC', 50000))"
```

---

## Success Metrics

### Technical Metrics
- **Data Persistence:** 100% (no data loss)
- **Agent Independence:** 100% (can run separately)
- **Error Recovery:** 95% success rate
- **API Response Time:** <2 seconds
- **Email Delivery Rate:** >95%

### User Experience Metrics
- **Task Completion Time:** <5 minutes per campaign
- **User Errors:** <5% error rate
- **Onboarding Time:** <10 minutes
- **User Satisfaction:** 8/10 target

### Campaign Performance
- **Open Rate:** >27% (industry avg: 15-25%)
- **Click Rate:** >3% (industry avg: 2-5%)
- **Response Rate:** >2.5% (industry avg: 0.5-2%)
- **Cost per Lead:** <$2

---

## Cost Breakdown

### Development (Local)
- PostgreSQL: **$0**
- Redis: **$0**
- Ollama: **$0**
- React + Vite: **$0**
- **Total: $0/month**

### Production (Free Tier)
- Backend (Render): **$0**
- Frontend (Vercel): **$0**
- Database (Render): **$0**
- Ollama (local): **$0**
- Gmail SMTP: **$0** (500/day)
- **Total: $0/month**

### Production (Self-Hosted)
- Hetzner VPS: **$4.50/month**
- Domain: **$1/month**
- Everything else: **$0**
- **Total: $5.50/month**

---

## Compliance Checklist

### Must-Have Before Launch
- [ ] Unsubscribe link in every email
- [ ] Physical address in footer
- [ ] Consent tracking database
- [ ] Opt-out management system
- [ ] SPF/DKIM/DMARC setup
- [ ] Bounce/complaint handling
- [ ] Rate limiting (start 20/day)
- [ ] Audit logging
- [ ] Data retention policy
- [ ] GDPR data export/delete functions
- [ ] Suppression list management
- [ ] Email validation before send

---

## Risk Mitigation

### Critical Risks

**1. Ollama Performance**
- **Risk:** Slow on CPU
- **Mitigation:** Use GPU or switch to Groq API (free)
- **Fallback:** Use Gemini free tier

**2. Email Deliverability**
- **Risk:** Emails going to spam
- **Mitigation:** SPF/DKIM/DMARC, warm-up, content optimization
- **Fallback:** Multiple sending domains

**3. Data Loss**
- **Risk:** Losing enriched data
- **Mitigation:** PostgreSQL persistence, immediate saves
- **Fallback:** Backup and recovery procedures

**4. Rate Limits**
- **Risk:** Gmail 500/day limit
- **Mitigation:** Track daily count, queue excess
- **Fallback:** Use Mailgun (5,000/month free)

---

## Next Immediate Actions

### Today (Right Now)
1. Create project structure
2. Setup Docker Compose
3. Start all services
4. Verify Ollama is working

### Tomorrow (Day 2)
1. Create database schema
2. Test database connection
3. Create CRUD utilities
4. Test all database operations

### Day 3
1. Create Ollama service
2. Create Email service
3. Test both services

### Days 4-5
1. Build all 3 agents
2. Test each independently
3. Integrate with database

---

## Support & Resources

### Documentation
- LangGraph: https://langchain-ai.github.io/langgraph/
- Ollama: https://ollama.ai/
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/

### Community
- LangChain Discord
- Ollama GitHub Issues
- FastAPI Discord

---

## Conclusion

This implementation plan provides a complete roadmap to build a production-ready B2B sales email campaign automation system using 100% free and open source technologies.

**Key Highlights:**
- ✅ Multi-agent AI system with LangGraph
- ✅ Unlimited email generation with Ollama
- ✅ Smart fallback chain for data enrichment
- ✅ Human-in-the-loop approval workflow
- ✅ Complete data persistence with PostgreSQL
- ✅ Free hosting on Render + Vercel
- ✅ Total cost: $0/month

**Timeline:** 14 days to working POC

**Start Date:** February 27, 2026  
**Target Completion:** March 12, 2026

---

**Document Version:** 3.0  
**Last Updated:** February 27, 2026  
**Status:** Ready to Implement
