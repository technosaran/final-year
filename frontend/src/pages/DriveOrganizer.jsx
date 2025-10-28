import React, { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { FolderOpen, File, Calendar, Tag } from 'lucide-react'
import axios from 'axios'

const DriveOrganizer = () => {
  const { getAuthHeaders } = useAuth()
  const [files, setFiles] = useState([])
  const [categories, setCategories] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchFiles()
  }, [])

  const fetchFiles = async () => {
    try {
      const headers = getAuthHeaders()
      const response = await axios.get('/api/drive/files', { headers })
      setFiles(response.data.files || [])
      setCategories(response.data.categories || {})
    } catch (error) {
      console.error('Failed to fetch files:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatFileSize = (bytes) => {
    if (!bytes || bytes === 'Unknown') return 'Unknown'
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(1024))
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i]
  }

  const getCategoryColor = (category) => {
    const colors = {
      'Document': 'bg-blue-100 text-blue-800',
      'Image': 'bg-green-100 text-green-800',
      'Spreadsheet': 'bg-yellow-100 text-yellow-800',
      'Presentation': 'bg-purple-100 text-purple-800',
      'Resume/CV': 'bg-red-100 text-red-800',
      'Report': 'bg-indigo-100 text-indigo-800',
      'Other': 'bg-gray-100 text-gray-800'
    }
    return colors[category] || colors['Other']
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Drive Organizer</h1>
          <p className="text-gray-600">AI-powered file categorization and organization</p>
        </div>
        <button onClick={fetchFiles} className="btn-primary">
          Refresh
        </button>
      </div>

      {/* Category Summary */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {Object.entries(categories).map(([category, categoryFiles]) => (
          <div key={category} className="card text-center">
            <div className="flex items-center justify-center mb-2">
              <FolderOpen className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="font-semibold text-gray-900">{category}</h3>
            <p className="text-2xl font-bold text-primary-600">{categoryFiles.length}</p>
            <p className="text-sm text-gray-600">files</p>
          </div>
        ))}
      </div>

      {/* Files List */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Files</h3>
        
        {files.length === 0 ? (
          <div className="text-center py-12">
            <File className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No files found</h3>
            <p className="text-gray-600">Connect your Google Drive to see AI-categorized files</p>
          </div>
        ) : (
          <div className="space-y-3">
            {files.map((file) => (
              <div
                key={file.id}
                className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center flex-1">
                  <File className="h-5 w-5 text-gray-400 mr-3 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <h4 className="font-medium text-gray-900 truncate">
                      {file.name}
                    </h4>
                    <div className="flex items-center text-sm text-gray-600 space-x-4 mt-1">
                      <div className="flex items-center">
                        <Calendar className="h-4 w-4 mr-1" />
                        {new Date(file.modifiedTime).toLocaleDateString()}
                      </div>
                      <span>{formatFileSize(file.size)}</span>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getCategoryColor(file.category)}`}>
                    <Tag className="h-3 w-3 mr-1" />
                    {file.category}
                  </span>
                  
                  {file.webViewLink && (
                    <a
                      href={file.webViewLink}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary-600 hover:text-primary-700 text-sm font-medium"
                    >
                      Open
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Organization Suggestions */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Organization Tips</h3>
        <div className="space-y-3">
          <div className="flex items-start">
            <div className="w-2 h-2 bg-blue-500 rounded-full mr-3 mt-2"></div>
            <p className="text-sm text-gray-700">Create folders for each category (Documents, Images, Spreadsheets)</p>
          </div>
          <div className="flex items-start">
            <div className="w-2 h-2 bg-green-500 rounded-full mr-3 mt-2"></div>
            <p className="text-sm text-gray-700">Use consistent naming conventions for better searchability</p>
          </div>
          <div className="flex items-start">
            <div className="w-2 h-2 bg-purple-500 rounded-full mr-3 mt-2"></div>
            <p className="text-sm text-gray-700">Archive old files to reduce clutter and improve performance</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DriveOrganizer