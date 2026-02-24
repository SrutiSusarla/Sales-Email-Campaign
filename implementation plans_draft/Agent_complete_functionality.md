# AI Agents for B2B Email Campaign System
**Complete Functionality Guide**

---

## Project Overview

**Goal:** Automate B2B sales outreach using AI agents that research companies, generate personalized emails, manage sending, and track responses.

**Core Workflow:**
```
Raw Data → AI Research → AI Email Generation → Human Approval → AI Publishing → AI Response Management
```

---

## Why AI Agents (Not Just APIs)?

**Traditional Service:**
```python
# Fixed logic - no intelligence
def enrich(company):
    email = hunter_io.find(company)  # Always calls
    data = clearbit.get(company)     # Always calls
    return {**email, **data}         # Wastes money
```

**Agent Approach:**
```python
# Agent decides intelligently
async def enrich(company):
    # Agent analyzes what's needed
    plan = await agent.create_plan(company)
    
    # Agent executes optimally
    result = await agent.execute(plan)
    
    # Agent validates quality
    if agent.quality_check(result) < 70:
        result = await agent.try_alternative()
    
    return result  # Saves costs, better quality
```

---

## The 4 AI Agents

```
┌─────────────────────────────────────────┐
│      ORCHESTRATOR AGENT                 │
│  (Coordinates workflow, manages state)  │
└─────────────────────────────────────────┘
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│ AGENT 1 │ │ AGENT 2 │ │ AGENT 3 │
│Research │→│ Content │→│Publishing│
│& Enrich │ │Generator│ │&Response│
└─────────┘ └─────────┘ └─────────┘
```

---

## Agent 1: Research & Enrichment Agent

### Purpose
Takes raw company data and intelligently enriches it with contacts, company info, and recent news.

### What It Does

**1. Analyzes Input**
```
Input: "Mayo Clinic, Rochester MN, $500K budget"

Agent thinks:
- Healthcare organization
- Need IT/Operations decision-makers
- Large budget = target C-level
- Healthcare = HIPAA-compliant messaging needed
```

**2. Creates Strategy**
```
Agent's Plan:
1. Search LinkedIn for CIO/VP Operations
2. Use Hunter.io for email patterns
3. Use Perplexity for recent news
4. Skip Clearbit (has website, save money)
5. Validate: Need 2+ contacts with emails
```

**3. Executes Intelligently**
```python
async def enrich(prospect):
    # Assess completeness
    if prospect.has_website:
        tools = ["website_scraper", "hunter_io"]  # Skip expensive Clearbit
    else:
        tools = ["clearbit", "hunter_io", "linkedin"]
    
    # Execute in optimal order
    results = {}
    for tool in tools:
        result = await use_tool(tool, prospect)
        
        if is_sufficient(results):
            break  # Stop early, save costs
        
        results.update(result)
    
    # Validate quality
    if quality_score(results) < 70:
        results = await try_alternative_sources()
    
    return results
```

**4. Handles Failures**
```
Hunter.io fails → Try Apollo.io
Apollo.io fails → Check LinkedIn
No email found → Use pattern guesser (firstname.lastname@company.com)
Validate with MX record check
```

### Tools Used

| Tool | Purpose | When Used |
|------|---------|-----------|
| Hunter.io | Find emails | Always (cheap, fast) |
| Clearbit | Company data | Only if no website |
| Apollo.io | Backup email finder | If Hunter.io fails |
| LinkedIn API | Find decision-makers | For contacts |
| Perplexity API | Recent news | Always (personalization) |
| Website Scraper | Extract company info | If website exists |
| Email Validator | Verify email (MX check) | Always |

### Decision Tree

```
Mayo Clinic
  │
  ├─ Has website? YES → Scrape (free) → Skip Clearbit
  │
  ├─ Find emails
  │   ├─ Hunter.io → Success ✓
  │   └─ Failed? → Apollo.io → Pattern guesser
  │
  ├─ Find contacts
  │   └─ LinkedIn: "Mayo Clinic CIO" → Found 3 people
  │
  ├─ Get news
  │   └─ Perplexity: "Mayo Clinic 2026" → "Launched AI diagnostics"
  │
  └─ Validate
      ├─ 2+ contacts? YES
      ├─ Valid emails? YES
      ├─ Recent news? YES
      └─ Quality: 92% ✓
```

