"""
Reports routes for generating and downloading reports.
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import Optional
import os

from reports import pdf_generator, bookkeeping_assistant
from i18n import translator

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/generate")
async def generate_report(
    business: dict,
    analysis: dict,
    report_type: str = "full",
    language: str = "en"
):
    """Generate a financial report."""
    try:
        if report_type == "full":
            filepath = pdf_generator.generate_full_report(business, analysis, language)
        elif report_type == "quick":
            filepath = pdf_generator.generate_quick_report(
                business, analysis.get('health_score', {})
            )
        else:
            raise HTTPException(400, "Invalid report type. Use 'full' or 'quick'")
        
        return {
            'status': 'generated',
            'filepath': filepath,
            'filename': os.path.basename(filepath),
            'type': report_type,
            'language': language
        }
        
    except Exception as e:
        raise HTTPException(500, f"Report generation error: {str(e)}")


@router.get("/download/{filename}")
async def download_report(filename: str):
    """Download a generated report."""
    filepath = os.path.join(pdf_generator.output_dir, filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(404, "Report not found")
    
    return FileResponse(
        filepath,
        media_type='application/pdf',
        filename=filename
    )


@router.post("/bookkeeping/categorize")
async def categorize_transaction(
    description: str,
    amount: float,
    is_credit: bool = False
):
    """Categorize a transaction."""
    return bookkeeping_assistant.categorize_transaction(description, amount, is_credit)


@router.post("/bookkeeping/journal-entry")
async def generate_journal_entry(transaction: dict):
    """Generate journal entry for a transaction."""
    return bookkeeping_assistant.generate_journal_entry(transaction)


@router.post("/bookkeeping/reconcile")
async def reconcile_accounts(
    ledger_balance: float,
    bank_balance: float
):
    """Reconcile account balances."""
    return bookkeeping_assistant.reconcile_accounts(ledger_balance, bank_balance)


@router.post("/bookkeeping/trial-balance")
async def generate_trial_balance(accounts: list):
    """Generate trial balance from accounts."""
    return bookkeeping_assistant.generate_trial_balance(accounts)
