# Financial Health Assessment Platform

AI-powered financial health assessment platform for Small and Medium Enterprises (SMEs).

## Features

- **Multi-format Data Ingestion**: Upload CSV, Excel, and PDF financial documents
- **Comprehensive Financial Analysis**: 20+ financial ratios across liquidity, profitability, solvency, and efficiency
- **AI-Powered Insights**: OpenAI-powered insights and actionable recommendations
- **Risk Assessment**: Identify and categorize financial risks with severity scoring
- **Credit Scoring**: 300-900 credit score with A-D rating system
- **Financial Forecasting**: Revenue, expense, and cash flow projections
- **Industry Benchmarking**: Compare metrics against industry standards
- **GST Compliance**: Mock GST API integration for compliance checking
- **Banking Integrations**: Mock bank and NBFC APIs for loan products
- **Multilingual Support**: English and Hindi (हिंदी)
- **Investor-Ready Reports**: Professional PDF reports
- **Automated Bookkeeping**: Transaction categorization and reconciliation

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL (SQLite for development)
- **ORM**: SQLAlchemy
- **Authentication**: JWT with bcrypt
- **Encryption**: AES-256 (Fernet)
- **AI**: OpenAI GPT

### Frontend
- **Framework**: React.js with Vite
- **UI Library**: Ant Design
- **Charts**: Recharts
- **HTTP Client**: Axios

## Project Structure

```
Financial Health Assessment Tool/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment variables template
│   ├── database/               # Database models and connection
│   ├── security/               # Authentication and encryption
│   ├── ingestion/              # Document parsing (CSV, Excel, PDF)
│   ├── analysis/               # Financial metrics and risk assessment
│   ├── ai/                     # OpenAI integration
│   ├── compliance/             # GST and tax compliance
│   ├── integrations/           # Banking API integrations
│   ├── reports/                # PDF generation and bookkeeping
│   ├── i18n/                   # Multilingual translations
│   └── routes/                 # API endpoints
│
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── main.jsx            # React entry point
        ├── App.jsx             # Main application component
        ├── styles/             # CSS styles
        ├── pages/              # Page components
        └── services/           # API services
```

## Quick Start

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
copy .env.example .env
# Edit .env with your settings

# Run the server
python main.py
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=sqlite:///./financial_health.db

# Security
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=  # Auto-generated if not provided

# AI
OPENAI_API_KEY=your-openai-api-key

# App Settings
DEBUG=true
```

## API Documentation

Once the backend is running, access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Key API Endpoints

### Upload
- `POST /api/upload/document` - Upload financial documents
- `POST /api/upload/validate` - Validate uploaded data

### Analysis
- `POST /api/analysis/full` - Full financial analysis
- `POST /api/analysis/metrics` - Calculate financial metrics
- `POST /api/analysis/risk` - Risk assessment
- `POST /api/analysis/credit-score` - Credit scoring
- `POST /api/analysis/forecast` - Financial forecasting
- `POST /api/analysis/benchmark` - Industry benchmarking

### Reports
- `POST /api/reports/generate` - Generate PDF report
- `GET /api/reports/download/{filename}` - Download report

### Integrations
- `GET /api/integrations/gst/verify/{gstin}` - Verify GSTIN
- `GET /api/integrations/gst/compliance/{gstin}` - Check GST compliance
- `POST /api/integrations/bank/loan-products` - Get loan products

## Industries Supported

- Manufacturing
- Retail
- Agriculture
- Services
- Logistics
- E-commerce
- Healthcare
- Construction

## Security Features

- AES-256 encryption for sensitive data at rest
- JWT authentication with short-lived tokens
- bcrypt password hashing
- HTTPS/TLS for data in transit
- Role-based access control (Admin, Analyst, User)
- Audit logging

## License

MIT License
