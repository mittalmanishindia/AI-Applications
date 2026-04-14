import streamlit as st
import pandas as pd
import json
import time
from agent import InsuranceFraudAgent

# Page Config
st.set_page_config(
    page_title="Life Insurance Fraud Detector",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        background-color: #2c3e50; 
        color: white; 
        font-weight: bold;
        border-radius: 8px;
        height: 50px;
    }
    .risk-card {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-container {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize Agent
@st.cache_resource
def load_agent():
    return InsuranceFraudAgent()

agent = load_agent()

# Sidebar
st.sidebar.title("🏥 Claims Guard AI")
st.sidebar.markdown("---")

# API Key Input
api_key = st.sidebar.text_input("Gemini API Key (Optional)", type="password", help="Enter your Google Gemini API Key to enable GenAI reasoning. Leave blank for simulated AI.")

st.sidebar.subheader("System Status")
st.sidebar.success("Agent Online")

# Initialize Agent with Key
@st.cache_resource
def load_agent(key):
    return InsuranceFraudAgent(gemini_api_key=key)

# Reload agent if key changes (simple way)
agent = InsuranceFraudAgent(gemini_api_key=api_key)

st.sidebar.info(f"Rules Loaded: {len(agent.rules)}")
st.sidebar.info(f"Policies Monitored: {len(agent.policies)}")

st.sidebar.markdown("---")
st.sidebar.subheader("Data Sources")
st.sidebar.code("claims.json\npolicies.json\ninsurance_rules.json", language="text")

# Main Content
st.title("📋 Life Insurance Claim Analysis")
st.markdown("Select a Claim ID to perform real-time fraud evaluation.")

# Input Section
col1, col2 = st.columns([1, 2])

with col1:
    claim_ids = [c['claim_id'] for c in agent.claims]
    selected_claim = st.selectbox("Select Claim ID", claim_ids)
    
    analyze_btn = st.button("Analyze Claim Risk")

if analyze_btn:
    with st.spinner('Agent is cross-referencing policy data and rules...'):
        time.sleep(1.5) # Simulate processing
        result = agent.run_analysis(selected_claim)
    
    if "error" in result:
        st.error(result["error"])
    else:
        # Display Results
        st.markdown("### 📊 Analysis Results")
        
        # Risk Badge Color
        risk_color = {
            "Low": "#28a745",      # Green
            "Medium": "#ffc107",   # Yellow
            "High": "#fd7e14",     # Orange
            "Critical": "#dc3545"  # Red
        }
        
        bg_color = risk_color.get(result['risk_level'], "#6c757d")
        
        # Top Metrics
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div class="risk-card" style="background-color: {bg_color}; color: white;">
                <h2>{result['risk_level']}</h2>
                <p>Risk Level</p>
            </div>
            """, unsafe_allow_html=True)
        with m2:
             st.markdown(f"""
            <div class="metric-container">
                <h2 style="color: #333;">{result['fraud_probability']:.2%}</h2>
                <p style="color: #666;">Fraud Probability</p>
            </div>
            """, unsafe_allow_html=True)
        with m3:
             st.markdown(f"""
            <div class="metric-container">
                <h2 style="color: #333;">{result['recommended_action']}</h2>
                <p style="color: #666;">Recommended Action</p>
            </div>
            """, unsafe_allow_html=True)

        # Detailed Analysis
        st.markdown("---")
        c1, c2 = st.columns([2, 1])
        
        with c1:
            st.subheader("🤖 AI Reasoning")
            st.info(result['explanation'])
            
            st.subheader("Risk Factors Detected")
            if result['risk_factors']:
                for factor in result['risk_factors']:
                    st.warning(f"⚠️ {factor}")
            else:
                st.success("✅ No specific risk factors detected.")

        with c2:
            st.subheader("Claim & Policy Details")
            claim_details = result['details']['claim']
            policy_details = result['details']['policy']
            
            st.json({
                "Claim Amount": f"${claim_details['claim_amount']:,}",
                "Cause": claim_details['cause_of_death'],
                "Location": claim_details['location'],
                "Policy Holder": policy_details['policy_holder'],
                "Policy Start": policy_details['start_date'],
                "Premium Status": policy_details['premium_status']
            })

        # Workflow Visualization
        st.markdown("---")
        st.subheader("⚙️ Decision Logic Visualization")
        
        # Determine path colors based on result
        is_high_risk = result['risk_level'] in ['High', 'Critical']
        risk_node_color = "red" if is_high_risk else "green"
        
        graph = f"""
        digraph G {{
            rankdir=LR;
            node [shape=box, style=filled, fillcolor="white", fontname="Arial"];
            
            Start [label="New Claim\\n{selected_claim}", shape=oval, fillcolor="#E3F2FD"];
            Data [label="Fetch Policy\\n& History", fillcolor="#FFF3E0"];
            Rules [label="Evaluate Rules\\n(Contestability, Amount, Cause)", fillcolor="#FFF3E0"];
            Score [label="Calculate\\nRisk Score", fillcolor="#FFF3E0"];
            Decision [label="{result['risk_level']} Risk\\n{result['recommended_action']}", style=filled, fillcolor="{risk_node_color}", fontcolor="white"];
            
            Start -> Data;
            Data -> Rules;
            Rules -> Score;
            Score -> Decision;
            
            subgraph cluster_0 {{
                label = "Agent Core";
                style=dashed;
                color=grey;
                Data; Rules; Score;
            }}
        }}
        """
        st.graphviz_chart(graph)

        # Export
        st.markdown("---")
        st.download_button(
            label="📥 Export Investigation Report (JSON)",
            data=json.dumps(result, indent=2),
            file_name=f"claim_investigation_{selected_claim}.json",
            mime="application/json"
        )

else:
    # Initial State / Placeholder
    st.info("👈 Select a claim and click 'Analyze' to start.")
    
    # Show recent claims table
    st.subheader("Recent Claims Queue")
    df = pd.DataFrame(agent.claims)
    st.dataframe(df[['claim_id', 'policy_id', 'claim_amount', 'cause_of_death', 'date_of_death']].head(10), use_container_width=True)