### Output Example

```json
{
  "company_name": "Mayo Clinic",
  "industry": "Healthcare",
  "contacts": [
    {
      "name": "John Smith",
      "title": "CIO",
      "email": "john.smith@mayoclinic.org",
      "confidence": 95
    }
  ],
  "recent_news": [
    "Launched AI diagnostics program (Jan 2026)",
    "Expanded telemedicine services"
  ],
  "enrichment_quality_score": 92,
  "cost": "$1.20"
}
```

---

## Agent 2: Content Generation Agent

### Purpose
Generates personalized, high-quality emails matching prospect's industry, pain points, and recent activities.

### What It Does

**1. Analyzes Context**
```
Mayo Clinic enriched data

Agent analyzes:
- Industry: Healthcare → Empathetic, professional tone
- Recent news: "AI diagnostics" → Mention AI/innovation
- Title: CIO → Focus on technical efficiency, ROI
- Size: 70K employees → Enterprise solutions
- Budget: $500K → Premium offering
```

**2. Selects Case Study**
```python
async def select_case_study(prospect, company_profile):
    scores = []
    for case_study in company_profile.case_studies:
        score = 0
        
        if case_study.industry == prospect.industry:
            score += 50  # Industry match
        
        if case_study.company_size == prospect.size:
            score += 20  # Size match
        
        if case_study.pain_points in prospect.recent_news:
            score += 30  # Pain point match
        
        scores.append((case_study, score))
    
    return max(scores, key=lambda x: x[1])[0]
```

**Agent selects:**
```
Available:
1. "Hospital reduces wait times 40%" (Healthcare, 50K) → Score: 100 ✓
2. "Tech company scales" (Technology, 500) → Score: 20
3. "Retail improves inventory" (Retail, 10K) → Score: 10

Selected: #1 (perfect match)
```

**3. Generates Email**
```python
async def generate_email(prospect, case_study):
    prompt = f"""
    Generate B2B email:
    
    PROSPECT:
    - Company: {prospect.company_name}
    - Contact: {prospect.contact.name}, {prospect.contact.title}
    - Recent: {prospect.recent_news[0]}
    
    PERSONALIZATION:
    - Reference their AI diagnostics launch
    - CIO = cares about technical efficiency, ROI
    - Healthcare = empathetic tone, patient outcomes
    
    OUR COMPANY:
    - Case study: Hospital reduced wait times 40%
    
    REQUIREMENTS:
    - Subject: 4-7 words, lowercase, mention AI
    - Preheader: 40 chars
    - Body: 100-150 words
    - CTA: "15-minute call?"
    - Tone: Professional, empathetic
    """
    
    email = await bedrock.generate(prompt)
    
    if validate(email).score < 80:
        email = await regenerate_with_feedback(email)
    
    return email
```

**4. Validates Quality**
```python
def validate(email):
    score = 100
    issues = []
    
    # Word count (target 144)
    if word_count not in range(100, 200):
        score -= 15
    
    # Personalization
    if company_name not in email.body:
        score -= 20
    
    if recent_news not in email.body:
        score -= 15
    
    # Subject line
    if len(email.subject.split()) > 7:
        score -= 10
    
    # CTA
    if "call" not in email.body.lower():
        score -= 20
    
    # Industry tone
    if industry == "Healthcare" and "patient" not in email.body:
        score -= 10
    
    return {"score": score, "pass": score >= 80}
```

### Tools Used

| Tool | Purpose | When Used |
|------|---------|-----------|
| AWS Bedrock (Claude) | Generate email | Always |
| Case Study Matcher | Select relevant case study | Always |
| Industry Context DB | Get industry guidelines | Always |
| Tone Analyzer | Ensure appropriate tone | Always |
| Email Validator | Check quality | Always |
| A/B Variant Generator | Create variants | When A/B testing |
| Attachment Selector | Choose PDFs | When needed |

