"""
Integration routes for banking and GST APIs.
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import date, timedelta

from integrations import bank_api_1, nbfc_api
from compliance import gst_integration, tax_checker
from ai import llm_engine

router = APIRouter(prefix="/integrations", tags=["Integrations"])


# Banking APIs
@router.post("/bank/connect")
async def connect_bank(
    account_number: str,
    bank_id: str = "bank1"
):
    """Connect to a bank API."""
    if bank_id == "bank1":
        success = bank_api_1.connect(account_number, "mock_api_key")
    else:
        success = nbfc_api.connect(account_number, "mock_api_key")
    
    return {'connected': success, 'bank_id': bank_id}


@router.get("/bank/balance/{account_number}")
async def get_bank_balance(account_number: str):
    """Get bank account balance."""
    return bank_api_1.get_account_balance(account_number)


@router.get("/bank/transactions/{account_number}")
async def get_bank_transactions(
    account_number: str,
    days: int = 30
):
    """Get bank transactions."""
    to_date = date.today()
    from_date = to_date - timedelta(days=days)
    return bank_api_1.get_transactions(account_number, from_date, to_date)


@router.post("/bank/loan-products")
async def get_loan_products(business_profile: dict):
    """Get available loan products from banks."""
    bank_products = bank_api_1.get_loan_products(business_profile)
    nbfc_products = nbfc_api.get_working_capital_products(business_profile)
    
    return {
        'bank_products': bank_products,
        'nbfc_products': nbfc_products,
        'total_options': len(bank_products) + len(nbfc_products)
    }


@router.post("/bank/invoice-financing")
async def get_invoice_financing(invoices: list):
    """Get invoice financing options."""
    return nbfc_api.get_invoice_financing_options(invoices)


@router.post("/bank/product-recommendations")
async def get_product_recommendations(
    credit_score: dict,
    financial_needs: dict,
    industry: str = "services"
):
    """Get AI-powered financial product recommendations."""
    return llm_engine.suggest_financial_products(credit_score, financial_needs, industry)


# GST Integration
@router.get("/gst/verify/{gstin}")
async def verify_gstin(gstin: str):
    """Verify GSTIN and get details."""
    return gst_integration.verify_gstin(gstin)


@router.get("/gst/filing-status/{gstin}")
async def get_gst_filing_status(gstin: str, financial_year: str = "2023-24"):
    """Get GST filing status."""
    return gst_integration.get_filing_status(gstin, financial_year)


@router.get("/gst/tax-liability/{gstin}")
async def get_gst_tax_liability(gstin: str, period: str):
    """Get GST tax liability for a period."""
    return gst_integration.get_tax_liability(gstin, period)


@router.get("/gst/compliance/{gstin}")
async def check_gst_compliance(gstin: str):
    """Check overall GST compliance status."""
    return gst_integration.check_compliance(gstin)


# Tax Compliance
@router.post("/tax/check-compliance")
async def check_tax_compliance(
    business_data: dict,
    tax_records: list = []
):
    """Check overall tax compliance."""
    return tax_checker.check_all_compliance(business_data, tax_records)


@router.post("/tax/optimization")
async def get_tax_optimization(financial_data: dict):
    """Get tax optimization suggestions."""
    return tax_checker.get_tax_optimization_suggestions(financial_data)
