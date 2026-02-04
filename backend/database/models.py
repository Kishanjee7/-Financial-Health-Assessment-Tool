"""
Database models for the Financial Health Assessment Platform.
All sensitive financial data is encrypted at rest.
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, DateTime, Date, ForeignKey, Text, 
    Integer, Float, Boolean, JSON, Enum as SQLEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum


Base = declarative_base()


def generate_uuid():
    """Generate a new UUID."""
    return str(uuid.uuid4())


class IndustryType(enum.Enum):
    """Industry classification for businesses."""
    MANUFACTURING = "manufacturing"
    RETAIL = "retail"
    AGRICULTURE = "agriculture"
    SERVICES = "services"
    LOGISTICS = "logistics"
    ECOMMERCE = "ecommerce"
    HEALTHCARE = "healthcare"
    CONSTRUCTION = "construction"
    OTHER = "other"


class StatementType(enum.Enum):
    """Types of financial statements."""
    INCOME_STATEMENT = "income_statement"
    BALANCE_SHEET = "balance_sheet"
    CASH_FLOW = "cash_flow"
    TRIAL_BALANCE = "trial_balance"


class RiskLevel(enum.Enum):
    """Risk level classification."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Business(Base):
    """Business entity representing an SME."""
    __tablename__ = "businesses"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False, index=True)
    legal_name = Column(String(255))
    industry = Column(String(50), default=IndustryType.OTHER.value)
    gstin = Column(String(15), unique=True, index=True)  # GST Identification Number
    pan = Column(String(10))  # PAN Number
    cin = Column(String(21))  # Company Identification Number
    incorporation_date = Column(Date)
    
    # Contact Information (encrypted)
    email = Column(String(255))
    phone = Column(String(20))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(10))
    
    # Business Details
    annual_turnover = Column(Float)  # Encrypted
    employee_count = Column(Integer)
    business_type = Column(String(50))  # Proprietorship, Partnership, Pvt Ltd, etc.
    
    # Banking Details (encrypted)
    bank_account_encrypted = Column(Text)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    financial_statements = relationship("FinancialStatement", back_populates="business", cascade="all, delete-orphan")
    cash_flows = relationship("CashFlow", back_populates="business", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="business", cascade="all, delete-orphan")
    inventory_items = relationship("Inventory", back_populates="business", cascade="all, delete-orphan")
    loans = relationship("LoanObligation", back_populates="business", cascade="all, delete-orphan")
    tax_records = relationship("TaxRecord", back_populates="business", cascade="all, delete-orphan")
    analysis_reports = relationship("AnalysisReport", back_populates="business", cascade="all, delete-orphan")


class FinancialStatement(Base):
    """Financial statements uploaded by businesses."""
    __tablename__ = "financial_statements"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    business_id = Column(String(36), ForeignKey("businesses.id"), nullable=False)
    
    statement_type = Column(String(50), nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    
    # Encrypted financial data stored as JSON
    data_encrypted = Column(Text, nullable=False)
    
    # Source file information
    source_filename = Column(String(255))
    source_format = Column(String(10))  # csv, xlsx, pdf
    
    # Metadata
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False)
    
    # Relationships
    business = relationship("Business", back_populates="financial_statements")


class CashFlow(Base):
    """Cash flow transactions and patterns."""
    __tablename__ = "cash_flows"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    business_id = Column(String(36), ForeignKey("businesses.id"), nullable=False)
    
    transaction_date = Column(Date, nullable=False)
    category = Column(String(100))  # Operating, Investing, Financing
    subcategory = Column(String(100))
    description = Column(Text)
    
    # Amount (encrypted for sensitive transactions)
    amount = Column(Float, nullable=False)
    is_inflow = Column(Boolean, nullable=False)
    
    # Source
    source = Column(String(50))  # bank_api, manual, imported
    reference_id = Column(String(100))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="cash_flows")


