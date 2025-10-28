import React, { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { Mail, FolderOpen, Calendar, TrendingUp, Clock, CheckCircle } from 'lucide-react'
import axios from 'axios'

const Dashboard = () => {
  const { getAuthHeaders } = useAuth()
  const [stats, setStats] = useState({
    emails: { unread_count: 0, today_count: 0 },
    drive: { recent_files_count: 0 },
    calendar: { today_meetings: 0, productivity_score: 0 }
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const headers = getAuthHeaders()
      
      const [emailStats, driveStats, calendarStats] = await Promise.all([
        axios.get('/api/gmail/stats', { headers }).catch(() => ({ data: { unread_count: 0, today_count: 0 } })),
        axios.get('/api/drive/stats', { headers }).catch(() => ({ data: { recent_files_count: 0 } })),
        axios.get('/api/calendar/stats', { headers }).catch(() => ({ data: { today_meetings: 0, productivity_score: 0 } }))
      ])

      setStats({
        emails: emailStats.data,
        drive: driveStats.data,
        calendar: calendarStats.data
      })
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const statCards = [
    {
      title: 'Unread Emails',
      value: stats.emails.unread_count || 0,
      icon: Mail,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      change: `+${stats.emails.today_count || 0} today`
    },
    {
      title: 'Recent Files',
      value: stats.drive.recent_files_count || 0,
      icon: FolderOpen,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
      change: 'This year'
    },
    {
      title: 'Today\'s Meetings',
      value: stats.calendar.today_meetings || 0,
      icon: Calendar,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
      change: 'Scheduled'
    },
    {
      title: 'Productivity Score',
      value: stats.calendar.productivity_score || 0,
      icon: TrendingUp,
      color: 'text-orange-600',
      bgColor: 'bg-orange-50',
      change: 'Out of 100'
    }
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Your AI-powered productivity overview</p>
        </div>
        <button
          onClick={fetchDashboardData}
          className="btn-primary flex items-center"
        >
          <Clock className="h-4 w-4 mr-2" />
          Refresh Data
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => (
          <div key={index} className="card">
            <div className="flex items-center">
              <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                <stat.icon className={`h-6 w-6 ${stat.color}`} />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                <p className="text-xs text-gray-500">{stat.change}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <button className="w-full flex items-center justify-between p-3 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <div className="flex items-center">
                <Mail className="h-5 w-5 text-blue-600 mr-3" />
                <span className="font-medium">Summarize Recent Emails</span>
              </div>
              <span className="text-sm text-gray-500">→</span>
            </button>
            
            <button className="w-full flex items-center justify-between p-3 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <div className="flex items-center">
                <FolderOpen className="h-5 w-5 text-green-600 mr-3" />
                <span className="font-medium">Organize Drive Files</span>
              </div>
              <span className="text-sm text-gray-500">→</span>
            </button>
            
            <button className="w-full flex items-center justify-between p-3 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <div className="flex items-center">
                <Calendar className="h-5 w-5 text-purple-600 mr-3" />
                <span className="font-medium">Optimize Schedule</span>
              </div>
              <span className="text-sm text-gray-500">→</span>
            </button>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Today's Insights</h3>
          <div className="space-y-3">
            {stats.emails.insights?.map((insight, index) => (
              <div key={index} className="flex items-start">
                <CheckCircle className="h-5 w-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
                <p className="text-sm text-gray-700">{insight}</p>
              </div>
            )) || (
              <div className="flex items-start">
                <CheckCircle className="h-5 w-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
                <p className="text-sm text-gray-700">Connect your services to see personalized insights</p>
              </div>
            )}
            
            {stats.calendar.insights?.map((insight, index) => (
              <div key={`cal-${index}`} className="flex items-start">
                <CheckCircle className="h-5 w-5 text-blue-500 mr-3 mt-0.5 flex-shrink-0" />
                <p className="text-sm text-gray-700">{insight}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between py-2">
            <div className="flex items-center">
              <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
              <span className="text-sm text-gray-700">Dashboard data refreshed</span>
            </div>
            <span className="text-xs text-gray-500">Just now</span>
          </div>
          
          <div className="flex items-center justify-between py-2">
            <div className="flex items-center">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
              <span className="text-sm text-gray-700">Connected to Google services</span>
            </div>
            <span className="text-xs text-gray-500">Today</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard