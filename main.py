"""
FastAPI application for AskYourDoc - Medical Lab Report Analysis with RAG
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import base64
import json
import os
from pathlib import Path

from knowledge_base import MedicalKnowledgeBase
from lab_report_processor import LabReportProcessor
from health_analyzer import HealthAnalyzer

# Initialize FastAPI app
app = FastAPI(
    title="AskYourDoc - Medical Lab Report Analysis",
    description="AI-powered medical lab report analysis with RAG workflow",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for components
knowledge_base = None
lab_processor = None
health_analyzer = None

# Pydantic models
class HealthAnalysisRequest(BaseModel):
    biomarker_data: Dict[str, float]
    user_symptoms: Optional[str] = ""
    user_lifestyle: Optional[str] = ""

class HealthAnalysisResponse(BaseModel):
    success: bool
    analysis: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class KnowledgeBaseStatus(BaseModel):
    loaded: bool
    datasets_count: int
    reference_ranges_count: int
    abnormalities_count: int
    embeddings_ready: bool

@app.on_event("startup")
async def startup_event():
    """Initialize the knowledge base and other components on startup"""
    global knowledge_base, lab_processor, health_analyzer
    
    try:
        # Initialize knowledge base
        knowledge_base = MedicalKnowledgeBase()
        knowledge_base.load_datasets()
        knowledge_base.load_reference_data()
        knowledge_base.initialize_embeddings()
        
        # Initialize other components
        lab_processor = LabReportProcessor()
        health_analyzer = HealthAnalyzer(knowledge_base)
        
        print("✅ AskYourDoc system initialized successfully")
        print(f"📊 Loaded {len(knowledge_base.datasets)} datasets")
        print(f"📋 Loaded {len(knowledge_base.reference_ranges)} reference ranges")
        print(f"🔍 Loaded {len(knowledge_base.abnormalities_mapping)} abnormality mappings")
        print(f"🧠 Created {len(knowledge_base.knowledge_texts)} knowledge embeddings")
        
    except Exception as e:
        print(f"❌ Error initializing system: {e}")
        raise e

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AskYourDoc - Medical Lab Report Analysis API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

@app.get("/knowledge-base/status", response_model=KnowledgeBaseStatus)
async def get_knowledge_base_status():
    """Get knowledge base status"""
    if not knowledge_base:
        raise HTTPException(status_code=503, detail="Knowledge base not initialized")
    
    return KnowledgeBaseStatus(
        loaded=True,
        datasets_count=len(knowledge_base.datasets),
        reference_ranges_count=len(knowledge_base.reference_ranges),
        abnormalities_count=len(knowledge_base.abnormalities_mapping),
        embeddings_ready=knowledge_base.vector_index is not None
    )

@app.post("/analyze/lab-report")
async def analyze_lab_report(
    file: UploadFile = File(...),
    user_symptoms: str = Form(""),
    user_lifestyle: str = Form("")
):
    """
    Analyze a lab report file (PDF or image) and generate health insights
    """
    if not lab_processor or not health_analyzer:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Determine file type
        file_extension = Path(file.filename).suffix.lower()
        
        # Process the file
        if file_extension == '.pdf':
            biomarker_data = lab_processor.process_pdf(file_content)
        elif file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
            biomarker_data = lab_processor.process_image(file_content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        if not biomarker_data:
            raise HTTPException(status_code=400, detail="No biomarker data found in the file")
        
        # Validate biomarker values
        validated_data = lab_processor.validate_biomarker_values(biomarker_data)
        
        # Perform health analysis
        analysis = health_analyzer.analyze_health_report(
            biomarker_data=biomarker_data,
            user_symptoms=user_symptoms,
            user_lifestyle=user_lifestyle
        )
        
        return JSONResponse(content={
            "success": True,
            "analysis": analysis,
            "extracted_biomarkers": biomarker_data,
            "validation": validated_data
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing lab report: {str(e)}")

@app.post("/analyze/biomarkers", response_model=HealthAnalysisResponse)
async def analyze_biomarkers(request: HealthAnalysisRequest):
    """
    Analyze biomarker data directly without file upload
    """
    if not health_analyzer:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        # Perform health analysis
        analysis = health_analyzer.analyze_health_report(
            biomarker_data=request.biomarker_data,
            user_symptoms=request.user_symptoms or "",
            user_lifestyle=request.user_lifestyle or ""
        )
        
        return HealthAnalysisResponse(
            success=True,
            analysis=analysis
        )
        
    except Exception as e:
        return HealthAnalysisResponse(
            success=False,
            error=f"Error analyzing biomarkers: {str(e)}"
        )

@app.post("/extract-biomarkers")
async def extract_biomarkers(file: UploadFile = File(...)):
    """
    Extract biomarker data from a lab report file without analysis
    """
    if not lab_processor:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Determine file type
        file_extension = Path(file.filename).suffix.lower()
        
        # Process the file
        if file_extension == '.pdf':
            biomarker_data = lab_processor.process_pdf(file_content)
        elif file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
            biomarker_data = lab_processor.process_image(file_content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Validate biomarker values
        validated_data = lab_processor.validate_biomarker_values(biomarker_data)
        
        return JSONResponse(content={
            "success": True,
            "biomarkers": biomarker_data,
            "validation": validated_data,
            "summary": lab_processor.get_extraction_summary(biomarker_data)
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting biomarkers: {str(e)}")

@app.get("/reference-ranges")
async def get_reference_ranges():
    """Get all available reference ranges"""
    if not knowledge_base:
        raise HTTPException(status_code=503, detail="Knowledge base not initialized")
    
    return {
        "reference_ranges": knowledge_base.reference_ranges,
        "abnormalities_mapping": knowledge_base.abnormalities_mapping
    }

@app.get("/reference-ranges/{biomarker}")
async def get_biomarker_reference_range(biomarker: str):
    """Get reference range for a specific biomarker"""
    if not knowledge_base:
        raise HTTPException(status_code=503, detail="Knowledge base not initialized")
    
    reference_range = knowledge_base.get_biomarker_reference_range(biomarker)
    if not reference_range:
        raise HTTPException(status_code=404, detail=f"Reference range not found for {biomarker}")
    
    return {
        "biomarker": biomarker,
        "reference_range": reference_range
    }

@app.post("/search-knowledge")
async def search_knowledge(query: str, top_k: int = 5):
    """Search the knowledge base for relevant information"""
    if not knowledge_base:
        raise HTTPException(status_code=503, detail="Knowledge base not initialized")
    
    try:
        results = knowledge_base.retrieve_contextual_knowledge(query, top_k)
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching knowledge base: {str(e)}")

@app.get("/datasets")
async def get_datasets():
    """Get information about loaded datasets"""
    if not knowledge_base:
        raise HTTPException(status_code=503, detail="Knowledge base not initialized")
    
    dataset_info = {}
    for name, df in knowledge_base.datasets.items():
        dataset_info[name] = {
            "rows": len(df),
            "columns": list(df.columns),
            "sample_data": df.head(3).to_dict('records') if len(df) > 0 else []
        }
    
    return {
        "datasets": dataset_info,
        "total_datasets": len(knowledge_base.datasets)
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run('main:app', host='0.0.0.0', port=port, log_level='info')