### Decision Tree

```
Generate for Mayo Clinic
  │
  ├─ Analyze
  │   ├─ Industry: Healthcare → Empathetic tone
  │   ├─ Title: CIO → Technical ROI focus
  │   └─ News: AI diagnostics → Reference this
  │
  ├─ Select case study
  │   └─ "Hospital reduces wait times 40%" ✓
  │
  ├─ Generate
  │   ├─ Subject: "mayo clinic + ai efficiency"
  │   ├─ Preheader: "How we helped similar hospitals"
  │   └─ Body: AI launch + case study + CTA
  │
  ├─ Validate
  │   ├─ Word count: 142 ✓
  │   ├─ Personalization: Company + news ✓
  │   ├─ Subject: 4 words ✓
  │   ├─ CTA: "15-min call?" ✓
  │   └─ Quality: 95% ✓
  │
  └─ Output for approval
```

### Output Example

```json
{
  "subject": "mayo clinic + ai efficiency",
  "preheader": "How we helped similar hospitals cut wait times 40%",
  "body": "Hi John,\n\nCongratulations on Mayo Clinic's new AI diagnostics program—exciting to see healthcare innovation.\n\nWe recently helped Cleveland Clinic reduce patient wait times by 40% using similar AI-driven improvements. Their CIO mentioned ROI was evident within 90 days.\n\nGiven your focus on technical efficiency and patient outcomes, I thought this might resonate.\n\n15-minute call to discuss?\n\nBest,\n[Sender]",
  "personalization_score": 95,
  "word_count": 142,
  "quality_score": 95,
  "generation_time": "3.2s",
  "cost": "$0.003"
}
```

---

## Agent 3: Publishing & Response Management Agent

### Purpose
Sends emails at optimal times, tracks engagement, classifies responses, manages lead lifecycle.

### What It Does

**1. Determines Send Time**
```python
async def determine_send_time(prospect):
    factors = {
        "timezone": prospect.timezone,  # CST
        "industry": prospect.industry,  # Healthcare
        "title": prospect.title,  # CIO
        "historical_data": get_open_patterns("Healthcare")
    }
    
    # Agent's reasoning:
    # "Healthcare CIOs check email 8-9 AM local time"
    # "Tuesday/Wednesday have 35% higher opens"
    # "Avoid Monday (overload) and Friday (weekend mode)"
    
    return {
        "send_at": "2026-02-18 08:30:00 CST",  # Tuesday 8:30 AM
        "confidence": 85,
        "reasoning": "Healthcare CIOs most active 8-9 AM Tue/Wed"
    }
```

**2. Manages Sequences**
```python
async def manage_sequence(lead_id, sequence):
    # Email 1 → wait 3 days → Email 2 → wait 5 days → Email 3
    
    await send_email(lead_id, sequence.emails[0])
    
    while sequence.has_next():
        await wait_until(sequence.next_send_time)
        
        # Check: Did they reply?
        if await check_reply(lead_id):
            await pause_sequence(lead_id)  # STOP!
            await notify_user("Lead responded")
            break
        
        # Check: Did they open?
        if await check_open(lead_id):
            sequence.next_email = adjust_for_engagement()
        
        await send_email(lead_id, sequence.next_email())
```

**3. Classifies Responses**
```python
async def classify_response(email_reply):
    prompt = f"""
    Classify: "{email_reply.body}"
    
    Categories:
    - INTERESTED: Wants meeting, positive
    - NOT_INTERESTED: Rejection, "remove me"
    - OUT_OF_OFFICE: Auto-reply
    - QUESTION: Asks question
    - WRONG_CONTACT: "Not the right person"
    """
    
    classification = await bedrock.classify(prompt)
    
    # Take action
    if classification == "INTERESTED":
        await update_lead_status(lead_id, "hot_lead")
        await pause_sequence(lead_id)
        await notify_sales_team()
        await add_points(lead_id, 3)
    
    elif classification == "NOT_INTERESTED":
        await stop_sequence(lead_id)
        await add_to_suppression_list()
    
    return classification
```

