"""
Mock Banking API Integration - Bank 1 (Major Bank)
Provides account balance, transactions, and loan product recommendations.
"""
from typing import Dict, List, Optional
from datetime import datetime, date, timedelta
from dataclasses import dataclass
import random


@dataclass
class BankAccount:
    account_number: str
    account_type: str
    balance: float
    currency: str = "INR"


class BankAPI1:
    """Mock integration with a major bank API."""
    
    BANK_NAME = "Sample National Bank"
    
    def __init__(self):
        self.connected = False
        self.account_id = None
    
    def connect(self, account_number: str, api_key: str) -> bool:
        """Mock connection to bank API."""
        if account_number and len(account_number) >= 10:
            self.connected = True
            self.account_id = account_number
            return True
        return False
    
    def get_account_balance(self, account_number: str) -> Dict:
        """Get current account balance."""
        return {
            'account_number': account_number[-4:].rjust(len(account_number), 'X'),
            'account_type': 'Current Account',
            'balance': round(random.uniform(100000, 5000000), 2),
            'available_balance': round(random.uniform(80000, 4500000), 2),
            'currency': 'INR',
            'as_of': datetime.now().isoformat()
        }
    
    def get_transactions(self, account_number: str, from_date: date, 
                        to_date: date) -> List[Dict]:
        """Get transaction history."""
        transactions = []
        current = from_date
        
        while current <= to_date:
            # Generate 1-5 transactions per day
            for _ in range(random.randint(1, 5)):
                is_credit = random.random() > 0.4
                amount = round(random.uniform(1000, 100000), 2)
                
                transactions.append({
                    'date': current.isoformat(),
                    'type': 'Credit' if is_credit else 'Debit',
                    'amount': amount,
                    'description': random.choice([
                        'NEFT Transfer', 'RTGS Payment', 'UPI Collection',
                        'Cheque Deposit', 'Vendor Payment', 'Salary Credit',
                        'GST Payment', 'Utility Bill', 'Supplier Payment'
                    ]),
                    'reference': f"TXN{random.randint(100000, 999999)}",
                    'balance': round(random.uniform(100000, 5000000), 2)
                })
            current += timedelta(days=1)
        
        return sorted(transactions, key=lambda x: x['date'], reverse=True)
    
    def get_loan_products(self, business_profile: Dict) -> List[Dict]:
        """Get available loan products based on business profile."""
        credit_score = business_profile.get('credit_score', 600)
        annual_turnover = business_profile.get('annual_turnover', 0)
        
        products = []
        
        # Working Capital Loan
        if credit_score >= 650:
            products.append({
                'product_name': 'Business Working Capital Loan',
                'bank': self.BANK_NAME,
                'max_amount': min(annual_turnover * 0.25, 50000000),
                'interest_rate': '10.5% - 12.5% p.a.',
                'tenure': 'Up to 12 months',
                'processing_fee': '0.5% of loan amount',
                'eligibility': 'Eligible based on credit profile',
                'features': [
                    'No collateral up to Rs. 50 Lakh',
                    'Flexible repayment options',
                    'Quick approval in 3-5 days'
                ]
            })
        
        # Term Loan
        if credit_score >= 700:
            products.append({
                'product_name': 'Business Term Loan',
                'bank': self.BANK_NAME,
                'max_amount': min(annual_turnover * 0.5, 100000000),
                'interest_rate': '11% - 13% p.a.',
                'tenure': 'Up to 60 months',
                'processing_fee': '1% of loan amount',
                'eligibility': 'Eligible',
                'features': [
                    'For expansion and capex',
                    'Moratorium period available',
                    'Flexible security options'
                ]
            })
        
        # Overdraft Facility
        products.append({
            'product_name': 'Business Overdraft',
            'bank': self.BANK_NAME,
            'max_amount': min(annual_turnover * 0.1, 10000000),
            'interest_rate': '12% - 14% p.a.',
            'tenure': 'Renewable annually',
            'processing_fee': '0.25% of limit',
            'eligibility': 'Eligible' if credit_score >= 600 else 'Conditional',
            'features': [
                'Pay interest only on utilized amount',
                'Revolving credit facility',
                'Against FD/Property'
            ]
        })
        
        return products
    
    def get_account_statement(self, account_number: str, period: str) -> Dict:
        """Get account statement summary."""
        transactions = self.get_transactions(
            account_number,
            date.today() - timedelta(days=30),
            date.today()
        )
        
        credits = sum(t['amount'] for t in transactions if t['type'] == 'Credit')
        debits = sum(t['amount'] for t in transactions if t['type'] == 'Debit')
        
        return {
            'account_number': account_number[-4:].rjust(len(account_number), 'X'),
            'period': period,
            'opening_balance': round(random.uniform(100000, 500000), 2),
            'total_credits': round(credits, 2),
            'total_debits': round(debits, 2),
            'closing_balance': round(random.uniform(150000, 600000), 2),
            'transaction_count': len(transactions),
            'average_balance': round(random.uniform(200000, 800000), 2)
        }


bank_api_1 = BankAPI1()
