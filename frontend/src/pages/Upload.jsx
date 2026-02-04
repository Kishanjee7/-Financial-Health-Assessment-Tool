import { useState } from 'react'
import {
    Upload as AntUpload,
    Card,
    Typography,
    Steps,
    Button,
    Table,
    Tag,
    Space,
    message,
    Alert,
    Row,
    Col
} from 'antd'
import {
    InboxOutlined,
    FileExcelOutlined,
    FilePdfOutlined,
    FileTextOutlined,
    CheckCircleOutlined,
    LoadingOutlined,
} from '@ant-design/icons'

const { Title, Text, Paragraph } = Typography
const { Dragger } = AntUpload

const supportedFormats = [
    { ext: '.csv', icon: <FileTextOutlined style={{ color: '#10B981' }} />, name: 'CSV Files' },
    { ext: '.xlsx', icon: <FileExcelOutlined style={{ color: '#107C41' }} />, name: 'Excel Files' },
    { ext: '.xls', icon: <FileExcelOutlined style={{ color: '#107C41' }} />, name: 'Excel (Legacy)' },
    { ext: '.pdf', icon: <FilePdfOutlined style={{ color: '#EF4444' }} />, name: 'PDF Documents' },
]

export default function Upload() {
    const [currentStep, setCurrentStep] = useState(0)
    const [uploadedFiles, setUploadedFiles] = useState([])
    const [processing, setProcessing] = useState(false)
    const [extractedData, setExtractedData] = useState(null)

    // Mock extracted data for demonstration
    const mockExtractedData = {
        income_statement: {
            revenue: 54000000,
            cogs: 32400000,
            gross_profit: 21600000,
            operating_expenses: 12960000,
            net_income: 8640000
        },
        balance_sheet: {
            total_assets: 125000000,
            current_assets: 45000000,
            total_liabilities: 50000000,
            current_liabilities: 24000000,
            equity: 75000000
        }
    }

    // Custom upload handler - simulates upload with mock data for demo
    const customUpload = async ({ file, onSuccess, onError }) => {
        setProcessing(true)

        // Simulate processing delay
        await new Promise(resolve => setTimeout(resolve, 1500))

        try {
            // Try to upload to actual backend first
            const formData = new FormData()
            formData.append('file', file)

            const response = await fetch('/api/upload/document', {
                method: 'POST',
                body: formData
            })

            if (response.ok) {
                const data = await response.json()
                onSuccess(data)
                return
            }
            throw new Error('Backend not available')
        } catch (error) {
            // Fallback to mock data for demo mode
            console.log('Using demo mode with mock data')
            onSuccess({
                extracted_data: mockExtractedData,
                demo_mode: true
            })
        }
    }

    const handleUpload = async (info) => {
        const { status, name, response } = info.file

        if (status === 'done') {
            setProcessing(false)
            const isDemoMode = response?.demo_mode
            message.success(
                isDemoMode
                    ? `${name} processed in demo mode with sample data`
                    : `${name} uploaded and processed successfully`
            )
            setUploadedFiles(prev => [...prev, {
                name,
                status: 'processed',
                demoMode: isDemoMode
            }])
            setCurrentStep(1)
            setExtractedData(response?.extracted_data || mockExtractedData)
        } else if (status === 'error') {
            setProcessing(false)
            message.error(`${name} upload failed.`)
        }
    }

    const uploadProps = {
        name: 'file',
        multiple: true,
        customRequest: customUpload,
        accept: '.csv,.xlsx,.xls,.pdf',
        onChange: handleUpload,
        showUploadList: false,
    }


    const extractedColumns = [
        { title: 'Item', dataIndex: 'item', key: 'item' },
        { title: 'Value', dataIndex: 'value', key: 'value', render: (val) => `₹${(val / 100000).toFixed(2)}L` },
    ]

    const getExtractedTableData = () => {
        if (!extractedData) return []
        const data = []

        if (extractedData.income_statement) {
            Object.entries(extractedData.income_statement).forEach(([key, value]) => {
                data.push({
                    key: `income_${key}`,
                    item: key.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
                    value,
                    category: 'Income Statement'
                })
            })
        }

        if (extractedData.balance_sheet) {
            Object.entries(extractedData.balance_sheet).forEach(([key, value]) => {
                data.push({
                    key: `balance_${key}`,
                    item: key.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
                    value,
                    category: 'Balance Sheet'
                })
            })
        }

        return data
    }

    return (
        <div className="fade-in">
            <Title level={2}>Upload Financial Documents</Title>
            <Text type="secondary" style={{ marginBottom: '2rem', display: 'block' }}>
                Upload your financial statements for AI-powered analysis
            </Text>

            <Steps
                current={currentStep}
                style={{ marginBottom: '2rem' }}
                items={[
                    { title: 'Upload Documents', icon: processing ? <LoadingOutlined /> : undefined },
                    { title: 'Review Data' },
                    { title: 'Run Analysis' },
                ]}
            />

            <Row gutter={24}>
                <Col xs={24} lg={14}>
                    <Card className="card">
                        <Dragger {...uploadProps} className="upload-zone">
                            <p className="ant-upload-drag-icon">
                                <InboxOutlined style={{ fontSize: '3rem', color: '#6366F1' }} />
                            </p>
                            <p className="ant-upload-text" style={{ fontSize: '1.125rem', fontWeight: 500 }}>
                                Click or drag files to upload
                            </p>
                            <p className="ant-upload-hint" style={{ color: '#6B7280' }}>
                                Support for CSV, Excel, and PDF files. Max size: 10MB per file.
                            </p>
                        </Dragger>

                        <div style={{ marginTop: '1.5rem' }}>
                            <Text strong>Supported Formats:</Text>
                            <Row gutter={16} style={{ marginTop: '0.75rem' }}>
                                {supportedFormats.map(format => (
                                    <Col span={6} key={format.ext}>
                                        <div style={{
                                            textAlign: 'center',
                                            padding: '1rem',
                                            background: '#F9FAFB',
                                            borderRadius: '8px'
                                        }}>
                                            <div style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>{format.icon}</div>
                                            <div style={{ fontSize: '0.75rem', color: '#6B7280' }}>{format.name}</div>
                                        </div>
                                    </Col>
                                ))}
                            </Row>
                        </div>
                    </Card>

                    {uploadedFiles.length > 0 && (
                        <Card className="card" style={{ marginTop: '1rem' }}>
                            <Text strong>Uploaded Files</Text>
                            <div style={{ marginTop: '1rem' }}>
                                {uploadedFiles.map((file, index) => (
                                    <div
                                        key={index}
                                        style={{
                                            display: 'flex',
                                            justifyContent: 'space-between',
                                            alignItems: 'center',
                                            padding: '0.75rem',
                                            background: '#F0FDF4',
                                            borderRadius: '8px',
                                            marginBottom: '0.5rem'
                                        }}
                                    >
                                        <Space>
                                            <CheckCircleOutlined style={{ color: '#10B981' }} />
                                            <Text>{file.name}</Text>
                                        </Space>
                                        <Tag color="green">Processed</Tag>
                                    </div>
                                ))}
                            </div>
                        </Card>
                    )}
                </Col>

                <Col xs={24} lg={10}>
                    <Card className="card">
                        <Title level={5}>Document Types</Title>
                        <Paragraph type="secondary" style={{ fontSize: '0.875rem' }}>
                            We accept the following financial documents:
                        </Paragraph>

                        <Space direction="vertical" style={{ width: '100%' }}>
                            {[
                                'Profit & Loss Statement',
                                'Balance Sheet',
                                'Cash Flow Statement',
                                'Bank Statements',
                                'Trial Balance',
                                'GST Returns'
                            ].map((doc, i) => (
                                <div
                                    key={i}
                                    style={{
                                        padding: '0.75rem',
                                        background: '#F9FAFB',
                                        borderRadius: '8px',
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '0.5rem'
                                    }}
                                >
                                    <CheckCircleOutlined style={{ color: '#6366F1' }} />
                                    <Text>{doc}</Text>
                                </div>
                            ))}
                        </Space>
                    </Card>

                    {extractedData && (
                        <Card className="card" style={{ marginTop: '1rem' }}>
                            <Title level={5}>Extracted Data Preview</Title>
                            <Table
                                dataSource={getExtractedTableData()}
                                columns={extractedColumns}
                                pagination={false}
                                size="small"
                            />

                            <Space style={{ marginTop: '1rem' }}>
                                <Button
                                    type="primary"
                                    onClick={() => {
                                        setCurrentStep(2)
                                        message.success('Analysis started!')
                                    }}
                                >
                                    Run Full Analysis
                                </Button>
                                <Button>Edit Data</Button>
                            </Space>
                        </Card>
                    )}
                </Col>
            </Row>
        </div>
    )
}