**4. Calculates Engagement**
```python
def calculate_score(lead_id):
    activities = get_activities(lead_id)
    
    score = 0
    for activity in activities:
        if activity.type == "opened": score += 1
        if activity.type == "clicked": score += 2
        if activity.type == "replied": score += 3
        if activity.type == "meeting": score += 5
    
    # Apply time decay (30 days)
    score = apply_time_decay(score, activities)
    
    # Assign grade
    if score >= 10: grade = "A"  # Hot
    elif score >= 5: grade = "B"  # Warm
    elif score >= 2: grade = "C"  # Cold
    else: grade = "D"  # Dead
    
    return {"score": score, "grade": grade}
```

### Tools Used

| Tool | Purpose | When Used |
|------|---------|-----------|
| AWS SES | Send emails | Always |
| Send Time Optimizer | Calculate best time | Always |
| Tracking Pixel | Track opens | Always |
| Link Tracker | Track clicks | Always |
| AWS Bedrock | Classify responses | When reply received |
| Engagement Scorer | Calculate lead score | Always |
| Sequence Manager | Handle sequences | When enabled |
| Bounce Handler | Process bounces | When occurs |

### Decision Tree

```
Send to Mayo Clinic
  │
  ├─ Determine time
  │   ├─ Timezone: CST
  │   ├─ Industry: Healthcare → 8-9 AM
  │   ├─ Day: Tuesday (35% higher)
  │   └─ Scheduled: Tue 8:30 AM CST
  │
  ├─ Send email
  │   ├─ Insert tracking pixel
  │   ├─ Convert to tracked links
  │   └─ Send via SES
  │
  ├─ Monitor (Day 1)
  │   ├─ Opened 8:45 AM ✓ → +1 pt
  │   ├─ Clicked 8:47 AM ✓ → +2 pts
  │   └─ Score: 3 (Grade C → B)
  │
  ├─ Wait 3 days for Email 2
  │   └─ No reply → Send Email 2
  │
  ├─ Monitor (Day 4)
  │   ├─ Opened 9:15 AM ✓ → +1 pt
  │   ├─ Replied 10:30 AM ✓ → +3 pts
  │   └─ Score: 7 (Grade B → A)
  │
  ├─ Classify reply
  │   ├─ "Interested, let's schedule"
  │   ├─ Classification: INTERESTED (98%)
  │   └─ Action: PAUSE, notify sales
  │
  └─ Update
      ├─ Status: Hot Lead
      ├─ Grade: A
      └─ Next: Sales follow-up
```

### Output Example

```json
{
  "lead_id": "mayo_clinic_001",
  "sequence_status": "paused",
  "emails_sent": 2,
  "engagement": {
    "opens": 2,
    "clicks": 1,
    "replies": 1,
    "score": 7,
    "grade": "A"
  },
  "last_activity": {
    "type": "replied",
    "timestamp": "2026-02-21 10:30:00",
    "classification": "INTERESTED",
    "confidence": 98
  },
  "reply": "Interested, let's schedule a call",
  "recommended_action": "Sales follow-up within 24 hours",
  "paused_reason": "Positive reply received"
}
```

---

## Orchestrator Agent

### Purpose
Coordinates all agents, manages workflow state, handles human approval, ensures smooth handoffs.

### What It Does

**1. Routes Work**
```python
async def run_campaign(prospects):
    for prospect in prospects:
        state = {
            "prospect": prospect,
            "enriched_data": None,
            "generated_email": None,
            "approval_status": "pending",
            "sent_status": None
        }
        
        # Step 1: Research
        state["enriched_data"] = await research_agent.enrich(prospect)
        
        if state["enriched_data"]["quality"] < 70:
            await handle_low_quality(prospect)
            continue
        
        # Step 2: Content
        state["generated_email"] = await content_agent.generate(
            state["enriched_data"]
        )
        
        # Step 3: Human Approval (PAUSE HERE)
        state["approval_status"] = "pending_review"
        await save_state(state)
        await wait_for_approval(prospect.id)
        
        # Step 4: Publishing
        if state["approval_status"] == "approved":
            state["sent_status"] = await publishing_agent.send(
                state["generated_email"]
            )
        
        await save_final_state(state)
```

