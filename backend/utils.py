"""
Utility functions for the AI Productivity Dashboard
"""
import re
import hashlib
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from functools import wraps
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

# Thread pool for CPU-bound tasks
thread_pool = ThreadPoolExecutor(max_workers=4)


def run_in_thread(func):
    """Decorator to run CPU-bound functions in thread pool"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(thread_pool, func, *args, **kwargs)
    return wrapper


def clean_text(text: str) -> str:
    """Clean and normalize text for processing"""
    if not text:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove email headers and signatures
    text = re.sub(r'From:.*?Subject:.*?\n', '', text, flags=re.DOTALL)
    text = re.sub(r'--\s*\n.*', '', text, flags=re.DOTALL)
    
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    return text.strip()


def extract_email_addresses(text: str) -> List[str]:
    """Extract email addresses from text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, text)


def extract_phone_numbers(text: str) -> List[str]:
    """Extract phone numbers from text"""
    phone_pattern = r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
    matches = re.findall(phone_pattern, text)
    return [''.join(match) for match in matches]


def extract_urls(text: str) -> List[str]:
    """Extract URLs from text"""
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.findall(url_pattern, text)


def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate simple text similarity using Jaccard similarity"""
    if not text1 or not text2:
        return 0.0
    
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0


def generate_cache_key(*args) -> str:
    """Generate a cache key from arguments"""
    key_string = '|'.join(str(arg) for arg in args)
    return hashlib.md5(key_string.encode()).hexdigest()


def format_file_size(bytes_size: int) -> str:
    """Format file size in human readable format"""
    if not bytes_size or bytes_size == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while bytes_size >= 1024 and i < len(size_names) - 1:
        bytes_size /= 1024.0
        i += 1
    
    return f"{bytes_size:.1f} {size_names[i]}"


def parse_datetime(date_string: str) -> Optional[datetime]:
    """Parse datetime string with multiple format support"""
    formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    logger.warning(f"Could not parse datetime: {date_string}")
    return None


def is_business_hours(dt: datetime) -> bool:
    """Check if datetime is within business hours (9 AM - 6 PM, Mon-Fri)"""
    return (
        dt.weekday() < 5 and  # Monday = 0, Friday = 4
        9 <= dt.hour < 18
    )


def calculate_productivity_score(
    meetings_today: int,
    focus_blocks: int,
    emails_processed: int,
    tasks_completed: int
) -> int:
    """Calculate productivity score based on various metrics"""
    score = 100
    
    # Penalize too many meetings
    if meetings_today > 6:
        score -= (meetings_today - 6) * 10
    elif meetings_today > 4:
        score -= (meetings_today - 4) * 5
    
    # Reward focus blocks
    score += min(focus_blocks * 15, 30)
    
    # Reward email processing
    score += min(emails_processed * 2, 20)
    
    # Reward task completion
    score += min(tasks_completed * 5, 25)
    
    return max(0, min(100, score))


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:250] + ('.' + ext if ext else '')
    
    return filename


def validate_email(email: str) -> bool:
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def mask_sensitive_data(data: str, mask_char: str = '*') -> str:
    """Mask sensitive data for logging"""
    if not data or len(data) < 4:
        return mask_char * len(data) if data else ""
    
    return data[:2] + mask_char * (len(data) - 4) + data[-2:]


def retry_with_backoff(max_retries: int = 3, backoff_factor: float = 1.0):
    """Decorator for retrying functions with exponential backoff"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    
                    wait_time = backoff_factor * (2 ** attempt)
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
            
        return wrapper
    return decorator


class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[datetime]] = {}
    
    def is_allowed(self, key: str) -> bool:
        """Check if request is allowed for given key"""
        now = datetime.utcnow()
        
        if key not in self.requests:
            self.requests[key] = []
        
        # Remove old requests outside the window
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if now - req_time < timedelta(seconds=self.window_seconds)
        ]
        
        # Check if under limit
        if len(self.requests[key]) < self.max_requests:
            self.requests[key].append(now)
            return True
        
        return False


# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=100, window_seconds=3600)