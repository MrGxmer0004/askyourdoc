"""
Demo example showing how to use the AskYourDoc system
"""

import json
from knowledge_base import MedicalKnowledgeBase
from lab_report_processor import LabReportProcessor
from health_analyzer import HealthAnalyzer

def demo_biomarker_analysis():
    """Demonstrate biomarker analysis without file upload"""
    print("🏥 AskYourDoc Demo - Biomarker Analysis")
    print("=" * 50)
    
    # Initialize components
    print("📊 Initializing Knowledge Base...")
    kb = MedicalKnowledgeBase()
    kb.load_datasets()
    kb.load_reference_data()
    kb.initialize_embeddings()
    
    print("🔬 Initializing Health Analyzer...")
    analyzer = HealthAnalyzer(kb)
    
    # Sample biomarker data
    sample_biomarkers = {
        "glucose": 110.0,
        "hba1c": 5.8,
        "total_cholesterol": 220.0,
        "ldl": 140.0,
        "hdl": 45.0,
        "tsh": 6.2,
        "crp": 2.5,
        "vitamin_d": 18.0
    }
    
    # Sample user data
    user_symptoms = """
    I've been feeling very tired lately and have gained about 10 pounds over the past 3 months. 
    I also experience joint pain, especially in my knees and hands. I feel cold more often than usual 
    and have noticed my hair is thinning. I'm having trouble concentrating at work.
    """
    
    user_lifestyle = """
    I work a desk job and sit for 8-10 hours a day. I don't exercise regularly, maybe once a week 
    if I'm lucky. My diet consists mostly of processed foods, takeout, and I drink 2-3 cups of coffee daily. 
    I get about 6 hours of sleep per night and feel stressed most of the time.
    """
    
    print(f"\n🧪 Sample Biomarker Data:")
    for biomarker, value in sample_biomarkers.items():
        print(f"  - {biomarker}: {value}")
    
    print(f"\n👤 User Symptoms: {user_symptoms.strip()}")
    print(f"\n🏃 User Lifestyle: {user_lifestyle.strip()}")
    
    # Perform analysis
    print(f"\n🔍 Performing Health Analysis...")
    analysis = analyzer.analyze_health_report(
        biomarker_data=sample_biomarkers,
        user_symptoms=user_symptoms,
        user_lifestyle=user_lifestyle
    )
    
    # Display results
    print(f"\n📋 ANALYSIS RESULTS")
    print("=" * 50)
    
    # Pillar 1: Biomarker Interpretation
    print(f"\n1️⃣ {analysis['pillar_1_biomarker_interpretation']['title']}")
    print("-" * 40)
    for biomarker, data in analysis['pillar_1_biomarker_interpretation']['biomarkers'].items():
        print(f"• {biomarker.upper()}: {data['value']} ({data['status']})")
        print(f"  Reference: {data['reference_range']}")
        print(f"  Interpretation: {data['interpretation']}")
        print()
    
    # Pillar 2: Symptom Correlation
    print(f"\n2️⃣ {analysis['pillar_2_symptom_correlation']['title']}")
    print("-" * 40)
    if analysis['pillar_2_symptom_correlation']['correlations']:
        for correlation in analysis['pillar_2_symptom_correlation']['correlations']:
            print(f"• {correlation['explanation']}")
    else:
        print("No specific correlations found between symptoms and biomarkers.")
    
    # Pillar 3: Predictive Insights
    print(f"\n3️⃣ {analysis['pillar_3_predictive_insights']['title']}")
    print("-" * 40)
    print(f"Overall Risk Level: {analysis['pillar_3_predictive_insights']['overall_risk_level'].upper()}")
    
    for risk in analysis['pillar_3_predictive_insights']['risk_assessments']:
        print(f"\n• {risk['condition']} Risk: {risk['risk_level'].upper()}")
        for factor in risk['risk_factors']:
            print(f"  - {factor}")
    
    # Pillar 4: Recommendations
    print(f"\n4️⃣ {analysis['pillar_4_actionable_recommendations']['title']}")
    print("-" * 40)
    
    if analysis['pillar_4_actionable_recommendations']['medical_consultation_required']:
        print("🚨 MEDICAL CONSULTATION REQUIRED")
        print("Immediate Actions:")
        for action in analysis['pillar_4_actionable_recommendations']['immediate_actions']:
            print(f"  - {action}")
        print()
    
    print("Lifestyle Recommendations:")
    for rec in analysis['pillar_4_actionable_recommendations']['lifestyle_recommendations'][:5]:
        print(f"  • {rec}")
    
    print("\nMonitoring Recommendations:")
    for rec in analysis['pillar_4_actionable_recommendations']['monitoring_recommendations'][:3]:
        print(f"  • {rec}")
    
    # Contextual Knowledge Used
    print(f"\n🧠 CONTEXTUAL KNOWLEDGE USED")
    print("-" * 40)
    total_insights = 0
    for biomarker, insights in analysis['contextual_knowledge_used'].items():
        if biomarker != 'general' and insights:
            total_insights += len(insights)
            print(f"• {biomarker}: {len(insights)} insights")
    
    print(f"• General: {len(analysis['contextual_knowledge_used'].get('general', []))} insights")
    print(f"Total contextual insights used: {total_insights + len(analysis['contextual_knowledge_used'].get('general', []))}")
    
    return analysis

def demo_knowledge_search():
    """Demonstrate knowledge base search functionality"""
    print(f"\n🔍 KNOWLEDGE BASE SEARCH DEMO")
    print("=" * 50)
    
    # Initialize knowledge base
    kb = MedicalKnowledgeBase()
    kb.load_datasets()
    kb.load_reference_data()
    kb.initialize_embeddings()
    
    # Test queries
    queries = [
        "TSH hypothyroidism symptoms",
        "glucose diabetes risk factors",
        "cholesterol cardiovascular disease",
        "vitamin D deficiency effects",
        "inflammation markers CRP"
    ]
    
    for query in queries:
        print(f"\n🔎 Query: '{query}'")
        results = kb.retrieve_contextual_knowledge(query, top_k=3)
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result['text'][:100]}...")
                print(f"     Type: {result['type']}, Score: {result['relevance_score']:.3f}")
        else:
            print("  No results found")

def demo_reference_ranges():
    """Demonstrate reference ranges functionality"""
    print(f"\n📋 REFERENCE RANGES DEMO")
    print("=" * 50)
    
    # Initialize knowledge base
    kb = MedicalKnowledgeBase()
    kb.load_datasets()
    kb.load_reference_data()
    
    # Show some reference ranges
    biomarkers = ["Hemoglobin", "TSH", "LDL Cholestrol", "Vitamin D"]
    
    for biomarker in biomarkers:
        range_info = kb.get_biomarker_reference_range(biomarker)
        if range_info:
            print(f"• {biomarker}: {range_info}")
        else:
            print(f"• {biomarker}: Not found")

if __name__ == "__main__":
    print("🚀 AskYourDoc System Demo")
    print("This demo shows the core functionality without requiring a server")
    print()
    
    try:
        # Run demos
        demo_reference_ranges()
        demo_knowledge_search()
        demo_biomarker_analysis()
        
        print(f"\n✅ Demo completed successfully!")
        print(f"\nTo run the full API server:")
        print(f"  python main.py")
        print(f"\nTo run the test suite:")
        print(f"  python test_system.py")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print(f"Make sure all dependencies are installed:")
        print(f"  pip install -r requirements.txt")
