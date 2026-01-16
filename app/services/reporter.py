from fpdf import FPDF
import json
class IncidentReporter(FPDF):
    def generate(self, incident_data):
        self.add_page()
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, f"PurpleAI Report #{incident_data['id']}", ln=True, align="C")
        self.set_font("Arial", "", 12)
        self.ln(10)
        self.multi_cell(0, 10, f"Analysis:\n{incident_data['ai_analysis']}")
        return self.output(dest='S').encode('latin-1')