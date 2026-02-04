"""
CSV file handler for financial data ingestion.
Parses and validates CSV financial statements.
"""
import pandas as pd
import io
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import re


class CSVHandler:
    """Handles CSV file parsing and data extraction."""
    
    # Common column name mappings
    COLUMN_MAPPINGS = {
        # Date columns
        'date': ['date', 'transaction_date', 'txn_date', 'posting_date', 'value_date'],
        'period': ['period', 'month', 'quarter', 'fiscal_period'],
        
        # Amount columns
        'amount': ['amount', 'value', 'total', 'net_amount', 'gross_amount'],
        'debit': ['debit', 'dr', 'debit_amount', 'outflow'],
        'credit': ['credit', 'cr', 'credit_amount', 'inflow'],
        'balance': ['balance', 'running_balance', 'closing_balance'],
        
        # Revenue/Expense
        'revenue': ['revenue', 'sales', 'income', 'turnover', 'gross_sales'],
        'expense': ['expense', 'expenses', 'cost', 'expenditure'],
        'profit': ['profit', 'net_profit', 'net_income', 'earnings'],
        
        # Categories
        'category': ['category', 'type', 'account_type', 'ledger_group'],
        'subcategory': ['subcategory', 'sub_category', 'account_sub_type'],
        'description': ['description', 'particulars', 'narration', 'remarks'],
        
        # Account identifiers
        'account_code': ['account_code', 'ledger_code', 'gl_code', 'account_no'],
        'account_name': ['account_name', 'ledger_name', 'account', 'ledger'],
        
        # Invoice related
        'invoice_no': ['invoice_no', 'invoice_number', 'bill_no', 'voucher_no'],
        'party_name': ['party_name', 'customer_name', 'vendor_name', 'name'],
        'gstin': ['gstin', 'gst_no', 'gst_number'],
        
        # Tax related
        'tax_amount': ['tax_amount', 'gst_amount', 'tax', 'gst'],
        'cgst': ['cgst', 'cgst_amount'],
        'sgst': ['sgst', 'sgst_amount'],
        'igst': ['igst', 'igst_amount'],
    }
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def parse_file(
        self, 
        file_content: bytes, 
        filename: str,
        encoding: str = 'utf-8'
    ) -> Tuple[pd.DataFrame, Dict]:
        """
        Parse a CSV file and return structured data.
        
        Args:
            file_content: Raw file bytes
            filename: Original filename
            encoding: File encoding
        
        Returns:
            Tuple of (DataFrame, metadata dict)
        """
        self.errors = []
        self.warnings = []
        metadata = {
            'filename': filename,
            'format': 'csv',
            'parsed_at': datetime.utcnow().isoformat(),
            'row_count': 0,
            'column_mappings': {}
        }
        
        try:
            # Try to decode with specified encoding
            try:
                content_str = file_content.decode(encoding)
            except UnicodeDecodeError:
                # Try common encodings
                for enc in ['latin-1', 'cp1252', 'iso-8859-1']:
                    try:
                        content_str = file_content.decode(enc)
                        metadata['detected_encoding'] = enc
                        break
                    except:
                        continue
                else:
                    raise ValueError("Unable to decode file with any common encoding")
            
            # Parse CSV
            df = pd.read_csv(io.StringIO(content_str))
            
            # Clean column names
            df.columns = [self._clean_column_name(col) for col in df.columns]
            
            # Map columns to standard names
            column_mappings = self._map_columns(df.columns.tolist())
            metadata['column_mappings'] = column_mappings
            
            # Convert date columns
            df = self._convert_dates(df, column_mappings)
            
            # Convert numeric columns
            df = self._convert_numerics(df)
            
            metadata['row_count'] = len(df)
            metadata['columns'] = df.columns.tolist()
            metadata['errors'] = self.errors
            metadata['warnings'] = self.warnings
            
            return df, metadata
            
        except Exception as e:
            self.errors.append(f"Failed to parse CSV: {str(e)}")
            return pd.DataFrame(), metadata
    
    def _clean_column_name(self, name: str) -> str:
        """Clean and normalize column name."""
        if not isinstance(name, str):
            name = str(name)
        # Remove extra whitespace, convert to lowercase
        name = re.sub(r'\s+', '_', name.strip().lower())
        # Remove special characters except underscore
        name = re.sub(r'[^a-z0-9_]', '', name)
        return name
    
    def _map_columns(self, columns: List[str]) -> Dict[str, str]:
        """Map CSV columns to standard field names."""
        mappings = {}
        for standard_name, variations in self.COLUMN_MAPPINGS.items():
            for col in columns:
                if col in variations or any(v in col for v in variations):
                    mappings[standard_name] = col
                    break
        return mappings
    
    def _convert_dates(self, df: pd.DataFrame, mappings: Dict) -> pd.DataFrame:
        """Convert date columns to datetime."""
        date_columns = ['date', 'period']
        for date_col in date_columns:
            if date_col in mappings:
                col_name = mappings[date_col]
                try:
                    df[col_name] = pd.to_datetime(df[col_name], errors='coerce')
                except Exception as e:
                    self.warnings.append(f"Could not parse dates in {col_name}: {e}")
        return df
    
    def _convert_numerics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert numeric columns, handling currency formatting."""
        numeric_patterns = ['amount', 'debit', 'credit', 'balance', 'revenue', 
                          'expense', 'profit', 'tax', 'gst', 'cgst', 'sgst', 'igst']
        
        for col in df.columns:
            if any(pattern in col for pattern in numeric_patterns):
                try:
                    # Remove currency symbols and commas
                    if df[col].dtype == 'object':
                        df[col] = df[col].astype(str).str.replace(r'[₹$,\s]', '', regex=True)
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                except Exception as e:
                    self.warnings.append(f"Could not convert {col} to numeric: {e}")
        
        return df
    
    def extract_financial_data(
        self, 
        df: pd.DataFrame, 
        statement_type: str
    ) -> Dict:
        """
        Extract structured financial data from DataFrame.
        
        Args:
            df: Parsed DataFrame
            statement_type: Type of financial statement
        
        Returns:
            Structured financial data dictionary
        """
        if statement_type == 'income_statement':
            return self._extract_income_statement(df)
        elif statement_type == 'balance_sheet':
            return self._extract_balance_sheet(df)
        elif statement_type == 'cash_flow':
            return self._extract_cash_flow(df)
        elif statement_type == 'transactions':
            return self._extract_transactions(df)
        else:
            return self._extract_generic(df)
    
    def _extract_income_statement(self, df: pd.DataFrame) -> Dict:
        """Extract income statement data."""
        data = {
            'type': 'income_statement',
            'revenue': {},
            'expenses': {},
            'totals': {}
        }
        
        # Try to identify revenue and expense rows
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            # Logic to categorize rows would go here
            # This is a simplified version
        
        # Calculate totals if numeric columns exist
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            data['totals'][col] = float(df[col].sum())
        
        return data
    
    def _extract_balance_sheet(self, df: pd.DataFrame) -> Dict:
        """Extract balance sheet data."""
        data = {
            'type': 'balance_sheet',
            'assets': {},
            'liabilities': {},
            'equity': {},
            'totals': {}
        }
        
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            data['totals'][col] = float(df[col].sum())
        
        return data
    
    def _extract_cash_flow(self, df: pd.DataFrame) -> Dict:
        """Extract cash flow data."""
        data = {
            'type': 'cash_flow',
            'operating': {},
            'investing': {},
            'financing': {},
            'totals': {}
        }
        
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            data['totals'][col] = float(df[col].sum())
        
        return data
    
    def _extract_transactions(self, df: pd.DataFrame) -> Dict:
        """Extract transaction data."""
        transactions = []
        
        for _, row in df.iterrows():
            txn = row.to_dict()
            # Convert NaN to None for JSON serialization
            txn = {k: (None if pd.isna(v) else v) for k, v in txn.items()}
            # Convert datetime to string
            for k, v in txn.items():
                if isinstance(v, pd.Timestamp):
                    txn[k] = v.isoformat()
            transactions.append(txn)
        
        return {
            'type': 'transactions',
            'count': len(transactions),
            'transactions': transactions
        }
    
    def _extract_generic(self, df: pd.DataFrame) -> Dict:
        """Extract generic data when type is unknown."""
        return {
            'type': 'generic',
            'row_count': len(df),
            'columns': df.columns.tolist(),
            'summary': df.describe().to_dict(),
            'sample': df.head(10).to_dict(orient='records')
        }


# Create global instance
csv_handler = CSVHandler()
