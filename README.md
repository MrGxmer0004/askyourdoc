# AskYourDoc - Medical Lab Report Analysis with RAG

A comprehensive AI-powered system for analyzing medical lab reports using Retrieval-Augmented Generation (RAG) workflow. The system combines medical datasets, reference ranges, and contextual knowledge to provide detailed health insights.

## 🏥 Features

- **Lab Report Processing**: Extract biomarker data from PDF and image files using OCR
- **RAG Workflow**: Retrieve relevant contextual knowledge from medical datasets
- **Four Pillars Analysis**: Comprehensive health analysis with structured insights
- **Knowledge Base**: Integrated medical datasets and reference ranges
- **API Endpoints**: RESTful API for easy integration
- **Medical Disclaimer**: Built-in safety measures and medical disclaimers

## 📊 Data Sources

The system uses several medical datasets:

- **Comprehensive Biomarkers Dataset**: 3,000+ records with multiple biomarkers
- **Diabetes/Pre-diabetes Dataset**: 2,000+ records for glucose metabolism analysis
- **Thyroid Dataset**: 1,800+ records for thyroid function assessment
- **Dyslipidemia/CVD Dataset**: 1,800+ records for cardiovascular risk assessment
- **Inflammation Dataset**: 1,800+ records for inflammatory markers
- **Medical Labs Training Data**: 1,000+ records with weak labels

## 🏗️ Architecture

### Core Components

1. **Knowledge Base Manager** (`knowledge_base.py`)
   - Loads and indexes medical datasets
   - Creates embeddings for semantic search
   - Manages reference ranges and abnormality mappings

2. **Lab Report Processor** (`lab_report_processor.py`)
   - Extracts biomarker data from PDF/image files
   - Validates biomarker values
   - Handles OCR for image processing

3. **Health Analyzer** (`health_analyzer.py`)
   - Implements Four Pillars analysis framework
   - Generates contextual insights using RAG
   - Provides actionable recommendations

4. **FastAPI Application** (`main.py`)
   - RESTful API endpoints
   - File upload handling
   - Response formatting

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AskYourDoc
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR** (for image processing)
   - **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

4. **Run the application**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## 📖 API Documentation

### Core Endpoints

#### 1. Analyze Lab Report
```http
POST /analyze/lab-report
Content-Type: multipart/form-data

Parameters:
- file: Lab report file (PDF or image)
- user_symptoms: User-provided symptoms (optional)
- user_lifestyle: User lifestyle information (optional)
```

#### 2. Analyze Biomarkers Directly
```http
POST /analyze/biomarkers
Content-Type: application/json

{
  "biomarker_data": {
    "glucose": 110.0,
    "hba1c": 5.8,
    "tsh": 6.2
  },
  "user_symptoms": "Feeling tired and gaining weight",
  "user_lifestyle": "Desk job, minimal exercise"
}
```

#### 3. Extract Biomarkers Only
```http
POST /extract-biomarkers
Content-Type: multipart/form-data

Parameters:
- file: Lab report file (PDF or image)
```

#### 4. Search Knowledge Base
```http
POST /search-knowledge?query=TSH hypothyroidism&top_k=5
```

#### 5. Get Reference Ranges
```http
GET /reference-ranges
GET /reference-ranges/{biomarker}
```

### Response Format

The analysis response follows the Four Pillars structure:

```json
{
  "success": true,
  "analysis": {
    "disclaimer": "Medical disclaimer text...",
    "pillar_1_biomarker_interpretation": {
      "title": "Interpretation of Key Biomarkers",
      "biomarkers": {
        "glucose": {
          "value": 110.0,
          "reference_range": "70-100 mg/dL",
          "status": "High",
          "interpretation": "Your glucose level is 110.0, which is classified as High...",
          "contextual_insights": [...]
        }
      }
    },
    "pillar_2_symptom_correlation": {
      "title": "Correlation Between Symptoms and Biomarker Trends",
      "correlations": [...],
      "symptom_analysis": {...}
    },
    "pillar_3_predictive_insights": {
      "title": "Predictive Insights on Potential Health Risks",
      "risk_assessments": [...],
      "overall_risk_level": "moderate"
    },
    "pillar_4_actionable_recommendations": {
      "title": "Clear, Actionable Recommendations",
      "immediate_actions": [...],
      "lifestyle_recommendations": [...],
      "monitoring_recommendations": [...],
      "medical_consultation_required": true
    },
    "contextual_knowledge_used": {...}
  }
}
```

## 🧪 Testing

Run the test suite to verify system functionality:

```bash
python test_system.py
```

The test suite includes:
- Knowledge base status verification
- Reference ranges validation
- Biomarker analysis testing
- Knowledge search functionality
- Dataset loading verification

## 🔧 Configuration

### Environment Variables

Create a `.env` file for configuration:

```env
# OpenAI API (if using OpenAI for additional analysis)
OPENAI_API_KEY=your_openai_api_key

# Tesseract path (if not in system PATH)
TESSERACT_CMD=/usr/local/bin/tesseract

# Server configuration
HOST=0.0.0.0
PORT=8000
```

### Customization

1. **Add New Datasets**: Place CSV files in the data directory and update `knowledge_base.py`
2. **Modify Reference Ranges**: Edit `data.txt` and `data (1).txt` files
3. **Custom Biomarker Patterns**: Update regex patterns in `lab_report_processor.py`
4. **Analysis Logic**: Modify analysis methods in `health_analyzer.py`

## 🛡️ Safety and Compliance

### Medical Disclaimer

The system includes comprehensive medical disclaimers and safety measures:

- **No Medical Diagnosis**: All insights are for informational purposes only
- **Professional Consultation Required**: Always recommends consulting healthcare providers
- **Critical Value Alerts**: Identifies values requiring immediate medical attention
- **Risk Stratification**: Provides risk levels but emphasizes professional evaluation

### Data Privacy

- No personal data is stored permanently
- All processing is done in memory
- File uploads are processed and discarded
- No external API calls for sensitive data

## 📈 Performance

- **Knowledge Base**: ~3,000 medical records indexed
- **Embeddings**: Semantic search with sentence transformers
- **Processing Speed**: ~2-5 seconds per analysis
- **Memory Usage**: ~500MB for full knowledge base
- **Concurrent Users**: Supports multiple simultaneous requests

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Important Notes

- **Not for Medical Use**: This system is for educational and research purposes only
- **Professional Consultation**: Always consult qualified healthcare providers
- **Data Accuracy**: Verify all biomarker extractions and interpretations
- **Regular Updates**: Keep medical datasets and reference ranges updated

## 🆘 Support

For issues and questions:
1. Check the test suite results
2. Review the API documentation
3. Check system logs for errors
4. Ensure all dependencies are installed correctly

## 🔮 Future Enhancements

- Integration with electronic health records
- Real-time biomarker monitoring
- Mobile application interface
- Advanced NLP for symptom analysis
- Integration with wearable devices
- Multi-language support
