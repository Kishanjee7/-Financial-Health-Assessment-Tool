"""
Upload routes for document processing.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List, Optional
import os
import uuid
from datetime import datetime

from config import settings
from security.auth import get_current_user, TokenData
from ingestion import csv_handler, excel_handler, pdf_handler, data_validator
from security.encryption import encrypt_data

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/document")
async def upload_document(
    file: UploadFile = File(...),
    business_id: Optional[str] = None,
    statement_type: Optional[str] = None
):
    """Upload a financial document for processing."""
    # Validate file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Unsupported file format. Allowed: {settings.ALLOWED_EXTENSIONS}")
    
    # Read file content
    content = await file.read()
    
    # Check file size
    if len(content) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(400, f"File too large. Maximum: {settings.MAX_UPLOAD_SIZE_MB}MB")
    
    # Process based on file type
    try:
        if ext == '.csv':
            df, metadata = csv_handler.parse_file(content, file.filename)
            extracted_data = csv_handler.extract_financial_data(df, statement_type or 'generic')
        elif ext in ['.xlsx', '.xls']:
            sheets, metadata = excel_handler.parse_file(content, file.filename)
            extracted_data = excel_handler.extract_financial_data(sheets, metadata)
        elif ext == '.pdf':
            data, metadata = pdf_handler.parse_file(content, file.filename)
            extracted_data = pdf_handler.extract_financial_data(data, metadata)
        else:
            raise HTTPException(400, "Unsupported file format")
        
        # Generate document ID
        doc_id = str(uuid.uuid4())
        
        # Save file
        save_path = os.path.join(settings.UPLOAD_DIR, f"{doc_id}{ext}")
        with open(save_path, 'wb') as f:
            f.write(content)
        
        return {
            'document_id': doc_id,
            'filename': file.filename,
            'format': ext[1:],
            'metadata': metadata,
            'extracted_data': extracted_data,
            'status': 'processed',
            'uploaded_at': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error processing file: {str(e)}")


@router.post("/validate")
async def validate_data(data: dict):
    """Validate uploaded financial data."""
    data_type = data.get('type', 'generic')
    
    if data_type == 'business':
        is_valid, issues = data_validator.validate_business_data(data)
    elif data_type == 'financial_statement':
        is_valid, issues = data_validator.validate_financial_statement(data)
    elif data_type == 'invoice':
        is_valid, issues = data_validator.validate_invoice_data(data)
    elif data_type == 'transactions':
        is_valid, issues = data_validator.validate_transaction_data(data.get('transactions', []))
    else:
        return {'valid': True, 'issues': [], 'message': 'No validation rules for this data type'}
    
    return {
        'valid': is_valid,
        'issues': [{'field': i.field, 'message': i.message, 'severity': i.severity.value} for i in issues],
        'summary': data_validator.get_validation_summary()
    }


@router.get("/formats")
async def get_supported_formats():
    """Get list of supported file formats."""
    return {
        'supported_formats': settings.ALLOWED_EXTENSIONS,
        'max_size_mb': settings.MAX_UPLOAD_SIZE_MB,
        'document_types': [
            {'type': 'income_statement', 'description': 'Profit & Loss Statement'},
            {'type': 'balance_sheet', 'description': 'Balance Sheet'},
            {'type': 'cash_flow', 'description': 'Cash Flow Statement'},
            {'type': 'trial_balance', 'description': 'Trial Balance'},
            {'type': 'transactions', 'description': 'Bank/Transaction Statement'},
        ]
    }
