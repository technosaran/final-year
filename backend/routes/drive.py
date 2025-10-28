from fastapi import APIRouter, HTTPException, Header
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from services.ai_summary import ai_service
from typing import List, Dict

router = APIRouter()

def get_drive_service(access_token: str):
    """Create Drive service with access token"""
    credentials = Credentials(token=access_token)
    return build('drive', 'v3', credentials=credentials)

@router.get("/files")
async def get_files(
    authorization: str = Header(...),
    max_results: int = 20
):
    """Fetch Google Drive files with AI categorization"""
    try:
        access_token = authorization.replace("Bearer ", "")
        service = get_drive_service(access_token)
        
        # Get files list
        results = service.files().list(
            pageSize=max_results,
            fields="nextPageToken, files(id, name, mimeType, size, modifiedTime, webViewLink)",
            orderBy="modifiedTime desc"
        ).execute()
        
        files = results.get('files', [])
        categorized_files = []
        
        for file in files:
            # AI categorization
            category = ai_service.categorize_file(file['name'])
            
            categorized_files.append({
                'id': file['id'],
                'name': file['name'],
                'mimeType': file['mimeType'],
                'size': file.get('size', 'Unknown'),
                'modifiedTime': file['modifiedTime'],
                'webViewLink': file.get('webViewLink', ''),
                'category': category
            })
        
        # Group by category
        categories = {}
        for file in categorized_files:
            cat = file['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(file)
        
        return {
            'files': categorized_files,
            'categories': categories,
            'total_count': len(categorized_files),
            'category_summary': {cat: len(files) for cat, files in categories.items()}
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch Drive files: {str(e)}")

@router.get("/stats")
async def get_drive_stats(authorization: str = Header(...)):
    """Get Drive storage and organization stats"""
    try:
        access_token = authorization.replace("Bearer ", "")
        service = get_drive_service(access_token)
        
        # Get storage info
        about = service.about().get(fields="storageQuota, user").execute()
        storage_quota = about.get('storageQuota', {})
        
        # Get recent files count
        recent_files = service.files().list(
            q="modifiedTime > '2024-01-01T00:00:00'",
            fields="files(id)"
        ).execute()
        
        return {
            'storage_used': storage_quota.get('usage', 'Unknown'),
            'storage_limit': storage_quota.get('limit', 'Unknown'),
            'recent_files_count': len(recent_files.get('files', [])),
            'user_email': about.get('user', {}).get('emailAddress', 'Unknown'),
            'insights': [
                f"You have {len(recent_files.get('files', []))} files modified this year",
                "Consider organizing files into folders for better productivity"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get Drive stats: {str(e)}")

@router.post("/organize")
async def suggest_organization(
    authorization: str = Header(...),
    file_ids: List[str] = None
):
    """Suggest file organization based on AI analysis"""
    try:
        access_token = authorization.replace("Bearer ", "")
        service = get_drive_service(access_token)
        
        suggestions = []
        
        if file_ids:
            for file_id in file_ids:
                file = service.files().get(fileId=file_id, fields="name, mimeType").execute()
                category = ai_service.categorize_file(file['name'])
                
                suggestions.append({
                    'file_id': file_id,
                    'file_name': file['name'],
                    'suggested_folder': category,
                    'reason': f"File appears to be a {category.lower()} based on name and type"
                })
        
        return {
            'suggestions': suggestions,
            'organization_tips': [
                "Create folders for each category (Documents, Images, Spreadsheets)",
                "Use consistent naming conventions",
                "Archive old files to reduce clutter"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate organization suggestions: {str(e)}")