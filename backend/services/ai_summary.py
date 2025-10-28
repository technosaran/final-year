from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import re
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class AISummaryService:
    def __init__(self):
        """Initialize AI models for summarization and task extraction"""
        try:
            # Use BART for summarization (free, offline)
            self.summarizer = pipeline(
                "summarization", 
                model="facebook/bart-large-cnn",
                device=-1  # Use CPU (free)
            )
            
            # Use sentence transformers for classification
            from sentence_transformers import SentenceTransformer
            self.classifier = SentenceTransformer('all-MiniLM-L6-v2')
            
            logger.info("AI models loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load AI models: {e}")
            self.summarizer = None
            self.classifier = None

    def summarize_text(self, text: str, max_length: int = 150) -> str:
        """Summarize text using BART model"""
        if not self.summarizer or not text.strip():
            return text[:200] + "..." if len(text) > 200 else text
        
        try:
            # Clean and prepare text
            cleaned_text = self._clean_text(text)
            
            if len(cleaned_text) < 50:  # Too short to summarize
                return cleaned_text
            
            # Generate summary
            summary = self.summarizer(
                cleaned_text, 
                max_length=max_length, 
                min_length=30, 
                do_sample=False
            )
            
            return summary[0]['summary_text']
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            return text[:200] + "..." if len(text) > 200 else text

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