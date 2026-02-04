import { useState, useEffect } from 'react'
import { Row, Col, Card, Statistic, Progress, Typography, Tag, Space, Spin } from 'antd'
import {
    ArrowUpOutlined,
    ArrowDownOutlined,
    CheckCircleOutlined,
    ExclamationCircleOutlined,
    ThunderboltOutlined,
    SafetyCertificateOutlined,
} from '@ant-design/icons'
import {
    AreaChart, Area, PieChart, Pie, Cell, BarChart, Bar,
    XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts'

const { Title, Text } = Typography

// Mock data for demonstration
const mockHealthScore = {
    overall_score: 72,
    rating: 'Good',
    components: {
        liquidity: 78,
        profitability: 65,
        solvency: 80,
        efficiency: 64
    }
}

const mockMetrics = [
    { name: 'Current Ratio', value: 1.85, rating: 'good', benchmark: 1.5 },
    { name: 'Quick Ratio', value: 1.2, rating: 'fair', benchmark: 1.0 },
    { name: 'Net Profit Margin', value: '8.5%', rating: 'good', benchmark: '7%' },
    { name: 'Debt to Equity', value: 0.65, rating: 'excellent', benchmark: 1.0 },
    { name: 'ROA', value: '12%', rating: 'excellent', benchmark: '8%' },
    { name: 'Working Capital', value: '₹25L', rating: 'good', benchmark: '₹20L' },
]

const mockRisks = [
    { name: 'Cash Flow Concentration', severity: 'medium', category: 'Operational' },
    { name: 'Accounts Receivable Aging', severity: 'high', category: 'Credit' },
    { name: 'Inventory Build-up', severity: 'low', category: 'Operational' },
]

const revenueData = [
    { month: 'Jan', revenue: 4200000, expenses: 3800000 },
    { month: 'Feb', revenue: 4500000, expenses: 3900000 },
    { month: 'Mar', revenue: 4800000, expenses: 4100000 },
    { month: 'Apr', revenue: 5100000, expenses: 4300000 },
    { month: 'May', revenue: 4900000, expenses: 4200000 },
    { month: 'Jun', revenue: 5400000, expenses: 4500000 },
]

const componentData = [
    { name: 'Liquidity', value: 78, fill: '#6366F1' },
    { name: 'Profitability', value: 65, fill: '#10B981' },
    { name: 'Solvency', value: 80, fill: '#F59E0B' },
    { name: 'Efficiency', value: 64, fill: '#EC4899' },
]

const COLORS = ['#6366F1', '#10B981', '#F59E0B', '#EC4899']

function HealthScoreCard({ score }) {
    const getScoreColor = (score) => {
        if (score >= 80) return '#10B981'
        if (score >= 60) return '#6366F1'
        if (score >= 40) return '#F59E0B'
        return '#EF4444'
    }

    const getRatingClass = (rating) => {
        return rating.toLowerCase().replace(' ', '-')
    }

    return (
        <Card className="card" style={{ textAlign: 'center' }}>
            <div className="health-score">
                <div
                    className="score-circle"
                    style={{
                        background: `linear-gradient(135deg, ${getScoreColor(score.overall_score)}, ${getScoreColor(score.overall_score)}dd)`
                    }}
                >
                    <span className="score-value">{score.overall_score}</span>
                    <span className="score-label">out of 100</span>
                </div>
                <span className={`score-rating ${getRatingClass(score.rating)}`}>
                    {score.rating} Financial Health
                </span>
            </div>

            <Row gutter={16} style={{ marginTop: '1.5rem' }}>
                {Object.entries(score.components).map(([key, value]) => (
                    <Col span={6} key={key}>
                        <Statistic
                            title={key.charAt(0).toUpperCase() + key.slice(1)}
                            value={value}
                            suffix="/100"
                            valueStyle={{ fontSize: '1rem', color: getScoreColor(value) }}
                        />
                    </Col>
                ))}
            </Row>
        </Card>
    )
}

function MetricsGrid({ metrics }) {
    return (
        <div className="metrics-grid">
            {metrics.map((metric, index) => (
                <div key={index} className="metric-card fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
                    <div className="metric-name">{metric.name}</div>
                    <div className="metric-value">{metric.value}</div>
                    <span className={`metric-rating ${metric.rating}`}>
                        {metric.rating === 'excellent' && <CheckCircleOutlined />}
                        {metric.rating === 'good' && <ThunderboltOutlined />}
                        {metric.rating === 'fair' && <ExclamationCircleOutlined />}
                        {' '}{metric.rating.charAt(0).toUpperCase() + metric.rating.slice(1)}
                    </span>
                    <div style={{ marginTop: '0.5rem', fontSize: '0.75rem', color: '#6B7280' }}>
                        Benchmark: {metric.benchmark}
                    </div>
                </div>
            ))}
        </div>
    )
}

function RiskOverview({ risks }) {
    const getSeverityColor = (severity) => {
        switch (severity) {
            case 'high': return 'red'
            case 'medium': return 'orange'
            case 'low': return 'green'
            default: return 'blue'
        }
    }

    return (
        <Card
            title={<span><SafetyCertificateOutlined /> Risk Overview</span>}
            className="card"
        >
            <Space direction="vertical" style={{ width: '100%' }}>
                {risks.map((risk, index) => (
                    <div
                        key={index}
                        style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            padding: '0.75rem',
                            background: '#F9FAFB',
                            borderRadius: '8px',
                            marginBottom: '0.5rem'
                        }}
                    >
                        <div>
                            <Text strong>{risk.name}</Text>
                            <br />
                            <Text type="secondary" style={{ fontSize: '0.75rem' }}>{risk.category}</Text>
                        </div>
                        <Tag color={getSeverityColor(risk.severity)}>
                            {risk.severity.toUpperCase()}
                        </Tag>
                    </div>
                ))}
            </Space>
        </Card>
    )
}

