"""
B2B Sales Email Campaign - Professional Dashboard
"""

import streamlit as st
import pandas as pd
from agents.orchestrator import run_campaign

st.set_page_config(page_title="Email Campaign", layout="wide")

# Initialize session state
if "prospects" not in st.session_state:
    st.session_state.prospects = []
if "enriched_data" not in st.session_state:
    st.session_state.enriched_data = {}
if "selected_rows" not in st.session_state:
    st.session_state.selected_rows = set()

# Header
st.title("Sales Email Campaign")
st.divider()

# Filters Row
col1, col2 = st.columns([1, 1])

with col1:
    if st.session_state.prospects:
        industries = ["All Industries"] + list(set([p.get('industry', 'Unknown') for p in st.session_state.prospects]))
    else:
        industries = ["All Industries"]
    selected_industry = st.selectbox("Filter by Industry", industries)

with col2:
    statuses = ["All Status", "Pending", "Enriched", "Generated", "Approved", "Sent"]
    selected_status = st.selectbox("Filter by Status", statuses)

# Action Buttons Row
col3, col4 = st.columns([1, 1])

with col3:
    if st.button("Enrich All", type="primary", width="stretch"):
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total = len(st.session_state.prospects)
            
            for idx, prospect in enumerate(st.session_state.prospects):
                if idx not in st.session_state.enriched_data:
                    company = prospect.get('company_name', 'Unknown')
                    
                    # Update progress
                    progress = (idx + 1) / total
                    progress_bar.progress(progress)
                    status_text.text(f"Processing {idx + 1}/{total}: {company}")
                    
                    # Log to console
                    print(f"[ENRICHMENT] Starting enrichment for: {company}")
                    
                    result = run_campaign(
                        prospect_id=f"prospect_{idx}",
                        prospect=prospect,
                        approved=False
                    )
                    
                    st.session_state.enriched_data[idx] = result
                    print(f"[ENRICHMENT] Completed: {company}")
            
            progress_bar.progress(1.0)
            status_text.text("All prospects enriched!")
            st.success("Enrichment complete!")
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            print(f"[ERROR] Enrichment failed: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

with col4:
    if st.button("Approve Selected", disabled=len(st.session_state.selected_rows)==0, width="stretch"):
        for idx in st.session_state.selected_rows:
            if idx in st.session_state.enriched_data:
                prospect = st.session_state.prospects[idx]
                result = run_campaign(prospect, approved=True)
                st.session_state.enriched_data[idx]['status'] = 'sent'
        st.success(f"Sent {len(st.session_state.selected_rows)} emails!")
        st.session_state.selected_rows = set()
        st.rerun()

st.divider()

# Upload Section
with st.container():
    st.subheader("Upload Prospects")
    uploaded_file = st.file_uploader(
        "Drag and drop CSV file or browse",
        type=['csv'],
        help="CSV will be automatically mapped to: company_name, location, budget, industry"
    )
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        # Flexible column mapping (case-insensitive, handles spaces)
        def find_column(df, possible_names):
            """Find column by matching possible names"""
            df_cols_lower = {col.lower().strip(): col for col in df.columns}
            for name in possible_names:
                if name.lower().strip() in df_cols_lower:
                    return df_cols_lower[name.lower().strip()]
            return None
        
        # Map to standard names
        mapping = {}
        
        company_col = find_column(df, ['company_name', 'company name', 'company', 'name'])
        if company_col:
            mapping[company_col] = 'company_name'
        
        location_col = find_column(df, ['location', 'region', 'region / location', 'city'])
        if location_col:
            mapping[location_col] = 'location'
        
        industry_col = find_column(df, ['industry', 'sector', 'vertical'])
        if industry_col:
            mapping[industry_col] = 'industry'
        
        budget_col = find_column(df, ['budget', 'deal size', 'value'])
        if budget_col:
            mapping[budget_col] = 'budget'
        
        # Rename columns
        df = df.rename(columns=mapping)
        
        # Add defaults for missing columns
        if 'location' not in df.columns:
            df['location'] = 'Unknown'
        if 'industry' not in df.columns:
            df['industry'] = 'General'
        
        # Check if company_name exists
        if 'company_name' not in df.columns:
            st.error("Could not find company name column. Please ensure your CSV has a column with company names.")
            st.info(f"Your columns: {', '.join(df.columns.tolist())}")
        else:
            # Show preview - display all columns from CSV
            st.write(f"**Preview** ({len(df)} prospects found)")
            st.dataframe(df, width="stretch", height=300)
            
            col_load, col_cancel = st.columns([1, 3])
            
            with col_load:
                if st.button("Load Prospects", type="primary"):
                    st.session_state.prospects = df.to_dict('records')
                    st.session_state.enriched_data = {}
                    st.session_state.selected_rows = set()
                    st.success(f"Loaded {len(df)} prospects")
                    st.rerun()
            st.rerun()

st.divider()

# Prospect List
if st.session_state.prospects:
    st.subheader("Prospect List")
    
    # Filter prospects
    filtered_prospects = []
    for idx, prospect in enumerate(st.session_state.prospects):
        # Industry filter
        if selected_industry != "All Industries" and prospect.get('industry') != selected_industry:
            continue
        
        # Status filter
        status = st.session_state.enriched_data.get(idx, {}).get('status', 'Pending')
        if selected_status != "All Status" and status != selected_status:
            continue
        
        filtered_prospects.append((idx, prospect))
    
    if not filtered_prospects:
        st.info("No prospects match the selected filters")
    else:
        # Display each prospect
        for idx, prospect in filtered_prospects:
            with st.container():
                # Main row - all at same level
                cols = st.columns([0.3, 2, 1.5, 1, 1, 1, 0.5])
            
            # Checkbox
            is_selected = cols[0].checkbox("", key=f"select_{idx}", value=idx in st.session_state.selected_rows)
            if is_selected:
                st.session_state.selected_rows.add(idx)
            else:
                st.session_state.selected_rows.discard(idx)
            
            # Company name
            cols[1].write(f"**{prospect['company_name']}**")
            
            # Industry
            cols[2].write(prospect.get('industry', 'N/A'))
            
            # Location
            cols[3].write(prospect.get('location', 'N/A'))
            
            # Status
            if idx in st.session_state.enriched_data:
                status = st.session_state.enriched_data[idx].get('status', 'pending_approval')
                # Make status user-friendly
                status_display = {
                    'pending_approval': 'Ready to Review',
                    'sent': 'Sent',
                    'skipped': 'Skipped'
                }.get(status, 'Enriched')
            else:
                status_display = 'Not Enriched'
            
            cols[5].write(status_display)
            
            # Expand button
            expand = cols[6].button("Details", key=f"expand_{idx}")
            
            # Expanded section
            if expand:
                st.session_state[f"expanded_{idx}"] = not st.session_state.get(f"expanded_{idx}", False)
                st.rerun()
            
            if st.session_state.get(f"expanded_{idx}", False):
                with st.container():
                    st.markdown("---")
                    
                    # Check if enriched
                    if idx not in st.session_state.enriched_data:
                        st.warning("Not enriched yet. Click 'Enrich All' first.")
                    else:
                        data = st.session_state.enriched_data[idx]
                        
                        # Debug: Show what we have
                        st.write(f"DEBUG: Keys in data: {list(data.keys())}")
                        
                        enriched = data.get('enriched_data', {})
                        email = data.get('email', {})
                        
                        if not enriched:
                            st.error("No enriched data found")
                        else:
                            st.success("Data found!")
                            st.json(enriched)  # Show raw data for now
                        col_left, col_right = st.columns(2)
                        
                        with col_left:
                            st.write("**Company Information**")
                            info = enriched['company_info']
                            st.write(info.get('description', 'N/A'))
                            if info.get('website'):
                                st.write(f"🌐 {info['website']}")
                            if info.get('employee_count'):
                                st.write(f"👥 Employees: {info['employee_count']}")
                            if info.get('revenue'):
                                st.write(f"💰 Revenue: {info['revenue']}")
                            
                            st.write("")
                            st.write("**Decision Makers**")
                            contacts = enriched.get('contacts', [])
                            if contacts:
                                for contact in contacts:
                                    st.write(f"**{contact.get('name', 'N/A')}** - {contact.get('title', 'N/A')}")
                                    st.write(f"📧 {contact.get('email', 'N/A')}")
                                    if contact.get('linkedin'):
                                        st.write(f"🔗 {contact['linkedin']}")
                                    st.write("")
                            else:
                                st.info("No contacts found")
                            
                            st.write("**Recent News**")
                            news = enriched.get('recent_news', [])
                            if news:
                                for item in news:
                                    st.write(f"• {item}")
                            else:
                                st.info("No recent news found")
                            
                            if enriched.get('pain_points'):
                                st.write("")
                                st.write("**Likely Pain Points**")
                                for pain in enriched['pain_points']:
                                    st.write(f"• {pain}")
                        
                        with col_right:
                            st.write("**Generated Email**")
                            
                            subject = st.text_input("Subject", email['subject'], key=f"subj_{idx}")
                            body = st.text_area("Body", email['body'], height=250, key=f"body_{idx}")
                            st.write(f"Word Count: {email['word_count']}")
                            
                            st.write("**Attachments**")
                            st.write("None")
                        
                        # Actions
                        action_cols = st.columns([1, 1, 1, 3])
                        
                        if action_cols[0].button("Approve", key=f"approve_{idx}", type="primary"):
                            # Resume Strands graph from approval node
                            result = run_campaign(
                                prospect_id=f"prospect_{idx}",
                                prospect=prospect,
                                approved=True
                            )
                            st.session_state.enriched_data[idx]['status'] = 'sent'
                            st.success("Email sent!")
                            st.rerun()
                        
                        if action_cols[1].button("Regenerate", key=f"regen_{idx}"):
                            result = run_campaign(prospect)
                            st.session_state.enriched_data[idx] = result
                            st.rerun()
                        
                        if action_cols[2].button("Skip", key=f"skip_{idx}"):
                            st.session_state.enriched_data[idx]['status'] = 'skipped'
                            st.rerun()
            
            st.divider()
else:
    st.info("Upload a CSV file to get started")
