"""
Data validation for financial data ingestion.
Ensures data integrity and consistency.
"""
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, date
import re
from pydantic import BaseModel, validator, ValidationError
from enum import Enum


class ValidationSeverity(Enum):
    """Severity levels for validation issues."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ValidationIssue(BaseModel):
    """Represents a validation issue."""
    field: str
    message: str
    severity: ValidationSeverity
    value: Optional[Any] = None
    suggestion: Optional[str] = None


class FinancialDataValidator:
    """Validates financial data for integrity and consistency."""
    
    # Valid Industry types
    VALID_INDUSTRIES = [
        'manufacturing', 'retail', 'agriculture', 'services',
        'logistics', 'ecommerce', 'healthcare', 'construction', 'other'
    ]
    
    # GST format regex (15 characters)
    GSTIN_PATTERN = re.compile(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$')
    
    # PAN format regex (10 characters)
    PAN_PATTERN = re.compile(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$')
    
    def __init__(self):
        self.issues: List[ValidationIssue] = []
    
    def validate_business_data(self, data: Dict) -> Tuple[bool, List[ValidationIssue]]:
        """
        Validate business registration data.
        
        Args:
            data: Business data dictionary
        
        Returns:
            Tuple of (is_valid, list of issues)
        """
        self.issues = []
        
        # Required fields
        required_fields = ['name']
        for field in required_fields:
            if not data.get(field):
                self.issues.append(ValidationIssue(
                    field=field,
                    message=f"Required field '{field}' is missing",
                    severity=ValidationSeverity.ERROR
                ))
        
        # Validate GSTIN if provided
        gstin = data.get('gstin')
        if gstin:
            if not self.GSTIN_PATTERN.match(gstin.upper()):
                self.issues.append(ValidationIssue(
                    field='gstin',
                    message="Invalid GSTIN format",
                    severity=ValidationSeverity.ERROR,
                    value=gstin,
                    suggestion="GSTIN should be 15 characters like 22AAAAA0000A1Z5"
                ))
        
        # Validate PAN if provided
        pan = data.get('pan')
        if pan:
            if not self.PAN_PATTERN.match(pan.upper()):
                self.issues.append(ValidationIssue(
                    field='pan',
                    message="Invalid PAN format",
                    severity=ValidationSeverity.ERROR,
                    value=pan,
                    suggestion="PAN should be 10 characters like AAAAA0000A"
                ))
        
        # Validate industry
        industry = data.get('industry', '').lower()
        if industry and industry not in self.VALID_INDUSTRIES:
            self.issues.append(ValidationIssue(
                field='industry',
                message=f"Unknown industry type: {industry}",
                severity=ValidationSeverity.WARNING,
                value=industry,
                suggestion=f"Valid industries: {', '.join(self.VALID_INDUSTRIES)}"
            ))
        
        # Validate email if provided
        email = data.get('email')
        if email and not self._is_valid_email(email):
            self.issues.append(ValidationIssue(
                field='email',
                message="Invalid email format",
                severity=ValidationSeverity.WARNING,
                value=email
            ))
        
        is_valid = not any(i.severity == ValidationSeverity.ERROR for i in self.issues)
        return is_valid, self.issues
    
    def validate_financial_statement(self, data: Dict) -> Tuple[bool, List[ValidationIssue]]:
        """
        Validate financial statement data.
        
        Args:
            data: Financial statement data
        
        Returns:
            Tuple of (is_valid, list of issues)
        """
        self.issues = []
        
        # Check for required date fields
        period_start = data.get('period_start')
        period_end = data.get('period_end')
        
        if not period_start:
            self.issues.append(ValidationIssue(
                field='period_start',
                message="Period start date is required",
                severity=ValidationSeverity.ERROR
            ))
        
        if not period_end:
            self.issues.append(ValidationIssue(
                field='period_end',
                message="Period end date is required",
                severity=ValidationSeverity.ERROR
            ))
        
        # Validate date range
        if period_start and period_end:
            try:
                start = self._parse_date(period_start)
                end = self._parse_date(period_end)
                
                if start > end:
                    self.issues.append(ValidationIssue(
                        field='period_start',
                        message="Period start date cannot be after end date",
                        severity=ValidationSeverity.ERROR,
                        value=f"{period_start} to {period_end}"
                    ))
                
                # Check if dates are in the future
                if end > date.today():
                    self.issues.append(ValidationIssue(
                        field='period_end',
                        message="Period end date is in the future",
                        severity=ValidationSeverity.WARNING,
                        value=str(period_end)
                    ))
                    
            except ValueError as e:
                self.issues.append(ValidationIssue(
                    field='period_start',
                    message=f"Invalid date format: {str(e)}",
                    severity=ValidationSeverity.ERROR
                ))
        
        # Validate numeric data if present
        financial_data = data.get('financial_data', {})
        self._validate_financial_values(financial_data)
        
        is_valid = not any(i.severity == ValidationSeverity.ERROR for i in self.issues)
        return is_valid, self.issues
    
    def validate_transaction_data(self, transactions: List[Dict]) -> Tuple[bool, List[ValidationIssue]]:
        """
        Validate transaction records.
        
        Args:
            transactions: List of transaction dictionaries
        
        Returns:
            Tuple of (is_valid, list of issues)
        """
        self.issues = []
        
        if not transactions:
            self.issues.append(ValidationIssue(
                field='transactions',
                message="No transactions provided",
                severity=ValidationSeverity.WARNING
            ))
            return True, self.issues
        
        for i, txn in enumerate(transactions):
            # Check for required fields
            if not txn.get('amount') and txn.get('amount') != 0:
                self.issues.append(ValidationIssue(
                    field=f'transactions[{i}].amount',
                    message="Transaction amount is required",
                    severity=ValidationSeverity.ERROR
                ))
            
            # Validate amount is numeric
            amount = txn.get('amount')
            if amount is not None:
                try:
                    float(amount)
                except (ValueError, TypeError):
                    self.issues.append(ValidationIssue(
                        field=f'transactions[{i}].amount',
                        message="Transaction amount must be numeric",
                        severity=ValidationSeverity.ERROR,
                        value=amount
                    ))
            
            # Check for transaction date
            if not txn.get('date') and not txn.get('transaction_date'):
                self.issues.append(ValidationIssue(
                    field=f'transactions[{i}].date',
                    message="Transaction date is missing",
                    severity=ValidationSeverity.WARNING
                ))
        
        is_valid = not any(i.severity == ValidationSeverity.ERROR for i in self.issues)
        return is_valid, self.issues
    
    def validate_invoice_data(self, invoice: Dict) -> Tuple[bool, List[ValidationIssue]]:
        """
        Validate invoice data.
        
        Args:
            invoice: Invoice dictionary
        
        Returns:
            Tuple of (is_valid, list of issues)
        """
        self.issues = []
        
        # Required fields
        required = ['invoice_number', 'invoice_type', 'total_amount']
        for field in required:
            if not invoice.get(field):
                self.issues.append(ValidationIssue(
                    field=field,
                    message=f"Required field '{field}' is missing",
                    severity=ValidationSeverity.ERROR
                ))
        
        # Validate invoice type
        invoice_type = invoice.get('invoice_type', '').lower()
        if invoice_type and invoice_type not in ['receivable', 'payable']:
            self.issues.append(ValidationIssue(
                field='invoice_type',
                message="Invoice type must be 'receivable' or 'payable'",
                severity=ValidationSeverity.ERROR,
                value=invoice_type
            ))
        
        # Validate amounts
        total = invoice.get('total_amount', 0)
        subtotal = invoice.get('subtotal', 0)
        tax = invoice.get('tax_amount', 0)
        
        if total and subtotal and tax:
            try:
                if abs(float(total) - (float(subtotal) + float(tax))) > 0.01:
                    self.issues.append(ValidationIssue(
                        field='total_amount',
                        message="Total amount doesn't match subtotal + tax",
                        severity=ValidationSeverity.WARNING,
                        value=f"Total: {total}, Subtotal: {subtotal}, Tax: {tax}"
                    ))
            except (ValueError, TypeError):
                pass
        
        # Validate party GSTIN if provided
        party_gstin = invoice.get('party_gstin')
        if party_gstin and not self.GSTIN_PATTERN.match(party_gstin.upper()):
            self.issues.append(ValidationIssue(
                field='party_gstin',
                message="Invalid party GSTIN format",
                severity=ValidationSeverity.WARNING,
                value=party_gstin
            ))
        
        is_valid = not any(i.severity == ValidationSeverity.ERROR for i in self.issues)
        return is_valid, self.issues
    
    def _validate_financial_values(self, data: Dict, prefix: str = ''):
        """Recursively validate financial values in nested dict."""
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                self._validate_financial_values(value, full_key)
            elif isinstance(value, (int, float)):
                # Check for suspiciously large values
                if abs(value) > 1e15:
                    self.issues.append(ValidationIssue(
                        field=full_key,
                        message="Unusually large value detected",
                        severity=ValidationSeverity.WARNING,
                        value=value
                    ))
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format."""
        pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return bool(pattern.match(email))
    
    def _parse_date(self, date_value) -> date:
        """Parse various date formats to date object."""
        if isinstance(date_value, date):
            return date_value
        if isinstance(date_value, datetime):
            return date_value.date()
        if isinstance(date_value, str):
            # Try common formats
            for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%Y/%m/%d']:
                try:
                    return datetime.strptime(date_value, fmt).date()
                except ValueError:
                    continue
            raise ValueError(f"Unable to parse date: {date_value}")
        raise ValueError(f"Invalid date type: {type(date_value)}")
    
    def get_validation_summary(self) -> Dict:
        """Get summary of validation issues."""
        return {
            'total_issues': len(self.issues),
            'errors': len([i for i in self.issues if i.severity == ValidationSeverity.ERROR]),
            'warnings': len([i for i in self.issues if i.severity == ValidationSeverity.WARNING]),
            'info': len([i for i in self.issues if i.severity == ValidationSeverity.INFO]),
            'issues': [i.dict() for i in self.issues]
        }


# Create global instance
data_validator = FinancialDataValidator()