function RevenueChart() {
    return (
        <Card
            title="Revenue vs Expenses Trend"
            className="card"
        >
            <div className="chart-container">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={revenueData}>
                        <defs>
                            <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#6366F1" stopOpacity={0.8} />
                                <stop offset="95%" stopColor="#6366F1" stopOpacity={0} />
                            </linearGradient>
                            <linearGradient id="colorExpenses" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#F59E0B" stopOpacity={0.8} />
                                <stop offset="95%" stopColor="#F59E0B" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                        <XAxis dataKey="month" stroke="#6B7280" />
                        <YAxis stroke="#6B7280" tickFormatter={(value) => `₹${(value / 100000).toFixed(0)}L`} />
                        <Tooltip
                            formatter={(value) => `₹${(value / 100000).toFixed(1)}L`}
                            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                        />
                        <Legend />
                        <Area type="monotone" dataKey="revenue" stroke="#6366F1" fillOpacity={1} fill="url(#colorRevenue)" name="Revenue" />
                        <Area type="monotone" dataKey="expenses" stroke="#F59E0B" fillOpacity={1} fill="url(#colorExpenses)" name="Expenses" />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </Card>
    )
}

function ComponentBreakdown() {
    return (
        <Card
            title="Health Score Components"
            className="card"
        >
            <div className="chart-container">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={componentData} layout="vertical">
                        <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                        <XAxis type="number" domain={[0, 100]} stroke="#6B7280" />
                        <YAxis dataKey="name" type="category" stroke="#6B7280" width={80} />
                        <Tooltip
                            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                        />
                        <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                            {componentData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.fill} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </Card>
    )
}

export default function Dashboard() {
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        // Simulate loading
        const timer = setTimeout(() => setLoading(false), 1000)
        return () => clearTimeout(timer)
    }, [])

    if (loading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
                <Spin size="large" />
            </div>
        )
    }

    return (
        <div className="fade-in">
            <Title level={2}>Financial Health Dashboard</Title>
            <Text type="secondary" style={{ marginBottom: '2rem', display: 'block' }}>
                Overview of your business financial health and key metrics
            </Text>

            <Row gutter={[24, 24]}>
                {/* Health Score */}
                <Col xs={24} lg={10}>
                    <HealthScoreCard score={mockHealthScore} />
                </Col>

                {/* Risk Overview */}
                <Col xs={24} lg={14}>
                    <RiskOverview risks={mockRisks} />
                </Col>

                {/* Key Metrics */}
                <Col span={24}>
                    <Title level={4} style={{ marginBottom: '1rem' }}>Key Financial Metrics</Title>
                    <MetricsGrid metrics={mockMetrics} />
                </Col>

                {/* Charts Row */}
                <Col xs={24} lg={14}>
                    <RevenueChart />
                </Col>

                <Col xs={24} lg={10}>
                    <ComponentBreakdown />
                </Col>
            </Row>
        </div>
    )
}
