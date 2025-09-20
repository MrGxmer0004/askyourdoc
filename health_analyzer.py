"""
Health Analyzer for generating comprehensive health insights using RAG workflow
"""

from typing import Dict, List, Any, Optional
from knowledge_base import MedicalKnowledgeBase
from lab_report_processor import LabReportProcessor
import json
from datetime import datetime

class HealthAnalyzer:
    def __init__(self, knowledge_base: MedicalKnowledgeBase):
        self.kb = knowledge_base
        self.medical_disclaimer = """
**IMPORTANT MEDICAL DISCLAIMER**

This analysis is for informational purposes only and should not be considered as medical advice, diagnosis, or treatment recommendation. The information provided is based on general medical knowledge and data patterns, but individual health conditions can vary significantly.

**CRITICAL WARNINGS:**
- This analysis is NOT a substitute for professional medical consultation
- Always consult with a qualified healthcare provider for any health concerns
- Do not make medical decisions based solely on this analysis
- Seek immediate medical attention for any urgent health issues
- Individual health conditions require personalized medical evaluation

The insights provided are based on statistical patterns and general medical knowledge, but your specific health situation may differ. Only a licensed healthcare professional can provide proper medical diagnosis and treatment recommendations.
"""
    
    def analyze_health_report(self, 
                            biomarker_data: Dict[str, float], 
                            user_symptoms: str = "", 
                            user_lifestyle: str = "") -> Dict[str, Any]:
        """
        Perform comprehensive health analysis using the Four Pillars approach
        """
        
        # Retrieve contextual knowledge for all biomarkers
        contextual_knowledge = self._retrieve_contextual_knowledge(biomarker_data)
        
        # Perform Four Pillars analysis
        analysis = {
            'disclaimer': self.medical_disclaimer,
            'timestamp': datetime.now().isoformat(),
            'pillar_1_biomarker_interpretation': self._analyze_biomarkers(biomarker_data, contextual_knowledge),
            'pillar_2_symptom_correlation': self._correlate_symptoms_biomarkers(biomarker_data, user_symptoms, contextual_knowledge),
            'pillar_3_predictive_insights': self._generate_predictive_insights(biomarker_data, contextual_knowledge),
            'pillar_4_actionable_recommendations': self._generate_recommendations(biomarker_data, user_symptoms, user_lifestyle, contextual_knowledge),
            'contextual_knowledge_used': contextual_knowledge
        }
        
        return analysis
    
    def _retrieve_contextual_knowledge(self, biomarker_data: Dict[str, float]) -> Dict[str, List[Dict]]:
        """Retrieve relevant contextual knowledge for each biomarker"""
        contextual_knowledge = {}
        
        for biomarker, value in biomarker_data.items():
            # Create query for this biomarker
            query = f"{biomarker} {value} biomarker analysis"
            knowledge = self.kb.retrieve_contextual_knowledge(query, top_k=3)
            contextual_knowledge[biomarker] = knowledge
        
        # Also get general health insights
        general_query = "health risk assessment biomarker patterns"
        general_knowledge = self.kb.retrieve_contextual_knowledge(general_query, top_k=5)
        contextual_knowledge['general'] = general_knowledge
        
        return contextual_knowledge
    
    def _analyze_biomarkers(self, biomarker_data: Dict[str, float], contextual_knowledge: Dict) -> Dict[str, Any]:
        """Pillar 1: Interpretation of Key Biomarkers"""
        analysis = {
            'title': 'Interpretation of Key Biomarkers',
            'biomarkers': {}
        }
        
        for biomarker, value in biomarker_data.items():
            # Get reference range
            reference_range = self.kb.get_biomarker_reference_range(biomarker)
            
            # Classify status
            status = self._classify_biomarker_status(biomarker, value, reference_range)
            
            # Get contextual insights
            biomarker_knowledge = contextual_knowledge.get(biomarker, [])
            
            analysis['biomarkers'][biomarker] = {
                'value': value,
                'reference_range': reference_range,
                'status': status,
                'interpretation': self._generate_biomarker_interpretation(biomarker, value, status, biomarker_knowledge),
                'contextual_insights': biomarker_knowledge
            }
        
        return analysis
    
    def _correlate_symptoms_biomarkers(self, biomarker_data: Dict[str, float], user_symptoms: str, contextual_knowledge: Dict) -> Dict[str, Any]:
        """Pillar 2: Correlation Between Symptoms and Biomarker Trends"""
        analysis = {
            'title': 'Correlation Between Symptoms and Biomarker Trends',
            'correlations': [],
            'symptom_analysis': self._analyze_symptoms(user_symptoms)
        }
        
        if not user_symptoms.strip():
            analysis['note'] = 'No symptoms provided for correlation analysis'
            return analysis
        
        # Find correlations between symptoms and biomarkers
        for biomarker, value in biomarker_data.items():
            biomarker_knowledge = contextual_knowledge.get(biomarker, [])
            correlation = self._find_symptom_biomarker_correlation(biomarker, value, user_symptoms, biomarker_knowledge)
            if correlation:
                analysis['correlations'].append(correlation)
        
        return analysis
    
    def _generate_predictive_insights(self, biomarker_data: Dict[str, float], contextual_knowledge: Dict) -> Dict[str, Any]:
        """Pillar 3: Predictive Insights on Potential Health Risks"""
        analysis = {
            'title': 'Predictive Insights on Potential Health Risks',
            'risk_assessments': [],
            'overall_risk_level': 'moderate'  # Default
        }
        
        # Assess risks based on biomarker patterns
        risks = []
        
        # Diabetes risk
        if 'glucose' in biomarker_data or 'hba1c' in biomarker_data:
            diabetes_risk = self._assess_diabetes_risk(biomarker_data, contextual_knowledge)
            if diabetes_risk:
                risks.append(diabetes_risk)
        
        # Cardiovascular risk
        if any(bm in biomarker_data for bm in ['total_cholesterol', 'ldl', 'hdl', 'triglycerides']):
            cv_risk = self._assess_cardiovascular_risk(biomarker_data, contextual_knowledge)
            if cv_risk:
                risks.append(cv_risk)
        
        # Thyroid risk
        if 'tsh' in biomarker_data:
            thyroid_risk = self._assess_thyroid_risk(biomarker_data, contextual_knowledge)
            if thyroid_risk:
                risks.append(thyroid_risk)
        
        # Inflammation risk
        if any(bm in biomarker_data for bm in ['crp', 'esr']):
            inflammation_risk = self._assess_inflammation_risk(biomarker_data, contextual_knowledge)
            if inflammation_risk:
                risks.append(inflammation_risk)
        
        analysis['risk_assessments'] = risks
        analysis['overall_risk_level'] = self._calculate_overall_risk_level(risks)
        
        return analysis
    
    def _generate_recommendations(self, biomarker_data: Dict[str, float], user_symptoms: str, user_lifestyle: str, contextual_knowledge: Dict) -> Dict[str, Any]:
        """Pillar 4: Clear, Actionable Recommendations"""
        analysis = {
            'title': 'Clear, Actionable Recommendations',
            'immediate_actions': [],
            'lifestyle_recommendations': [],
            'monitoring_recommendations': [],
            'medical_consultation_required': False
        }
        
        # Check for critical values requiring immediate medical attention
        critical_findings = self._identify_critical_findings(biomarker_data)
        if critical_findings:
            analysis['immediate_actions'].extend(critical_findings)
            analysis['medical_consultation_required'] = True
        
        # Generate lifestyle recommendations
        lifestyle_recs = self._generate_lifestyle_recommendations(biomarker_data, user_lifestyle, contextual_knowledge)
        analysis['lifestyle_recommendations'].extend(lifestyle_recs)
        
        # Generate monitoring recommendations
        monitoring_recs = self._generate_monitoring_recommendations(biomarker_data, contextual_knowledge)
        analysis['monitoring_recommendations'].extend(monitoring_recs)
        
        return analysis
    
    def _classify_biomarker_status(self, biomarker: str, value: float, reference_range: Optional[str]) -> str:
        """Classify biomarker as Normal, High, Low, or Unknown"""
        if not reference_range:
            return "Unknown"
        
        # Use the knowledge base classification method
        return self.kb._classify_value(value, reference_range)
    
    def _generate_biomarker_interpretation(self, biomarker: str, value: float, status: str, knowledge: List[Dict]) -> str:
        """Generate interpretation for a biomarker based on value and contextual knowledge"""
        interpretation = f"Your {biomarker} level is {value}, which is classified as {status}."
        
        if knowledge:
            # Add contextual insights
            for insight in knowledge[:2]:  # Use top 2 insights
                if insight['type'] == 'dataset_insight':
                    interpretation += f" {insight['text']}"
                elif insight['type'] == 'abnormality_mapping':
                    interpretation += f" This pattern is associated with {insight['condition']}."
        
        return interpretation
    
    def _analyze_symptoms(self, user_symptoms: str) -> Dict[str, Any]:
        """Analyze user-provided symptoms"""
        if not user_symptoms.strip():
            return {'symptoms_provided': False}
        
        # Simple symptom analysis - in production, you'd use more sophisticated NLP
        symptoms = user_symptoms.lower().split()
        common_symptoms = {
            'fatigue': ['tired', 'fatigue', 'exhausted', 'weak'],
            'weight_changes': ['weight', 'gain', 'loss', 'obese'],
            'mood_changes': ['depressed', 'anxious', 'mood', 'irritable'],
            'digestive_issues': ['nausea', 'vomiting', 'diarrhea', 'constipation'],
            'cardiovascular': ['chest', 'pain', 'heart', 'palpitations'],
            'neurological': ['headache', 'dizziness', 'confusion', 'memory']
        }
        
        detected_symptoms = []
        for category, symptom_list in common_symptoms.items():
            if any(symptom in user_symptoms.lower() for symptom in symptom_list):
                detected_symptoms.append(category)
        
        return {
            'symptoms_provided': True,
            'raw_symptoms': user_symptoms,
            'detected_categories': detected_symptoms
        }
    
    def _find_symptom_biomarker_correlation(self, biomarker: str, value: float, user_symptoms: str, knowledge: List[Dict]) -> Optional[Dict]:
        """Find correlations between symptoms and biomarkers"""
        # This is a simplified correlation - in production, you'd use more sophisticated analysis
        correlations = {
            'tsh': ['fatigue', 'weight_changes', 'mood_changes'],
            'glucose': ['fatigue', 'weight_changes', 'digestive_issues'],
            'hba1c': ['fatigue', 'weight_changes'],
            'total_cholesterol': ['cardiovascular'],
            'ldl': ['cardiovascular'],
            'crp': ['fatigue', 'cardiovascular']
        }
        
        if biomarker in correlations:
            symptom_categories = self._analyze_symptoms(user_symptoms)['detected_categories']
            matching_symptoms = [cat for cat in symptom_categories if cat in correlations[biomarker]]
            
            if matching_symptoms:
                return {
                    'biomarker': biomarker,
                    'value': value,
                    'correlated_symptoms': matching_symptoms,
                    'explanation': f"Your {biomarker} level of {value} may be related to your reported symptoms: {', '.join(matching_symptoms)}"
                }
        
        return None
    
    def _assess_diabetes_risk(self, biomarker_data: Dict[str, float], contextual_knowledge: Dict) -> Optional[Dict]:
        """Assess diabetes risk based on glucose and HbA1c"""
        risk_factors = []
        risk_level = 'low'
        
        if 'glucose' in biomarker_data:
            glucose = biomarker_data['glucose']
            if glucose >= 126:
                risk_factors.append(f"Fasting glucose {glucose} mg/dL indicates diabetes")
                risk_level = 'high'
            elif glucose >= 100:
                risk_factors.append(f"Fasting glucose {glucose} mg/dL indicates prediabetes")
                risk_level = 'moderate'
        
        if 'hba1c' in biomarker_data:
            hba1c = biomarker_data['hba1c']
            if hba1c >= 6.5:
                risk_factors.append(f"HbA1c {hba1c}% indicates diabetes")
                risk_level = 'high'
            elif hba1c >= 5.7:
                risk_factors.append(f"HbA1c {hba1c}% indicates prediabetes")
                risk_level = 'moderate'
        
        if risk_factors:
            return {
                'condition': 'Diabetes/Pre-diabetes',
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'contextual_insights': contextual_knowledge.get('general', [])[:2]
            }
        
        return None
    
    def _assess_cardiovascular_risk(self, biomarker_data: Dict[str, float], contextual_knowledge: Dict) -> Optional[Dict]:
        """Assess cardiovascular risk based on lipid profile"""
        risk_factors = []
        risk_level = 'low'
        
        if 'total_cholesterol' in biomarker_data:
            tc = biomarker_data['total_cholesterol']
            if tc >= 240:
                risk_factors.append(f"Total cholesterol {tc} mg/dL is high")
                risk_level = 'moderate'
        
        if 'ldl' in biomarker_data:
            ldl = biomarker_data['ldl']
            if ldl >= 160:
                risk_factors.append(f"LDL cholesterol {ldl} mg/dL is high")
                risk_level = 'moderate'
        
        if 'hdl' in biomarker_data:
            hdl = biomarker_data['hdl']
            if hdl < 40:
                risk_factors.append(f"HDL cholesterol {hdl} mg/dL is low")
                risk_level = 'moderate'
        
        if risk_factors:
            return {
                'condition': 'Cardiovascular Disease',
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'contextual_insights': contextual_knowledge.get('general', [])[:2]
            }
        
        return None
    
    def _assess_thyroid_risk(self, biomarker_data: Dict[str, float], contextual_knowledge: Dict) -> Optional[Dict]:
        """Assess thyroid risk based on TSH levels"""
        if 'tsh' in biomarker_data:
            tsh = biomarker_data['tsh']
            risk_factors = []
            risk_level = 'low'
            
            if tsh > 10:
                risk_factors.append(f"TSH {tsh} mIU/L indicates overt hypothyroidism")
                risk_level = 'high'
            elif tsh > 4.5:
                risk_factors.append(f"TSH {tsh} mIU/L indicates subclinical hypothyroidism")
                risk_level = 'moderate'
            elif tsh < 0.4:
                risk_factors.append(f"TSH {tsh} mIU/L indicates possible hyperthyroidism")
                risk_level = 'moderate'
            
            if risk_factors:
                return {
                    'condition': 'Thyroid Dysfunction',
                    'risk_level': risk_level,
                    'risk_factors': risk_factors,
                    'contextual_insights': contextual_knowledge.get('tsh', [])[:2]
                }
        
        return None
    
    def _assess_inflammation_risk(self, biomarker_data: Dict[str, float], contextual_knowledge: Dict) -> Optional[Dict]:
        """Assess inflammation risk based on CRP and ESR"""
        risk_factors = []
        risk_level = 'low'
        
        if 'crp' in biomarker_data:
            crp = biomarker_data['crp']
            if crp > 3.0:
                risk_factors.append(f"CRP {crp} mg/L indicates elevated inflammation")
                risk_level = 'moderate'
        
        if 'esr' in biomarker_data:
            esr = biomarker_data['esr']
            if esr > 20:
                risk_factors.append(f"ESR {esr} mm/hr indicates elevated inflammation")
                risk_level = 'moderate'
        
        if risk_factors:
            return {
                'condition': 'Inflammation',
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'contextual_insights': contextual_knowledge.get('general', [])[:2]
            }
        
        return None
    
    def _calculate_overall_risk_level(self, risks: List[Dict]) -> str:
        """Calculate overall risk level based on individual risk assessments"""
        if not risks:
            return 'low'
        
        risk_levels = [risk['risk_level'] for risk in risks]
        
        if 'high' in risk_levels:
            return 'high'
        elif 'moderate' in risk_levels:
            return 'moderate'
        else:
            return 'low'
    
    def _identify_critical_findings(self, biomarker_data: Dict[str, float]) -> List[str]:
        """Identify critical findings requiring immediate medical attention"""
        critical_findings = []
        
        # Define critical thresholds
        critical_thresholds = {
            'glucose': 300,  # Very high glucose
            'tsh': 20,       # Very high TSH
            'creatinine': 3.0,  # High creatinine
            'crp': 10.0      # Very high CRP
        }
        
        for biomarker, value in biomarker_data.items():
            if biomarker in critical_thresholds:
                if value >= critical_thresholds[biomarker]:
                    critical_findings.append(f"CRITICAL: {biomarker} level of {value} requires immediate medical attention")
        
        return critical_findings
    
    def _generate_lifestyle_recommendations(self, biomarker_data: Dict[str, float], user_lifestyle: str, contextual_knowledge: Dict) -> List[str]:
        """Generate lifestyle recommendations based on biomarkers"""
        recommendations = []
        
        # General recommendations
        recommendations.append("Maintain a balanced diet rich in fruits, vegetables, and whole grains")
        recommendations.append("Engage in regular physical activity (at least 150 minutes per week)")
        recommendations.append("Maintain a healthy weight")
        recommendations.append("Avoid smoking and limit alcohol consumption")
        recommendations.append("Get adequate sleep (7-9 hours per night)")
        
        # Specific recommendations based on biomarkers
        if 'glucose' in biomarker_data or 'hba1c' in biomarker_data:
            recommendations.append("Limit refined carbohydrates and sugary foods")
            recommendations.append("Monitor carbohydrate intake and consider portion control")
        
        if any(bm in biomarker_data for bm in ['total_cholesterol', 'ldl', 'hdl', 'triglycerides']):
            recommendations.append("Reduce saturated and trans fats in your diet")
            recommendations.append("Increase intake of omega-3 fatty acids")
            recommendations.append("Consider soluble fiber supplements")
        
        if 'tsh' in biomarker_data:
            recommendations.append("Ensure adequate iodine intake through diet")
            recommendations.append("Consider selenium-rich foods (Brazil nuts, fish)")
        
        if 'vitamin_d' in biomarker_data:
            recommendations.append("Get regular sun exposure (15-30 minutes daily)")
            recommendations.append("Consider vitamin D supplementation if deficient")
        
        return recommendations
    
    def _generate_monitoring_recommendations(self, biomarker_data: Dict[str, float], contextual_knowledge: Dict) -> List[str]:
        """Generate monitoring recommendations"""
        recommendations = []
        
        # General monitoring
        recommendations.append("Schedule regular follow-up lab tests as recommended by your healthcare provider")
        recommendations.append("Keep a record of your lab results to track trends over time")
        
        # Specific monitoring based on findings
        if 'glucose' in biomarker_data or 'hba1c' in biomarker_data:
            recommendations.append("Monitor blood glucose levels regularly if recommended by your doctor")
            recommendations.append("Consider HbA1c testing every 3-6 months")
        
        if any(bm in biomarker_data for bm in ['total_cholesterol', 'ldl', 'hdl', 'triglycerides']):
            recommendations.append("Monitor lipid profile every 6-12 months")
        
        if 'tsh' in biomarker_data:
            recommendations.append("Monitor thyroid function tests every 6-12 months")
        
        return recommendations
