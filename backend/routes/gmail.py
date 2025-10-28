from fastapi import APIRouter, HTTPException, Header
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from services.ai_summary import ai_service
import base64
from typing import Optional, List, Dict

router = APIRouter()

def get_gmail_service(access_token: str):
    """Create Gmail service with access token"""
    credentials = Credentials(token=access_token)
    return build('gmail', 'v1', credentials=credentials)

@router.get("/messages")
async def get_messages(
    authorization: str = Header(...),
    max_results: int = 10
):
    """Fetch recent Gmail messages with AI summaries"""
    try:
        # Extract token from Authorization header
        access_token = authorization.replace("Bearer ", "")
        service = get_gmail_service(access_token)
        
        # Get message list
        results = service.users().messages().list(
            userId='me',
            maxResults=max_results,
            q='is:unread OR newer_than:7d'  # Unread or from last 7 days
        ).execute()
        
        messages = results.get('messages', [])
        processed_messages = []
        
        for msg in messages:
            # Get full message
            message = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()
            
            # Extract message data
            headers = message['payload'].get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            
            # Extract body
            body = extract_message_body(message['payload'])
            
            # AI processing
            summary = ai_service.summarize_text(body) if body else "No content to summarize"
            tasks = ai_service.extract_tasks(body) if body else []
            
            processed_messages.append({
                'id': msg['id'],
                'subject': subject,
                'sender': sender,
                'date': date,
                'summary': summary,
                'tasks': tasks,
                'snippet': message.get('snippet', '')
            })
        
        return {
            'messages': processed_messages,
            'total_count': len(processed_messages)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch Gmail messages: {str(e)}")

@router.get("/stats")
async def get_email_stats(authorization: str = Header(...)):
    """Get email statistics and insights"""
    try:
        access_token = authorization.replace("Bearer ", "")
        service = get_gmail_service(access_token)
        
        # Get various email counts
        unread_result = service.users().messages().list(
            userId='me',
            q='is:unread'
        ).execute()
        
        today_result = service.users().messages().list(
            userId='me',
            q='newer_than:1d'
        ).execute()
        
        return {
            'unread_count': unread_result.get('resultSizeEstimate', 0),
            'today_count': today_result.get('resultSizeEstimate', 0),
            'processed_today': len(today_result.get('messages', [])),
            'insights': [
                f"You have {unread_result.get('resultSizeEstimate', 0)} unread emails",
                f"Received {today_result.get('resultSizeEstimate', 0)} emails today"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get email stats: {str(e)}")

def extract_message_body(payload) -> str:
    """Extract text body from Gmail message payload"""
    body = ""
    
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                body = base64.urlsafe_b64decode(data).decode('utf-8')
                break
            elif part['mimeType'] == 'text/html':
                data = part['body']['data']
                body = base64.urlsafe_b64decode(data).decode('utf-8')
    else:
        if payload['mimeType'] == 'text/plain':
            data = payload['body']['data']
            body = base64.urlsafe_b64decode(data).decode('utf-8')
    
    return body