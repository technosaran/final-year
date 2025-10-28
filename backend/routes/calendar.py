from fastapi import APIRouter, HTTPException, Header
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from services.ai_summary import ai_service
from datetime import datetime, timedelta
from typing import List, Dict

router = APIRouter()

def get_calendar_service(access_token: str):
    """Create Calendar service with access token"""
    credentials = Credentials(token=access_token)
    return build('calendar', 'v3', credentials=credentials)

@router.get("/events")
async def get_events(
    authorization: str = Header(...),
    days_ahead: int = 7
):
    """Fetch upcoming calendar events with AI insights"""
    try:
        access_token = authorization.replace("Bearer ", "")
        service = get_calendar_service(access_token)
        
        # Calculate time range
        now = datetime.utcnow()
        time_min = now.isoformat() + 'Z'
        time_max = (now + timedelta(days=days_ahead)).isoformat() + 'Z'
        
        # Get events
        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            maxResults=50,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        processed_events = []
        
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            processed_events.append({
                'id': event['id'],
                'summary': event.get('summary', 'No Title'),
                'description': event.get('description', ''),
                'start': start,
                'end': end,
                'location': event.get('location', ''),
                'attendees': len(event.get('attendees', [])),
                'meeting_link': extract_meeting_link(event.get('description', ''))
            })
        
        # AI analysis
        efficiency_analysis = ai_service.analyze_calendar_efficiency(processed_events)
        
        return {
            'events': processed_events,
            'total_events': len(processed_events),
            'efficiency_analysis': efficiency_analysis,
            'upcoming_today': [e for e in processed_events if is_today(e['start'])]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch calendar events: {str(e)}")

@router.get("/stats")
async def get_calendar_stats(authorization: str = Header(...)):
    """Get calendar statistics and productivity insights"""
    try:
        access_token = authorization.replace("Bearer ", "")
        service = get_calendar_service(access_token)
        
        # Get today's events
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        today_events = service.events().list(
            calendarId='primary',
            timeMin=today_start.isoformat() + 'Z',
            timeMax=today_end.isoformat() + 'Z',
            singleEvents=True
        ).execute()
        
        # Get this week's events
        week_start = today_start - timedelta(days=today_start.weekday())
        week_end = week_start + timedelta(days=7)
        
        week_events = service.events().list(
            calendarId='primary',
            timeMin=week_start.isoformat() + 'Z',
            timeMax=week_end.isoformat() + 'Z',
            singleEvents=True
        ).execute()
        
        today_count = len(today_events.get('items', []))
        week_count = len(week_events.get('items', []))
        
        return {
            'today_meetings': today_count,
            'week_meetings': week_count,
            'average_daily_meetings': week_count / 7,
            'insights': [
                f"You have {today_count} meetings scheduled for today",
                f"This week you have {week_count} total meetings",
                "Consider blocking focus time between meetings" if today_count > 4 else "Good meeting balance today"
            ],
            'productivity_score': calculate_productivity_score(today_count, week_count)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get calendar stats: {str(e)}")

@router.get("/focus-time")
async def get_focus_time_suggestions(authorization: str = Header(...)):
    """Suggest optimal focus time blocks based on calendar"""
    try:
        access_token = authorization.replace("Bearer ", "")
        service = get_calendar_service(access_token)
        
        # Get today's events
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        events = service.events().list(
            calendarId='primary',
            timeMin=today_start.isoformat() + 'Z',
            timeMax=today_end.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        # Find gaps between meetings
        focus_blocks = []
        events_list = events.get('items', [])
        
        if events_list:
            # Check morning block (9 AM to first meeting)
            first_meeting = datetime.fromisoformat(events_list[0]['start'].get('dateTime', '').replace('Z', '+00:00'))
            morning_start = today_start.replace(hour=9)
            
            if first_meeting > morning_start + timedelta(hours=1):
                focus_blocks.append({
                    'start': morning_start.isoformat(),
                    'end': first_meeting.isoformat(),
                    'duration_hours': (first_meeting - morning_start).total_seconds() / 3600,
                    'suggestion': 'Morning focus block - great for deep work'
                })
        
        return {
            'focus_blocks': focus_blocks,
            'recommendations': [
                "Block 2-hour chunks for deep work",
                "Avoid scheduling meetings during your peak energy hours",
                "Use the Pomodoro technique during focus blocks"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate focus time suggestions: {str(e)}")

def extract_meeting_link(description: str) -> str:
    """Extract meeting link from event description"""
    import re
    
    # Common meeting link patterns
    patterns = [
        r'https://[a-zA-Z0-9.-]+\.zoom\.us/[^\s]+',
        r'https://meet\.google\.com/[^\s]+',
        r'https://teams\.microsoft\.com/[^\s]+',
        r'https://[a-zA-Z0-9.-]+\.webex\.com/[^\s]+'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, description)
        if match:
            return match.group(0)
    
    return ""

def is_today(date_str: str) -> bool:
    """Check if date string is today"""
    try:
        event_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        today = datetime.now().date()
        return event_date.date() == today
    except:
        return False

def calculate_productivity_score(today_meetings: int, week_meetings: int) -> int:
    """Calculate a simple productivity score based on meeting load"""
    if today_meetings == 0:
        return 100  # No meetings = high focus potential
    elif today_meetings <= 3:
        return 80   # Manageable meeting load
    elif today_meetings <= 6:
        return 60   # Busy but manageable
    else:
        return 30   # Overloaded with meetings