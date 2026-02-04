import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import {
    DashboardOutlined,
    UploadOutlined,
    LineChartOutlined,
    FileTextOutlined,
    SettingOutlined,
    BankOutlined,
    SafetyCertificateOutlined,
} from '@ant-design/icons'
import Dashboard from './pages/Dashboard'
import Upload from './pages/Upload'
import Analysis from './pages/Analysis'
import Reports from './pages/Reports'

function Sidebar() {
    const location = useLocation()

    const navItems = [
        { path: '/', icon: <DashboardOutlined />, label: 'Dashboard' },
        { path: '/upload', icon: <UploadOutlined />, label: 'Upload Documents' },
        { path: '/analysis', icon: <LineChartOutlined />, label: 'Analysis' },
        { path: '/reports', icon: <FileTextOutlined />, label: 'Reports' },
    ]

    return (
        <aside className="sidebar">
            <div className="sidebar-logo">
                <BankOutlined style={{ fontSize: '1.5rem' }} />
                <span>FinHealth</span>
            </div>

            <nav className="sidebar-nav">
                {navItems.map((item) => (
                    <Link
                        key={item.path}
                        to={item.path}
                        className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
                    >
                        {item.icon}
                        <span>{item.label}</span>
                    </Link>
                ))}
            </nav>

            <div className="sidebar-footer" style={{ borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '1rem' }}>
                <Link to="/settings" className="nav-item">
                    <SettingOutlined />
                    <span>Settings</span>
                </Link>
            </div>
        </aside>
    )
}

function App() {
    return (
        <Router>
            <div className="app">
                <div className="layout">
                    <Sidebar />
                    <main className="main-content">
                        <Routes>
                            <Route path="/" element={<Dashboard />} />
                            <Route path="/upload" element={<Upload />} />
                            <Route path="/analysis" element={<Analysis />} />
                            <Route path="/reports" element={<Reports />} />
                        </Routes>
                    </main>
                </div>
            </div>
        </Router>
    )
}

export default App
