"""
AI Summary Service - Production-ready ML service with async support
"""
import asyncio
import time
from typing import List, Dict, Optional, Tuple
import logging
import re
from concurrent.futures import ThreadPoolExecutor

from config import settings
from utils import run_in_thread, clean_text
from schemas import EmailTask, SummarizationResponse, TaskExtractionResponse

logger = logging.getLogger(__name__)

# Thread pool for CPU-bound ML operations
ml_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="ml_worker")


class AISummaryService:
    """Production AI service with proper error handling and async support"""
    
    def __init__(self):
        """Initialize AI models for summarization and task extraction"""
        self.summarizer = None
        self.classifier = None
        self._models_loaded = False
        self._loading = False
        
        # Start loading models in background
        asyncio.create_task(self._load_models_async())
    
    async def _load_models_async(self):
        """Load AI models asynchronously to avoid blocking startup"""
        if self._loading or self._models_loaded:
            return
        
        self._loading = True
        try:
            logger.info("Loading AI models in background...")
            
            # Load models in thread pool to avoid blocking
            await asyncio.get_event_loop().run_in_executor(
                ml_executor, self._load_models_sync
            )
            
            self._models_loaded = True
            logger.info("AI models loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load AI models: {e}")
            # Continue without models - graceful degradation
        finally:
            self._loading = False
    
    def _load_models_sync(self):
        """Synchronous model loading (runs in thread pool)"""
        try:
            # Use BART for summarization (free, offline)
            from transformers import pipeline
            self.summarizer = pipeline(
                "summarization", 
                model=settings.summarization_model,
                device=-1,  # Use CPU (free)
                model_kwargs={"cache_dir": settings.ai_model_cache_dir}
            )
            
            # Use sentence transformers for classification
            from sentence_transformers import SentenceTransformer
            self.classifier = SentenceTransformer(
                settings.classification_model,
                cache_folder=settings.ai_model_cache_dir
            )
            
        except ImportError as e:
            logger.error(f"Missing ML dependencies: {e}")
            raise
        except Exception as e:
            logger.error(f"Model loading error: {e}")
            raise

    @run_in_thread
    def _summarize_sync(self, text: str, max_length: int, min_length: int) -> Dict:
        """Synchronous summarization (runs in thread pool)"""
        if not self.summarizer:
            raise RuntimeError("Summarizer model not loaded")
        
        return self.summarizer(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )
    
    async def summarize_text(self, text: str, max_length: int = 150) -> SummarizationResponse:
        """Summarize text using BART model with async support"""
        start_time = time.time()
        
        if not text or not text.strip():
            return SummarizationResponse(
                summary="",
                confidence_score=0.0,
                processing_time=0.0
            )
        
        try:
            # Clean and prepare text
            cleaned_text = clean_text(text)
            
            if len(cleaned_text) < 50:  # Too short to summarize
                return SummarizationResponse(
                    summary=cleaned_text,
                    confidence_score=1.0,
                    processing_time=time.time() - start_time
                )
            
            # Ensure models are loaded
            if not self._models_loaded:
                await self._load_models_async()
            
            if not self.summarizer:
                # Graceful fallback
                fallback_summary = cleaned_text[:max_length] + "..." if len(cleaned_text) > max_length else cleaned_text
                return SummarizationResponse(
                    summary=fallback_summary,
                    confidence_score=0.5,
                    processing_time=time.time() - start_time
                )
            
            # Generate summary asynchronously
            min_length = min(30, len(cleaned_text) // 4)
            result = await self._summarize_sync(cleaned_text, max_length, min_length)
            
            summary_text = result[0]['summary_text']
            confidence = result[0].get('score', 0.8)  # Default confidence
            
            return SummarizationResponse(
                summary=summary_text,
                confidence_score=confidence,
                processing_time=time.time() - start_time
            )
            
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            # Graceful fallback
            fallback_summary = text[:max_length] + "..." if len(text) > max_length else text
            return SummarizationResponse(
                summary=fallback_summary,
                confidence_score=0.0,
                processing_time=time.time() - start_time
            )

    def extract_tasks(self, text: str) -> List[str]:
        """Extract actionable tasks from text"""
        tasks = []
        
        # Task indicators
        task_patterns = [
            r'(?:please|can you|could you|need to|have to|must|should)\s+([^.!?]+)',
            r'(?:action item|todo|task|follow up):\s*([^.!?]+)',
            r'(?:by|before|until)\s+\w+day[^.!?]*',
            r'(?:schedule|book|arrange|set up|organize)\s+([^.!?]+)',
            r'(?:review|check|verify|confirm|update)\s+([^.!?]+)'
        ]
        
        for pattern in task_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                task = match.strip()
                if len(task) > 10 and task not in tasks:
                    tasks.append(task)
        
        return tasks[:5]  # Return top 5 tasks

    def categorize_file(self, filename: str, content_preview: str = "") -> str:
        """Categorize files based on name and content"""
        filename_lower = filename.lower()
        
        # Simple rule-based categorization
        if any(ext in filename_lower for ext in ['.pdf', '.doc', '.docx']):
            if any(word in filename_lower for word in ['resume', 'cv']):
                return 'Resume/CV'
            elif any(word in filename_lower for word in ['report', 'analysis']):
                return 'Report'
            elif any(word in filename_lower for word in ['contract', 'agreement']):
                return 'Legal Document'
            else:
                return 'Document'
        
        elif any(ext in filename_lower for ext in ['.jpg', '.png', '.gif', '.jpeg']):
            return 'Image'
        
        elif any(ext in filename_lower for ext in ['.xlsx', '.xls', '.csv']):
            return 'Spreadsheet'
        
        elif any(ext in filename_lower for ext in ['.ppt', '.pptx']):
            return 'Presentation'
        
        else:
            return 'Other'

    def analyze_calendar_efficiency(self, events: List[Dict]) -> Dict:
        """Analyze calendar for efficiency insights"""
        if not events:
            return {"total_meetings": 0, "suggestions": []}
        
        total_meetings = len(events)
        meeting_hours = 0
        gaps = []
        
        # Simple analysis
        for event in events:
            # Assume 1 hour per meeting if duration not specified
            meeting_hours += 1
        
        suggestions = []
        
        if meeting_hours > 6:
            suggestions.append("Consider reducing meeting time - you have over 6 hours of meetings")
        
        if total_meetings > 8:
            suggestions.append("High meeting density - consider batching similar meetings")
        
        return {
            "total_meetings": total_meetings,
            "estimated_meeting_hours": meeting_hours,
            "suggestions": suggestions
        }

    def _clean_text(self, text: str) -> str:
        """Clean text for processing"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove email headers and signatures
        text = re.sub(r'From:.*?Subject:.*?\n', '', text, flags=re.DOTALL)
        text = re.sub(r'--\s*\n.*', '', text, flags=re.DOTALL)
        
        return text.strip()

# Global instance
ai_service = AISummaryService()