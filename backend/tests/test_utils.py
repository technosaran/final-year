"""
Tests for utility functions
"""
import pytest
from datetime import datetime

from utils import (
    clean_text, extract_email_addresses, extract_phone_numbers,
    format_file_size, calculate_text_similarity, validate_email,
    sanitize_filename, is_business_hours, calculate_productivity_score
)


class TestTextProcessing:
    """Test text processing utilities"""
    
    def test_clean_text(self):
        """Test text cleaning"""
        html_text = "<p>Hello <b>world</b>!</p>"
        cleaned = clean_text(html_text)
        assert cleaned == "Hello world!"
        
        # Test with None
        assert clean_text(None) == ""
        
        # Test with empty string
        assert clean_text("") == ""
    
    def test_extract_email_addresses(self):
        """Test email extraction"""
        text = "Contact us at support@example.com or admin@test.org"
        emails = extract_email_addresses(text)
        assert "support@example.com" in emails
        assert "admin@test.org" in emails
        assert len(emails) == 2
    
    def test_extract_phone_numbers(self):
        """Test phone number extraction"""
        text = "Call us at (555) 123-4567 or 555.987.6543"
        phones = extract_phone_numbers(text)
        assert len(phones) >= 1
    
    def test_calculate_text_similarity(self):
        """Test text similarity calculation"""
        text1 = "hello world"
        text2 = "hello universe"
        similarity = calculate_text_similarity(text1, text2)
        assert 0 <= similarity <= 1
        
        # Identical texts
        assert calculate_text_similarity(text1, text1) == 1.0
        
        # Empty texts
        assert calculate_text_similarity("", "") == 0.0


class TestFileUtils:
    """Test file-related utilities"""
    
    def test_format_file_size(self):
        """Test file size formatting"""
        assert format_file_size(0) == "0 B"
        assert format_file_size(1024) == "1.0 KB"
        assert format_file_size(1024 * 1024) == "1.0 MB"
        assert format_file_size(1024 * 1024 * 1024) == "1.0 GB"
    
    def test_sanitize_filename(self):
        """Test filename sanitization"""
        dangerous = "file<>name?.txt"
        safe = sanitize_filename(dangerous)
        assert "<" not in safe
        assert ">" not in safe
        assert "?" not in safe
        
        # Test long filename
        long_name = "a" * 300 + ".txt"
        sanitized = sanitize_filename(long_name)
        assert len(sanitized) <= 255


class TestValidation:
    """Test validation utilities"""
    
    def test_validate_email(self):
        """Test email validation"""
        assert validate_email("test@example.com") is True
        assert validate_email("invalid-email") is False
        assert validate_email("") is False
        assert validate_email("test@") is False
    
    def test_is_business_hours(self):
        """Test business hours check"""
        # Monday 10 AM
        monday_10am = datetime(2024, 1, 1, 10, 0)  # Monday
        assert is_business_hours(monday_10am) is True
        
        # Saturday 10 AM
        saturday_10am = datetime(2024, 1, 6, 10, 0)  # Saturday
        assert is_business_hours(saturday_10am) is False
        
        # Monday 8 PM
        monday_8pm = datetime(2024, 1, 1, 20, 0)  # Monday
        assert is_business_hours(monday_8pm) is False


class TestProductivityScore:
    """Test productivity score calculation"""
    
    def test_calculate_productivity_score(self):
        """Test productivity score calculation"""
        # Perfect day
        score = calculate_productivity_score(
            meetings_today=3,
            focus_blocks=2,
            emails_processed=10,
            tasks_completed=5
        )
        assert 80 <= score <= 100
        
        # Overloaded day
        score = calculate_productivity_score(
            meetings_today=10,
            focus_blocks=0,
            emails_processed=0,
            tasks_completed=0
        )
        assert score < 50
        
        # Minimum score
        score = calculate_productivity_score(0, 0, 0, 0)
        assert score >= 0
        
        # Maximum score
        score = calculate_productivity_score(0, 2, 10, 5)
        assert score <= 100