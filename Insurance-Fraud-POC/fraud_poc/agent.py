import json
import os
from datetime import datetime

# Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
CLAIMS_FILE = os.path.join(DATA_DIR, 'claims.json')
POLICIES_FILE = os.path.join(DATA_DIR, 'policies.json')
RULES_FILE = os.path.join(DATA_DIR, 'insurance_rules.json')

class InsuranceFraudAgent:
    def __init__(self, gemini_api_key=None):
        self.claims = self.load_json_data(CLAIMS_FILE)
        self.policies = self.load_json_data(POLICIES_FILE)
        self.rules = self.load_json_data(RULES_FILE)
        self.gemini_api_key = gemini_api_key

    def load_json_data(self, filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found at {filepath}")
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {filepath}")
            return []

    def get_claim(self, claim_id):
        for claim in self.claims:
            if claim['claim_id'] == claim_id:
                return claim
        return None

    def get_policy(self, policy_id):
        for policy in self.policies:
            if policy['policy_id'] == policy_id:
                return policy
        return None

    def calculate_days_since_inception(self, start_date_str, death_date_str):
        try:
            start = datetime.strptime(start_date_str, "%Y-%m-%d")
            end = datetime.strptime(death_date_str, "%Y-%m-%d")
            return (end - start).days
        except:
            return 9999 # Default to long time if error

    def evaluate_rules(self, claim, policy, rules):
        violations = []
        total_risk_score = 0
        
        days_active = self.calculate_days_since_inception(policy['start_date'], claim['date_of_death'])

        # Context for rule evaluation
        context = {
            "claim_amount": claim.get('claim_amount', 0),
            "cause_of_death": claim.get('cause_of_death'),
            "location": claim.get('location'),
            "days_since_inception": days_active,
            "premium_status": policy.get('premium_status'),
            "coverage_amount": policy.get('coverage_amount', 0),
            "medical_history": policy.get('medical_history_flag')
        }

        for rule in rules:
            try:
                if eval(rule['condition'], {}, context):
                    violations.append(rule)
                    total_risk_score += rule['risk_score']
            except Exception as e:
                print(f"Error evaluating rule {rule['rule_id']}: {e}")

        return violations, total_risk_score

    def generate_llm_analysis(self, claim, policy, violations, risk_level, probability):
        """
        Generates a reasoning paragraph. 
        Uses Google Gemini if API key is present, otherwise uses a sophisticated template.
        """
        # 1. Try Real LLM (Gemini)
        if self.gemini_api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_api_key)
                
                # Using Gemini 2.0 Flash-Lite as requested
                model = genai.GenerativeModel("gemini-2.0-flash-lite-preview-02-05")
                
                prompt = f"""
                You are an expert SIU (Special Investigations Unit) Fraud Analyst.
                Analyze the following insurance claim and explain the fraud risk assessment.
                
                CLAIM CONTEXT:
                - Claim ID: {claim['claim_id']}
                - Cause of Death: {claim['cause_of_death']}
                - Location: {claim['location']}
                - Claim Amount: ${claim['claim_amount']:,}
                - Policy Start Date: {policy['start_date']}
                - Policy Status: {policy['premium_status']}
                
                RISK ASSESSMENT:
                - Calculated Risk Level: {risk_level}
                - Fraud Probability: {probability:.0%}
                - Detected Violations: {[v['rule_name'] for v in violations]}
                
                INSTRUCTIONS:
                Write a concise, professional paragraph (max 3 sentences) explaining WHY this claim is flagged. 
                Focus on the correlation between the policy age, amount, and cause of death. 
                Do not mention "AI" or "Model". Write as a human investigator.
                """
                
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"LLM Error: {e}")
                # Fall through to template if LLM fails
        
        # 2. Fallback: Sophisticated Template (Simulated LLM)
        if not violations:
            return "Upon review, the claim details align with standard policy provisions. No significant anomalies were detected in the cross-reference of medical history and event circumstances."
        
        reasons = [v['description'].lower() for v in violations]
        reason_text = " and ".join(reasons)
        
        # Dynamic phrasing based on risk
        if risk_level == "Critical":
            opener = "This claim presents a critical fraud risk profile due to a convergence of high-severity indicators."
        elif risk_level == "High":
            opener = "Investigation is recommended as the claim exhibits significant deviations from standard patterns."
        else:
            opener = "The claim has been flagged for review due to specific policy violations."

        return (
            f"{opener} Specifically, we detected that {reason_text}. "
            f"Given the {policy['premium_status']} status and the timeline of events, this warrants immediate SIU attention."
            " (Simulated AI Response)"
        )

    def run_analysis(self, claim_id):
        claim = self.get_claim(claim_id)
        if not claim:
            return {"error": "Claim not found"}

        policy = self.get_policy(claim['policy_id'])
        if not policy:
            return {"error": "Policy not found"}

        violations, risk_score = self.evaluate_rules(claim, policy, self.rules)

        # Additional Heuristics
        if claim['claim_amount'] > policy['coverage_amount']:
             v = {
                 "rule_name": "Over-limit Claim", 
                 "risk_score": 50, 
                 "description": f"claim amount ({claim['claim_amount']}) exceeds policy coverage"
             }
             violations.append(v)
             risk_score += 50
        
        days_active = self.calculate_days_since_inception(policy['start_date'], claim['date_of_death'])
        if policy.get('medical_history_flag') != 'clean' and days_active < 730:
             v = {
                 "rule_name": "Non-Disclosure Risk",
                 "risk_score": 45,
                 "description": "potential non-disclosure of medical history occurred on a recent policy"
             }
             violations.append(v)
             risk_score += 45

        # Calculate Probability (adjusted scale for better distribution)
        # Using 150 as denominator instead of 100 for more realistic probabilities
        probability = min(risk_score / 150.0, 0.99)
        if probability < 0.01: probability = 0.01

        # Determine Risk Level (adjusted thresholds)
        if probability > 0.6:
            risk_level = "Critical"
            action = "SIU Referral (Special Investigations)"
        elif probability > 0.35:
            risk_level = "High"
            action = "Manual Review Required"
        elif probability > 0.15:
            risk_level = "Medium"
            action = "Request Additional Docs"
        else:
            risk_level = "Low"
            action = "Auto-Process"

        # Generate Reasoning (LLM or Template)
        explanation = self.generate_llm_analysis(claim, policy, violations, risk_level, probability)

        return {
            "claim_id": claim_id,
            "fraud_probability": probability,
            "risk_level": risk_level,
            "risk_factors": [v['rule_name'] for v in violations],
            "recommended_action": action,
            "explanation": explanation,
            "details": {
                "violations": violations,
                "claim": claim,
                "policy": policy
            }
        }

if __name__ == "__main__":
    agent = InsuranceFraudAgent()
    result = agent.run_analysis("C1002")
    print(json.dumps(result, indent=2))
