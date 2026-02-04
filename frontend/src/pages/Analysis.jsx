import { useState } from 'react'
import {
    Card,
    Typography,
    Row,
    Col,
    Tabs,
    Table,
    Tag,
    Space,
    Button,
    Progress,
    Collapse,
    Alert
} from 'antd'
import {
    LineChartOutlined,
    SafetyCertificateOutlined,
    BankOutlined,
    TrophyOutlined,
    BulbOutlined,
    RiseOutlined,
} from '@ant-design/icons'
import {
    RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts'

const { Title, Text, Paragraph } = Typography
const { Panel } = Collapse

// Mock analysis data
const metricsData = {
    liquidity: [
        { name: 'Current Ratio', value: 1.85, rating: 'good', benchmark: 1.5 },
        { name: 'Quick Ratio', value: 1.2, rating: 'fair', benchmark: 1.0 },
        { name: 'Cash Ratio', value: 0.45, rating: 'fair', benchmark: 0.5 },
    ],
    profitability: [
        { name: 'Gross Profit Margin', value: '40%', rating: 'excellent', benchmark: '35%' },
        { name: 'Net Profit Margin', value: '8.5%', rating: 'good', benchmark: '7%' },
        { name: 'ROE', value: '15%', rating: 'excellent', benchmark: '12%' },
        { name: 'ROA', value: '12%', rating: 'excellent', benchmark: '8%' },
    ],
    solvency: [
        { name: 'Debt to Equity', value: 0.65, rating: 'excellent', benchmark: 1.0 },
        { name: 'Interest Coverage', value: 5.2, rating: 'excellent', benchmark: 3.0 },
        { name: 'Debt Ratio', value: '40%', rating: 'good', benchmark: '50%' },
    ],
    efficiency: [
        { name: 'Asset Turnover', value: 1.8, rating: 'good', benchmark: 1.5 },
        { name: 'Inventory Turnover', value: 8.5, rating: 'good', benchmark: 7.0 },
        { name: 'Receivables Turnover', value: 12, rating: 'excellent', benchmark: 10 },
    ]
}

const radarData = [
    { subject: 'Liquidity', A: 75, fullMark: 100 },
    { subject: 'Profitability', A: 85, fullMark: 100 },
    { subject: 'Solvency', A: 90, fullMark: 100 },
    { subject: 'Efficiency', A: 70, fullMark: 100 },
    { subject: 'Growth', A: 65, fullMark: 100 },
]

const forecastData = [
    { month: 'Jul', actual: null, forecast: 5600000, optimistic: 6200000, pessimistic: 5000000 },
    { month: 'Aug', actual: null, forecast: 5800000, optimistic: 6500000, pessimistic: 5200000 },
    { month: 'Sep', actual: null, forecast: 6100000, optimistic: 6900000, pessimistic: 5400000 },
    { month: 'Oct', actual: null, forecast: 6400000, optimistic: 7300000, pessimistic: 5600000 },
    { month: 'Nov', actual: null, forecast: 6700000, optimistic: 7700000, pessimistic: 5800000 },
    { month: 'Dec', actual: null, forecast: 7100000, optimistic: 8200000, pessimistic: 6100000 },
]

const risks = [
    {
        name: 'Accounts Receivable Aging',
        severity: 'high',
        category: 'Credit Risk',
        description: '25% of receivables are overdue by 60+ days',
        mitigation: 'Implement stricter credit policies and follow-up procedures'
    },
    {
        name: 'Cash Flow Concentration',
        severity: 'medium',
        category: 'Operational',
        description: 'Top 3 customers contribute 65% of revenue',
        mitigation: 'Diversify customer base and develop new revenue streams'
    },
    {
        name: 'Inventory Buildup',
        severity: 'low',
        category: 'Operational',
        description: 'Inventory levels 15% above optimal',
        mitigation: 'Optimize inventory management and review procurement cycles'
    },
]

const recommendations = [
    { priority: 'high', text: 'Reduce accounts receivable aging by implementing automated payment reminders', impact: 'Improve cash flow by ₹15-20L' },
    { priority: 'high', text: 'Negotiate extended payment terms with key suppliers', impact: 'Improve working capital cycle by 10 days' },
    { priority: 'medium', text: 'Consider invoice financing for faster cash conversion', impact: 'Access to ₹50L additional liquidity' },
    { priority: 'medium', text: 'Optimize inventory levels to reduce carrying costs', impact: 'Save ₹5-8L annually' },
    { priority: 'low', text: 'Explore term deposit options for idle cash', impact: 'Earn additional ₹2-3L in interest' },
]

const MetricsTable = ({ data }) => {
    const columns = [
        { title: 'Metric', dataIndex: 'name', key: 'name' },
        {
            title: 'Value',
            dataIndex: 'value',
            key: 'value',
            render: (val) => <Text strong>{val}</Text>
        },
        {
            title: 'Rating',
            dataIndex: 'rating',
            key: 'rating',
            render: (rating) => {
                const colors = { excellent: 'green', good: 'blue', fair: 'orange', poor: 'red' }
                return <Tag color={colors[rating]}>{rating.toUpperCase()}</Tag>
            }
        },
        { title: 'Benchmark', dataIndex: 'benchmark', key: 'benchmark' },
    ]

    return <Table dataSource={data} columns={columns} pagination={false} size="small" />
}

export default function Analysis() {
    const [activeTab, setActiveTab] = useState('overview')

    const tabItems = [
        {
            key: 'overview',
            label: <span><LineChartOutlined /> Overview</span>,
            children: (
                <Row gutter={[24, 24]}>
                    <Col xs={24} lg={12}>
                        <Card className="card">
                            <Title level={5}>Health Score Breakdown</Title>
                            <div style={{ height: 300 }}>
                                <ResponsiveContainer width="100%" height="100%">
                                    <RadarChart data={radarData}>
                                        <PolarGrid stroke="#E5E7EB" />
                                        <PolarAngleAxis dataKey="subject" tick={{ fill: '#6B7280', fontSize: 12 }} />
                                        <PolarRadiusAxis angle={30} domain={[0, 100]} />
                                        <Radar name="Score" dataKey="A" stroke="#6366F1" fill="#6366F1" fillOpacity={0.5} />
                                        <Tooltip />
                                    </RadarChart>
                                </ResponsiveContainer>
                            </div>
                        </Card>
                    </Col>

                    <Col xs={24} lg={12}>
                        <Card className="card">
                            <Title level={5}>Credit Score</Title>
                            <div style={{ textAlign: 'center', padding: '2rem 0' }}>
                                <Progress
                                    type="dashboard"
                                    percent={75}
                                    format={() => '725'}
                                    strokeColor={{ '0%': '#6366F1', '100%': '#10B981' }}
                                    width={150}
                                />
                                <div style={{ marginTop: '1rem' }}>
                                    <Tag color="green" style={{ fontSize: '1rem', padding: '0.5rem 1rem' }}>
                                        <TrophyOutlined /> Rating: A
                                    </Tag>
                                </div>
                                <Paragraph type="secondary" style={{ marginTop: '1rem' }}>
                                    Your credit score indicates good creditworthiness
                                </Paragraph>
                            </div>
                        </Card>
                    </Col>
                </Row>
            )
        },
        {
            key: 'metrics',
            label: <span><RiseOutlined /> Metrics</span>,
            children: (
                <Tabs
                    tabPosition="left"
                    items={[
                        { key: 'liquidity', label: 'Liquidity', children: <MetricsTable data={metricsData.liquidity} /> },
                        { key: 'profitability', label: 'Profitability', children: <MetricsTable data={metricsData.profitability} /> },
                        { key: 'solvency', label: 'Solvency', children: <MetricsTable data={metricsData.solvency} /> },
                        { key: 'efficiency', label: 'Efficiency', children: <MetricsTable data={metricsData.efficiency} /> },
                    ]}
                />
            )
        },
        {
            key: 'forecast',
            label: <span><LineChartOutlined /> Forecast</span>,
            children: (
                <Card className="card">
                    <Title level={5}>12-Month Revenue Forecast</Title>
                    <div style={{ height: 350 }}>
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={forecastData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                                <XAxis dataKey="month" stroke="#6B7280" />
                                <YAxis stroke="#6B7280" tickFormatter={(v) => `₹${(v / 100000).toFixed(0)}L`} />
                                <Tooltip formatter={(v) => `₹${(v / 100000).toFixed(1)}L`} />
                                <Legend />
                                <Line type="monotone" dataKey="forecast" stroke="#6366F1" strokeWidth={2} name="Base Forecast" />
                                <Line type="monotone" dataKey="optimistic" stroke="#10B981" strokeDasharray="5 5" name="Optimistic" />
                                <Line type="monotone" dataKey="pessimistic" stroke="#EF4444" strokeDasharray="5 5" name="Pessimistic" />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </Card>
            )
        },
        {
            key: 'risks',
            label: <span><SafetyCertificateOutlined /> Risks</span>,
            children: (
                <Card className="card">
                    <Collapse accordion>
                        {risks.map((risk, index) => (
                            <Panel
                                key={index}
                                header={
                                    <Space>
                                        <Tag color={risk.severity === 'high' ? 'red' : risk.severity === 'medium' ? 'orange' : 'green'}>
                                            {risk.severity.toUpperCase()}
                                        </Tag>
                                        {risk.name}
                                    </Space>
                                }
                            >
                                <Paragraph><strong>Category:</strong> {risk.category}</Paragraph>
                                <Paragraph><strong>Description:</strong> {risk.description}</Paragraph>
                                <Alert
                                    message="Recommended Action"
                                    description={risk.mitigation}
                                    type="info"
                                    showIcon
                                    icon={<BulbOutlined />}
                                />
                            </Panel>
                        ))}
                    </Collapse>
                </Card>
            )
        },
        {
            key: 'recommendations',
            label: <span><BulbOutlined /> Recommendations</span>,
            children: (
                <Card className="card">
                    <Space direction="vertical" style={{ width: '100%' }}>
                        {recommendations.map((rec, index) => (
                            <Card
                                key={index}
                                size="small"
                                style={{
                                    borderLeft: `4px solid ${rec.priority === 'high' ? '#EF4444' : rec.priority === 'medium' ? '#F59E0B' : '#10B981'}`
                                }}
                            >
                                <Row justify="space-between" align="middle">
                                    <Col span={18}>
                                        <Text strong>{rec.text}</Text>
                                        <br />
                                        <Text type="secondary" style={{ fontSize: '0.875rem' }}>
                                            Expected Impact: {rec.impact}
                                        </Text>
                                    </Col>
                                    <Col>
                                        <Tag color={rec.priority === 'high' ? 'red' : rec.priority === 'medium' ? 'orange' : 'green'}>
                                            {rec.priority.toUpperCase()}
                                        </Tag>
                                    </Col>
                                </Row>
                            </Card>
                        ))}
                    </Space>
                </Card>
            )
        },
    ]

    return (
        <div className="fade-in">
            <Row justify="space-between" align="middle" style={{ marginBottom: '1.5rem' }}>
                <Col>
                    <Title level={2}>Financial Analysis</Title>
                    <Text type="secondary">Comprehensive analysis of your financial health</Text>
                </Col>
                <Col>
                    <Space>
                        <Button type="primary" icon={<BankOutlined />}>View Loan Options</Button>
                        <Button>Export Analysis</Button>
                    </Space>
                </Col>
            </Row>

            <Tabs activeKey={activeTab} onChange={setActiveTab} items={tabItems} />
        </div>
    )
}