**2. Manages Approval**
```python
async def wait_for_approval(prospect_id):
    while True:
        approval = await check_approval_status(prospect_id)
        
        if approval == "approved":
            return "proceed"
        
        elif approval == "rejected":
            action = await handle_rejection(prospect_id)
            if action == "regenerate":
                return "regenerate"
            else:
                return "skip"
        
        elif approval == "edited":
            return "use_edited"
        
        await asyncio.sleep(60)  # Check again in 1 min
```

**3. Handles Errors**
```python
async def handle_failure(agent_name, error, state):
    if agent_name == "research_agent":
        if error.type == "api_rate_limit":
            await asyncio.sleep(60)
            return "retry"
        elif error.type == "no_data_found":
            return "manual_fallback"
    
    elif agent_name == "content_agent":
        if error.type == "low_quality":
            return "retry_different_case_study"
    
    elif agent_name == "publishing_agent":
        if error.type == "bounce":
            return "skip"
```

### Decision Tree

```
Campaign: 500 prospects
  │
  ├─ For each prospect:
  │   │
  │   ├─ Research Agent
  │   │   ├─ Success? → Continue
  │   │   └─ Failed? → Retry/skip
  │   │
  │   ├─ Quality check
  │   │   ├─ Score > 70? → Continue
  │   │   └─ Score < 70? → Manual/skip
  │   │
  │   ├─ Content Agent
  │   │   ├─ Success? → Continue
  │   │   └─ Failed? → Retry
  │   │
  │   ├─ PAUSE for approval
  │   │   ├─ Approved? → Publishing
  │   │   ├─ Rejected? → Regenerate/skip
  │   │   └─ Edited? → Use edited
  │   │
  │   └─ Publishing Agent
  │       ├─ Success? → Complete
  │       └─ Failed? → Retry/fail
  │
  └─ Campaign complete → Report
```

---

## Complete Workflow Example

### Mayo Clinic Processing

```
┌─────────────────────────────────────────┐
│ ORCHESTRATOR: Start Mayo Clinic         │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ RESEARCH AGENT                          │
│ - Input: "Mayo Clinic, Rochester, $500K"│
│ - Decision: Has website, skip Clearbit  │
│ - Using: Hunter.io, LinkedIn, Perplexity│
│ - Found: 2 contacts, recent news        │
│ - Quality: 92% ✓                        │
│ - Cost: $1.20, Time: 8s                 │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ ORCHESTRATOR: Quality OK → Content      │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ CONTENT AGENT                           │
│ - Analyzing: Healthcare, CIO, AI launch │
│ - Case study: Cleveland Clinic (40%)    │
│ - Generating with Bedrock...            │
│ - Subject: "mayo clinic + ai efficiency"│
│ - Body: 142 words, personalized         │
│ - Quality: 95% ✓                        │
│ - Cost: $0.003, Time: 3s                │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ ORCHESTRATOR: PAUSE for human approval  │
│ - Saved state to database               │
│ - Waiting for user...                   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ USER: Reviews email → APPROVED ✓        │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ ORCHESTRATOR: Approved → Publishing     │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ PUBLISHING AGENT                        │
│ - Optimal time: Tue 8:30 AM CST         │
│ - Scheduled send                        │
│ - Sent via SES ✓                        │
│ - Tracking: Pixel + links inserted      │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ PUBLISHING AGENT: Monitoring            │
│ - Day 1: Opened (8:45 AM) → +1 pt       │
│ - Day 1: Clicked (8:47 AM) → +2 pts     │
│ - Day 4: Replied (10:30 AM) → +3 pts    │
│ - Total: 7 pts, Grade A                 │
│ - Classification: INTERESTED            │
│ - Action: PAUSE sequence, notify sales  │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ ORCHESTRATOR: Campaign complete         │
│ - Status: Hot Lead                      │
│ - Next: Sales team follow-up            │
└─────────────────────────────────────────┘
```

