# Setup & Run

## 1. Install Dependencies
```bash
pip install -r requirements.txt
```

## 2. Get Google API Key (Free)
1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

## 3. Configure
```bash
cp .env.example .env
```
Edit `.env` and add your Google API key:
```
GOOGLE_API_KEY=your_key_here
```

## 4. Run
```bash
streamlit run app.py
```

Opens at: http://localhost:8501

## 5. Test
1. Upload CSV with columns: `company_name`, `location`, `budget`, `industry`
2. Click "Enrich All" or expand individual rows
3. Review generated emails
4. Approve to send

## CSV Example
```csv
company_name,location,budget,industry
Mayo Clinic,Rochester MN,500000,Healthcare
Tesla Inc,Austin TX,1000000,Technology
```

## Features
- State persists in `sessions/` folder
- Close browser and resume anytime
- Bulk approve with filters
- Edit emails before sending
