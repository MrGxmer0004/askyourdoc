"""
Knowledge Base Manager for Medical Lab Report Analysis
Handles loading, indexing, and retrieval of medical datasets and reference ranges
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import os

class MedicalKnowledgeBase:
    def __init__(self, data_dir: str = "."):
        self.data_dir = Path(data_dir)
        self.datasets = {}
        self.reference_ranges = {}
        self.abnormalities_mapping = {}
        self.embedding_model = None
        self.vector_index = None
        self.knowledge_embeddings = None
        self.knowledge_texts = []
        
    def load_datasets(self):
        """Load all medical datasets from CSV files"""
        dataset_files = {
            'comprehensive': 'comprehensive_biomarkers_dataset.csv',
            'diabetes': 'diabetes_prediabetes_dataset.csv',
            'thyroid': 'thyroid_hypothyroid_dataset.csv',
            'dyslipidemia': 'dyslipidemia_cvd_dataset.csv',
            'inflammation': 'inflammation_dataset.csv',
            'medical_labs': 'medical_labs_training_weaklabels.csv'
        }
        
        for name, filename in dataset_files.items():
            filepath = self.data_dir / filename
            if filepath.exists():
                self.datasets[name] = pd.read_csv(filepath)
                print(f"Loaded {name} dataset: {len(self.datasets[name])} records")
            else:
                print(f"Warning: {filename} not found")
    
    def load_reference_data(self):
        """Load reference ranges and abnormality mappings from text files"""
        # Load reference ranges from data.txt
        data_file = self.data_dir / "data.txt"
        if data_file.exists():
            with open(data_file, 'r', encoding='utf-8') as f:
                content = f.read()
                self._parse_reference_ranges(content)
        
        # Load abnormalities mapping from data (1).txt
        data1_file = self.data_dir / "data (1).txt"
        if data1_file.exists():
            with open(data1_file, 'r', encoding='utf-8') as f:
                content = f.read()
                self._parse_abnormalities_mapping(content)
    
    def _parse_reference_ranges(self, content: str):
        """Parse reference ranges from data.txt content"""
        lines = content.split('\n')
        for line in lines:
            if ':' in line and '"' in line:
                # Extract key-value pairs
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip().strip('"')
                    value = parts[1].strip().strip('",')
                    self.reference_ranges[key] = value
    
    def _parse_abnormalities_mapping(self, content: str):
        """Parse abnormalities mapping from data (1).txt content"""
        lines = content.split('\n')
        current_abnormality = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('("') and line.endswith(')'):
                # Parse tuple format: ("abnormality", "condition", "prevalence")
                try:
                    # Simple parsing for the tuple format
                    if line.startswith('("') and '", "' in line:
                        parts = line[2:-1].split('", "')
                        if len(parts) >= 2:
                            abnormality = parts[0]
                            condition = parts[1]
                            prevalence = parts[2] if len(parts) > 2 else ""
                            
                            if abnormality not in self.abnormalities_mapping:
                                self.abnormalities_mapping[abnormality] = []
                            
                            self.abnormalities_mapping[abnormality].append({
                                'condition': condition,
                                'prevalence': prevalence
                            })
                except:
                    continue
    
    def initialize_embeddings(self):
        """Initialize sentence transformer model and create embeddings for knowledge base"""
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self._create_knowledge_embeddings()
    
    def _create_knowledge_embeddings(self):
        """Create embeddings for all knowledge base content"""
        self.knowledge_texts = []
        
        # Add reference ranges
        for biomarker, range_info in self.reference_ranges.items():
            text = f"Reference range for {biomarker}: {range_info}"
            self.knowledge_texts.append({
                'text': text,
                'type': 'reference_range',
                'biomarker': biomarker,
                'source': 'reference_ranges'
            })
        
        # Add abnormalities mapping
        for abnormality, conditions in self.abnormalities_mapping.items():
            for condition_info in conditions:
                text = f"Abnormality {abnormality} is associated with {condition_info['condition']}. Prevalence: {condition_info['prevalence']}"
                self.knowledge_texts.append({
                    'text': text,
                    'type': 'abnormality_mapping',
                    'abnormality': abnormality,
                    'condition': condition_info['condition'],
                    'source': 'abnormalities_mapping'
                })
        
        # Add dataset insights
        self._add_dataset_insights()
        
        # Create embeddings
        texts_only = [item['text'] for item in self.knowledge_texts]
        self.knowledge_embeddings = self.embedding_model.encode(texts_only)
        
        # Create FAISS index
        dimension = self.knowledge_embeddings.shape[1]
        self.vector_index = faiss.IndexFlatIP(dimension)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(self.knowledge_embeddings)
        self.vector_index.add(self.knowledge_embeddings)
    
    def _add_dataset_insights(self):
        """Add statistical insights from datasets"""
        for dataset_name, df in self.datasets.items():
            if dataset_name == 'comprehensive':
                self._add_comprehensive_insights(df)
            elif dataset_name == 'diabetes':
                self._add_diabetes_insights(df)
            elif dataset_name == 'thyroid':
                self._add_thyroid_insights(df)
            elif dataset_name == 'dyslipidemia':
                self._add_dyslipidemia_insights(df)
            elif dataset_name == 'inflammation':
                self._add_inflammation_insights(df)
    
    def _add_comprehensive_insights(self, df: pd.DataFrame):
        """Add insights from comprehensive biomarkers dataset"""
        # TSH insights
        if 'tsh_uIU_mL' in df.columns:
            tsh_data = df['tsh_uIU_mL'].dropna()
            if len(tsh_data) > 0:
                tsh_high = tsh_data[tsh_data > 4.5]
                if len(tsh_high) > 0:
                    text = f"From comprehensive dataset: {len(tsh_high)}/{len(tsh_data)} patients have TSH > 4.5 mIU/L, indicating potential hypothyroidism"
                    self.knowledge_texts.append({
                        'text': text,
                        'type': 'dataset_insight',
                        'biomarker': 'TSH',
                        'threshold': '4.5',
                        'source': 'comprehensive_dataset'
                    })
        
        # HbA1c insights
        if 'hba1c_percent' in df.columns:
            hba1c_data = df['hba1c_percent'].dropna()
            if len(hba1c_data) > 0:
                prediabetes = hba1c_data[(hba1c_data >= 5.7) & (hba1c_data < 6.5)]
                diabetes = hba1c_data[hba1c_data >= 6.5]
                if len(prediabetes) > 0:
                    text = f"From comprehensive dataset: {len(prediabetes)}/{len(hba1c_data)} patients have HbA1c 5.7-6.4%, indicating prediabetes"
                    self.knowledge_texts.append({
                        'text': text,
                        'type': 'dataset_insight',
                        'biomarker': 'HbA1c',
                        'range': '5.7-6.4',
                        'source': 'comprehensive_dataset'
                    })
    
    def _add_diabetes_insights(self, df: pd.DataFrame):
        """Add insights from diabetes dataset"""
        if 'hba1c_percent' in df.columns:
            hba1c_data = df['hba1c_percent'].dropna()
            if len(hba1c_data) > 0:
                prediabetes_count = len(df[df['label_prediabetes'] == 1])
                diabetes_count = len(df[df['label_diabetes'] == 1])
                text = f"From diabetes dataset: {prediabetes_count} patients with prediabetes, {diabetes_count} with diabetes out of {len(df)} total"
                self.knowledge_texts.append({
                    'text': text,
                    'type': 'dataset_insight',
                    'biomarker': 'HbA1c',
                    'source': 'diabetes_dataset'
                })
    
    def _add_thyroid_insights(self, df: pd.DataFrame):
        """Add insights from thyroid dataset"""
        if 'tsh_uIU_mL' in df.columns:
            hypothyroid_count = len(df[df['label_hypothyroid'] == 1])
            text = f"From thyroid dataset: {hypothyroid_count}/{len(df)} patients diagnosed with hypothyroidism"
            self.knowledge_texts.append({
                'text': text,
                'type': 'dataset_insight',
                'biomarker': 'TSH',
                'source': 'thyroid_dataset'
            })
    
    def _add_dyslipidemia_insights(self, df: pd.DataFrame):
        """Add insights from dyslipidemia dataset"""
        if 'label_dyslipidemia' in df.columns:
            dyslipidemia_count = len(df[df['label_dyslipidemia'] == 1])
            text = f"From dyslipidemia dataset: {dyslipidemia_count}/{len(df)} patients diagnosed with dyslipidemia"
            self.knowledge_texts.append({
                'text': text,
                'type': 'dataset_insight',
                'biomarker': 'Lipid Profile',
                'source': 'dyslipidemia_dataset'
            })
    
    def _add_inflammation_insights(self, df: pd.DataFrame):
        """Add insights from inflammation dataset"""
        if 'label_inflammation' in df.columns:
            inflammation_count = len(df[df['label_inflammation'] == 1])
            text = f"From inflammation dataset: {inflammation_count}/{len(df)} patients show signs of inflammation"
            self.knowledge_texts.append({
                'text': text,
                'type': 'dataset_insight',
                'biomarker': 'CRP/ESR',
                'source': 'inflammation_dataset'
            })
    
    def retrieve_contextual_knowledge(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve relevant contextual knowledge based on query"""
        if self.vector_index is None or self.embedding_model is None:
            return []
        
        # Encode query
        query_embedding = self.embedding_model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.vector_index.search(query_embedding, top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.knowledge_texts):
                result = self.knowledge_texts[idx].copy()
                result['relevance_score'] = float(score)
                results.append(result)
        
        return results
    
    def get_biomarker_reference_range(self, biomarker: str) -> Optional[str]:
        """Get reference range for a specific biomarker"""
        return self.reference_ranges.get(biomarker)
    
    def get_abnormalities_for_biomarker(self, biomarker: str) -> List[Dict]:
        """Get possible abnormalities and conditions for a biomarker"""
        results = []
        for abnormality, conditions in self.abnormalities_mapping.items():
            if biomarker.lower() in abnormality.lower():
                results.extend(conditions)
        return results
    
    def analyze_biomarker_values(self, biomarker_values: Dict[str, float]) -> Dict[str, Any]:
        """Analyze biomarker values against reference ranges and datasets"""
        analysis = {}
        
        for biomarker, value in biomarker_values.items():
            if biomarker in self.reference_ranges:
                range_info = self.reference_ranges[biomarker]
                analysis[biomarker] = {
                    'value': value,
                    'reference_range': range_info,
                    'status': self._classify_value(value, range_info),
                    'contextual_knowledge': self.retrieve_contextual_knowledge(f"{biomarker} {value}", top_k=3)
                }
        
        return analysis
    
    def _classify_value(self, value: float, range_info: str) -> str:
        """Classify biomarker value as Normal, High, or Low based on reference range"""
        # Simple parsing of reference ranges
        # This is a basic implementation - in production, you'd want more sophisticated parsing
        try:
            if '<' in range_info:
                threshold = float(range_info.split('<')[1].split()[0])
                return "High" if value >= threshold else "Normal"
            elif '>' in range_info:
                threshold = float(range_info.split('>')[1].split()[0])
                return "Low" if value <= threshold else "Normal"
            elif '-' in range_info:
                parts = range_info.split('-')
                if len(parts) == 2:
                    low = float(parts[0].split()[-1])
                    high = float(parts[1].split()[0])
                    if value < low:
                        return "Low"
                    elif value > high:
                        return "High"
                    else:
                        return "Normal"
        except:
            pass
        
        return "Unknown"
    
    def save_knowledge_base(self, filepath: str):
        """Save the knowledge base to disk"""
        kb_data = {
            'reference_ranges': self.reference_ranges,
            'abnormalities_mapping': self.abnormalities_mapping,
            'knowledge_texts': self.knowledge_texts
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(kb_data, f)
        
        # Save embeddings separately
        embeddings_file = filepath.replace('.pkl', '_embeddings.npy')
        np.save(embeddings_file, self.knowledge_embeddings)
    
    def load_knowledge_base(self, filepath: str):
        """Load the knowledge base from disk"""
        with open(filepath, 'rb') as f:
            kb_data = pickle.load(f)
        
        self.reference_ranges = kb_data['reference_ranges']
        self.abnormalities_mapping = kb_data['abnormalities_mapping']
        self.knowledge_texts = kb_data['knowledge_texts']
        
        # Load embeddings
        embeddings_file = filepath.replace('.pkl', '_embeddings.npy')
        if os.path.exists(embeddings_file):
            self.knowledge_embeddings = np.load(embeddings_file)
            
            # Recreate FAISS index
            dimension = self.knowledge_embeddings.shape[1]
            self.vector_index = faiss.IndexFlatIP(dimension)
            faiss.normalize_L2(self.knowledge_embeddings)
            self.vector_index.add(self.knowledge_embeddings)