---

## Agent Tools Summary

### Research Agent Tools
- Hunter.io (email finding)
- Clearbit (company data)
- Apollo.io (backup email)
- LinkedIn API (contacts)
- Perplexity API (news/research)
- Website Scraper (company info)
- Email Validator (MX check)

### Content Agent Tools
- AWS Bedrock/Claude (email generation)
- Case Study Matcher (relevance scoring)
- Industry Context DB (guidelines)
- Tone Analyzer (appropriate tone)
- Email Validator (quality check)
- A/B Variant Generator (testing)
- Attachment Selector (PDFs)

### Publishing Agent Tools
- AWS SES (email sending)
- Send Time Optimizer (timing)
- Tracking Pixel Generator (opens)
- Link Tracker (clicks)
- AWS Bedrock/Claude (response classification)
- Engagement Scorer (lead scoring)
- Sequence Manager (multi-email)
- Bounce Handler (failures)

### Orchestrator Tools
- State Manager (workflow persistence)
- Approval Queue (human-in-loop)
- Error Handler (retry logic)
- Agent Router (coordination)
- Cost Tracker (budget monitoring)

---

## Key Agent Capabilities

### Intelligence
- **Autonomous Decision-Making:** Agents decide which tools to use
- **Cost Optimization:** Skip expensive APIs when possible
- **Quality Validation:** Self-check outputs before proceeding
- **Error Recovery:** Try alternatives when primary approach fails

### Adaptability
- **Context-Aware:** Adjust behavior based on industry, role, company size
- **Learning:** Improve from historical performance data
- **Flexible Routing:** Change workflow based on results

### Efficiency
- **Parallel Processing:** Handle multiple prospects simultaneously
- **Early Stopping:** Stop enrichment when sufficient data obtained
- **Smart Retries:** Retry with different approach, not same failed method

---

## Agent vs Service Comparison

| Aspect | Traditional Service | AI Agent |
|--------|-------------------|----------|
| **Decision Making** | Fixed logic | Autonomous |
| **Cost** | Always calls all APIs | Optimizes API usage |
| **Quality** | No validation | Self-validates |
| **Errors** | Simple retry | Intelligent alternatives |
| **Personalization** | Template-based | Context-aware |
| **Adaptability** | Requires code changes | Learns and adapts |

---

## Implementation Notes

### Agent Framework Options
- **LangGraph:** Best for complex workflows, state management
- **LangChain:** Good for tool integration, simpler than LangGraph
- **Custom:** Build your own orchestration (more control, more work)

### Recommended Approach
1. **POC (Weeks 1-5):** Start with simple services (no agents)
2. **MVP (Weeks 6-10):** Add agent layer to Research & Content
3. **Production (Weeks 11+):** Full agent orchestration with LangGraph

### Why This Progression?
- Prove concept quickly without agent complexity
- Add intelligence where it provides most value
- Evolve to full agent system based on real needs

---

## Cost Comparison

### Traditional Service (500 prospects)
```
Clearbit: 500 × $2 = $1,000
Hunter.io: 500 × $0.50 = $250
Email generation: 500 × $0.003 = $1.50
Total: $1,251.50
```

### Agent Approach (500 prospects)
```
Clearbit: 200 × $2 = $400 (agent skipped 300)
Hunter.io: 500 × $0.50 = $250
Email generation: 500 × $0.003 = $1.50
Agent reasoning: 500 × $0.001 = $0.50
Total: $652
Savings: $599.50 (48% reduction)
```

---

## Success Metrics

### Agent Performance
- **Enrichment Quality:** >85% score
- **Cost Optimization:** >40% savings vs fixed approach
- **Generation Quality:** >90% email score
- **Response Time:** <30 seconds per prospect

### Campaign Performance
- **Open Rate:** >27% (industry avg: 15-25%)
- **Reply Rate:** >2.5% (industry avg: 0.5-2%)
- **Lead Quality:** >60% Grade A/B leads
- **ROI:** 3x improvement over manual outreach

---

**End of Document**
