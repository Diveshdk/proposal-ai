# Enhanced DAO Analyzer with HyperOn
import spacy
import requests
import json
from datetime import datetime
from hyperon import MeTTa

nlp = spacy.load("en_core_web_sm")

class DAOAnalyzer:
    def __init__(self):
        self.pyth_url = "https://hermes.pyth.network/v2/updates/price/latest"
        self.metta = MeTTa()  # Direct HyperOn instance

    def extract_amount(self, doc):
        amounts = [ent.text for ent in doc.ents if ent.label_ == "MONEY"]
        return amounts[0] if amounts else "Not specified"

    def extract_timeline(self, doc):
        dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
        return dates[0] if dates else "Timeline unspecified"

    def check_pyth_oracle(self, token="FET"):
        try:
            response = requests.get(f"{self.pyth_url}?ids[]={token}", timeout=5)
            return response.json()['parsed'][0]['price'] if response.ok else "Price N/A"
        except:
            return "Oracle offline"

    def assess_technical_feasibility(self, doc):
        tech_terms = ["smart contract", "blockchain", "integration", "API"]
        score = sum(1 for term in tech_terms if term in doc.text.lower())
        return min(10, score * 2)

    def verify_metta_compliance(self, proposal_text):
        try:
            result = self.metta.run(f'!(compliance-check "{proposal_text}")')
            return str(result[0][0]) if result else "Pending review"
        except:
            return "MeTTa error"

    def generate_report(self, proposal_text):
        doc = nlp(proposal_text)
        analysis = {
            "amount": self.extract_amount(doc),
            "timeline": self.extract_timeline(doc),
            "fet_price": self.check_pyth_oracle(),
            "tech_score": self.assess_technical_feasibility(doc),
            "compliance": self.verify_metta_compliance(proposal_text),
            "timestamp": datetime.now().isoformat()
        }
        
        compliant = "compliant" in analysis['compliance'].lower()
        analysis['recommendation'] = "APPROVE" if (analysis['tech_score'] >= 6 and compliant) else "REVIEW"
        analysis['confidence'] = 0.85 if analysis['recommendation'] == "APPROVE" else 0.6
        
        return analysis

# Ready for your proposals! 
analyzer = DAOAnalyzer()
