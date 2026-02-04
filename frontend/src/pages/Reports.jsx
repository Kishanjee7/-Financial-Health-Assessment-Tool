import { useState } from 'react'
import {
    Card,
    Typography,
    Row,
    Col,
    Button,
    Radio,
    Select,
    Space,
    Divider,
    message,
    Spin
} from 'antd'
import {
    FilePdfOutlined,
    DownloadOutlined,
    GlobalOutlined,
    PrinterOutlined,
    ShareAltOutlined,
} from '@ant-design/icons'

const { Title, Text, Paragraph } = Typography

const reportTypes = [
    {
        id: 'full',
        name: 'Full Analysis Report',
        description: 'Comprehensive investor-ready report with all metrics, risk assessment, and recommendations',
        pages: '15-20 pages',
        icon: <FilePdfOutlined style={{ fontSize: '2rem', color: '#6366F1' }} />
    },
    {
        id: 'quick',
        name: 'Quick Summary',
        description: 'One-page executive summary of financial health score and key highlights',
        pages: '1 page',
        icon: <FilePdfOutlined style={{ fontSize: '2rem', color: '#10B981' }} />
    },
    {
        id: 'benchmark',
        name: 'Industry Benchmark Report',
        description: 'Comparison against industry standards with detailed analysis',
        pages: '8-10 pages',
        icon: <FilePdfOutlined style={{ fontSize: '2rem', color: '#F59E0B' }} />
    },
    {
        id: 'forecast',
        name: 'Financial Forecast Report',
        description: 'Detailed projections for revenue, expenses, and cash flow',
        pages: '10-12 pages',
        icon: <FilePdfOutlined style={{ fontSize: '2rem', color: '#EC4899' }} />
    },
]

const generatedReports = [
    { name: 'Full_Analysis_Report_Jan2024.pdf', date: '2024-01-15', size: '2.4 MB' },
    { name: 'Quick_Summary_Jan2024.pdf', date: '2024-01-15', size: '256 KB' },
    { name: 'Benchmark_Report_Q4_2023.pdf', date: '2023-12-01', size: '1.8 MB' },
]

export default function Reports() {
    const [selectedReport, setSelectedReport] = useState('full')
    const [language, setLanguage] = useState('en')
    const [generating, setGenerating] = useState(false)

    const handleGenerate = async () => {
        setGenerating(true)
        // Simulate report generation
        setTimeout(() => {
            setGenerating(false)
            message.success('Report generated successfully!')
        }, 2000)
    }

    return (
        <div className="fade-in">
            <Title level={2}>Financial Reports</Title>
            <Text type="secondary" style={{ marginBottom: '2rem', display: 'block' }}>
                Generate and download professional financial reports
            </Text>

            <Row gutter={24}>
                <Col xs={24} lg={16}>
                    <Card className="card">
                        <Title level={4}>Select Report Type</Title>

                        <Radio.Group
                            value={selectedReport}
                            onChange={(e) => setSelectedReport(e.target.value)}
                            style={{ width: '100%' }}
                        >
                            <Space direction="vertical" style={{ width: '100%' }}>
                                {reportTypes.map(report => (
                                    <Radio
                                        key={report.id}
                                        value={report.id}
                                        style={{
                                            width: '100%',
                                            padding: '1rem',
                                            background: selectedReport === report.id ? '#EEF2FF' : '#F9FAFB',
                                            borderRadius: '8px',
                                            border: selectedReport === report.id ? '2px solid #6366F1' : '2px solid transparent',
                                            transition: 'all 0.2s ease'
                                        }}
                                    >
                                        <Row align="middle" gutter={16}>
                                            <Col>{report.icon}</Col>
                                            <Col flex="1">
                                                <Text strong>{report.name}</Text>
                                                <br />
                                                <Text type="secondary" style={{ fontSize: '0.875rem' }}>
                                                    {report.description}
                                                </Text>
                                            </Col>
                                            <Col>
                                                <Text type="secondary">{report.pages}</Text>
                                            </Col>
                                        </Row>
                                    </Radio>
                                ))}
                            </Space>
                        </Radio.Group>

                        <Divider />

                        <Title level={5}>Report Options</Title>
                        <Row gutter={16} align="middle">
                            <Col>
                                <Text>Language: </Text>
                                <Select
                                    value={language}
                                    onChange={setLanguage}
                                    style={{ width: 150 }}
                                    options={[
                                        { value: 'en', label: 'English' },
                                        { value: 'hi', label: 'हिंदी (Hindi)' },
                                    ]}
                                />
                            </Col>
                        </Row>

                        <Divider />

                        <Space>
                            <Button
                                type="primary"
                                size="large"
                                icon={generating ? <Spin size="small" /> : <FilePdfOutlined />}
                                onClick={handleGenerate}
                                disabled={generating}
                            >
                                {generating ? 'Generating...' : 'Generate Report'}
                            </Button>
                            <Button size="large" icon={<PrinterOutlined />}>Print Preview</Button>
                            <Button size="large" icon={<ShareAltOutlined />}>Share</Button>
                        </Space>
                    </Card>
                </Col>

                <Col xs={24} lg={8}>
                    <Card className="card">
                        <Title level={5}>Recent Reports</Title>
                        <Space direction="vertical" style={{ width: '100%' }}>
                            {generatedReports.map((report, index) => (
                                <div
                                    key={index}
                                    style={{
                                        display: 'flex',
                                        justifyContent: 'space-between',
                                        alignItems: 'center',
                                        padding: '0.75rem',
                                        background: '#F9FAFB',
                                        borderRadius: '8px'
                                    }}
                                >
                                    <div>
                                        <Text strong style={{ fontSize: '0.875rem' }}>{report.name}</Text>
                                        <br />
                                        <Text type="secondary" style={{ fontSize: '0.75rem' }}>
                                            {report.date} • {report.size}
                                        </Text>
                                    </div>
                                    <Button type="link" icon={<DownloadOutlined />} size="small">
                                        Download
                                    </Button>
                                </div>
                            ))}
                        </Space>
                    </Card>

                    <Card className="card" style={{ marginTop: '1rem' }}>
                        <Title level={5}><GlobalOutlined /> Multilingual Support</Title>
                        <Paragraph type="secondary" style={{ fontSize: '0.875rem' }}>
                            Generate reports in multiple languages:
                        </Paragraph>
                        <Space direction="vertical">
                            <Text>• English (Default)</Text>
                            <Text>• हिंदी (Hindi)</Text>
                        </Space>
                    </Card>
                </Col>
            </Row>
        </div>
    )
}