class Invoice(Base):
    """Accounts receivable and payable."""
    __tablename__ = "invoices"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    business_id = Column(String(36), ForeignKey("businesses.id"), nullable=False)
    
    invoice_number = Column(String(50), nullable=False)
    invoice_type = Column(String(20), nullable=False)  # receivable, payable
    
    party_name = Column(String(255))
    party_gstin = Column(String(15))
    
    invoice_date = Column(Date, nullable=False)
    due_date = Column(Date)
    
    # Amounts
    subtotal = Column(Float, nullable=False)
    tax_amount = Column(Float, default=0)
    total_amount = Column(Float, nullable=False)
    paid_amount = Column(Float, default=0)
    
    # Status
    status = Column(String(20), default="pending")  # pending, partial, paid, overdue
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="invoices")


class Inventory(Base):
    """Inventory levels for applicable businesses."""
    __tablename__ = "inventory"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    business_id = Column(String(36), ForeignKey("businesses.id"), nullable=False)
    
    item_code = Column(String(50), nullable=False)
    item_name = Column(String(255), nullable=False)
    category = Column(String(100))
    
    quantity = Column(Float, nullable=False)
    unit = Column(String(20))
    unit_cost = Column(Float)
    total_value = Column(Float)
    
    reorder_level = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="inventory_items")


class LoanObligation(Base):
    """Loans and credit obligations."""
    __tablename__ = "loan_obligations"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    business_id = Column(String(36), ForeignKey("businesses.id"), nullable=False)
    
    lender_name = Column(String(255), nullable=False)
    lender_type = Column(String(50))  # bank, nbfc, private
    loan_type = Column(String(50))  # term_loan, working_capital, overdraft, etc.
    
    principal_amount = Column(Float, nullable=False)
    outstanding_amount = Column(Float, nullable=False)
    interest_rate = Column(Float)
    
    start_date = Column(Date)
    end_date = Column(Date)
    emi_amount = Column(Float)
    
    # Security/Collateral
    is_secured = Column(Boolean, default=False)
    collateral_description = Column(Text)
    
    status = Column(String(20), default="active")  # active, closed, defaulted
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="loans")


class TaxRecord(Base):
    """Tax records and compliance data."""
    __tablename__ = "tax_records"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    business_id = Column(String(36), ForeignKey("businesses.id"), nullable=False)
    
    tax_type = Column(String(50), nullable=False)  # gst, income_tax, tds
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    
    # GST specific
    gstr_type = Column(String(10))  # GSTR-1, GSTR-3B, etc.
    filing_date = Column(Date)
    
    # Amounts
    tax_liability = Column(Float)
    tax_paid = Column(Float)
    input_credit = Column(Float)
    
    # Compliance status
    is_filed = Column(Boolean, default=False)
    is_compliant = Column(Boolean, default=True)
    compliance_issues = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="tax_records")


class AnalysisReport(Base):
    """Generated analysis reports and insights."""
    __tablename__ = "analysis_reports"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    business_id = Column(String(36), ForeignKey("businesses.id"), nullable=False)
    
    report_type = Column(String(50), nullable=False)  # full, quick, investor
    language = Column(String(5), default="en")
    
    # Health Score (0-100)
    overall_health_score = Column(Float)
    liquidity_score = Column(Float)
    profitability_score = Column(Float)
    solvency_score = Column(Float)
    efficiency_score = Column(Float)
    growth_score = Column(Float)
    
    # Detailed Analysis (JSON)
    financial_ratios = Column(JSON)
    risk_assessment = Column(JSON)
    creditworthiness = Column(JSON)
    recommendations = Column(JSON)
    industry_benchmark = Column(JSON)
    
    # AI-generated insights
    ai_summary = Column(Text)
    ai_recommendations = Column(JSON)
    
    # Forecasting
    forecast_data = Column(JSON)
    
    # Report file
    pdf_path = Column(String(500))
    
    generated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="analysis_reports")


class User(Base):
    """User accounts for authentication."""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    full_name = Column(String(255))
    phone = Column(String(20))
    
    # Associated businesses
    business_ids = Column(JSON, default=list)
    
    # Role
    role = Column(String(20), default="user")  # user, admin, analyst
    
    # Preferences
    preferred_language = Column(String(5), default="en")
    
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)


class AuditLog(Base):
    """Audit trail for security and compliance."""
    __tablename__ = "audit_logs"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"))
    business_id = Column(String(36), ForeignKey("businesses.id"))
    
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(String(36))
    
    details = Column(JSON)
    ip_address = Column(String(45))
    
    created_at = Column(DateTime, default=datetime.utcnow)
