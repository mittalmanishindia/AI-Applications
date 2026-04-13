# Agentic Life Insurance Fraud Detection System

An AI-powered agent designed to detect fraud in life insurance claims by analyzing policy details, claim context, and behavioral patterns. The system now features **Google Gemini 2.0 Flash-Lite** integration for advanced natural language reasoning.

## 📁 Project Structure

```
/fraud_poc/
   /data/
       claims.json         # Sample insurance claims
       policies.json       # Policy holder data
       insurance_rules.json # Configurable fraud rules
   agent.py                # Core logic for insurance fraud analysis
   ui_app.py               # Streamlit Web UI
   generate_user_guide.py  # Script to generate documentation
   readme.md               # This file
```

## 🚀 How to Run

1.  **Install Dependencies**:
    ```bash
    pip install streamlit pandas google-generativeai
    ```

2.  **Run the Application**:
    Navigate to the project directory and run:
    ```bash
    python -m streamlit run fraud_poc/ui_app.py
    ```

3.  **Use the Interface**:
    -   Select a **Claim ID** (e.g., `C1002`).
    -   (Optional) Enter your **Gemini API Key** in the sidebar for AI-powered reasoning.
    -   Click **Analyze Claim Risk**.
    -   View the assessment with risk score, AI reasoning, and workflow diagram.

## 🧠 Agent Capabilities

### Rule-Based Scoring
The agent evaluates claims against configurable rules:
-   **Contestable Period**: Checks if the claim is within 2 years of policy inception.
-   **High Value Threshold**: Flags claims exceeding $1,000,000.
-   **Suspicious Causes**: Flags vague causes of death like "Unknown" or "Unverified Accident".
-   **Foreign Death**: Higher risk for deaths occurring overseas.
-   **Lapsed Policy**: Automatic flag for claims on inactive policies.

### Behavioral Analysis
Beyond simple rules, the system performs cross-referencing:
-   **Non-Disclosure Detection**: Identifies potential medical history concealment on recent policies.
-   **Policy Status Validation**: Automatically flags claims linked to "Lapsed" or inactive policies.
-   **Amount Deviation**: Detects claims significantly higher than policy coverage.

### AI-Powered Reasoning (NEW!)
-   **Gemini Integration**: When an API key is provided, the system uses Google's Gemini 2.0 Flash-Lite model to generate sophisticated, human-like investigation narratives.
-   **Fallback Mode**: Without an API key, uses an advanced template system that produces professional-sounding reports.
-   **Contextual Analysis**: The AI considers policy age, claim amount, cause of death, and violation patterns to explain the risk assessment.

## 📊 Sample Run

**Scenario**: User selects `C1002` (Accidental Fall, $2M Claim, Policy started 2 months ago).

**Output**:
-   **Risk Level**: **Critical** (Red Badge)
-   **Probability**: ~85%
-   **Risk Factors**:
    -   Contestable Period (< 2 years)
    -   High Value Claim (>$1M)
    -   Non-Disclosure Risk (if applicable)
-   **AI Reasoning** (with Gemini): *"This claim warrants immediate investigation due to the substantial payout request occurring within the contestable period. The accidental fall at a remote location, combined with the policy's recent inception date, presents multiple red flags that require thorough verification of circumstances and beneficiary relationships."*
-   **Action**: SIU Referral

## 🎯 Key Features

1.  **Interactive Dashboard**: Clean, modern Streamlit interface with color-coded risk badges.
2.  **Workflow Visualization**: Dynamic flowchart showing the decision path from claim intake to final recommendation.
3.  **Export Capability**: Download investigation reports as JSON for record-keeping.
4.  **Flexible AI Backend**: Supports both Gemini-powered and template-based reasoning.
5.  **Zero Database**: Uses JSON files for easy deployment and demonstration.

## 🔮 Future Enhancements (Roadmap)

### Phase 2: Machine Learning Integration
1.  **IsolationForest Anomaly Detection**: Implement unsupervised learning (Scikit-Learn) to detect outliers without pre-defined rules.
2.  **Vector Embeddings**: Convert transaction metadata into vector embeddings for semantic similarity search against known fraud cases.

### Phase 3: Multi-Agent Architecture
3.  **Multi-Agent Orchestration**:
    -   *Risk Agent*: Scores the transaction using rules and ML.
    -   *Investigator Agent*: Gathers external OSINT data (social media, public records).
    -   *Decision Agent*: Synthesizes inputs for a final verdict.

### Phase 4: Production Deployment
4.  **Real-time API**: Expose `agent.py` logic via FastAPI for integration with policy management systems.
5.  **Medical Record NLP**: Parse PDF medical records to find inconsistencies with cause of death.
6.  **Hospital API Integration**: Verify death certificates directly with issuing hospitals.
7.  **Audit Trail**: Complete logging system for compliance and review.

## 🔐 Security Notes

-   API keys are handled securely via Streamlit's password input (not stored in code).
-   The `eval()` function is used for rule evaluation in this POC. In production, replace with a proper rule engine (e.g., Python's `ast.literal_eval` or a DSL parser).

## 📖 Documentation

Run the documentation generator to create a detailed Word document:
```bash
python fraud_poc/generate_user_guide.py
```

This will create `Life_Insurance_Fraud_User_Guide.docx` with comprehensive usage instructions.

## 🛠️ Technology Stack

-   **Backend**: Python 3.9+
-   **UI Framework**: Streamlit
-   **AI/LLM**: Google Gemini 2.0 Flash-Lite (via `google-generativeai`)
-   **Data Storage**: JSON files (for demonstration)
-   **Visualization**: Graphviz (for workflow diagrams)

## 📝 License

This is a Proof of Concept (POC) for demonstration purposes. Not intended for production use without proper security hardening and compliance review.
