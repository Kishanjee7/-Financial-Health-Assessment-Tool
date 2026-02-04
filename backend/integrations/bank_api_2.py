"""
Mock NBFC API Integration - Bank 2 (NBFC)
Provides working capital loans, invoice financing, and credit lines.
"""
from typing import Dict, List
from datetime import datetime
from dataclasses import dataclass
import random


class NBFCAPI:
    """Mock integration with an NBFC for alternative financing."""
    
    NBFC_NAME = "Sample Finance Ltd"
    
    def __init__(self):
        self.connected = False
    
    def connect(self, business_id: str, api_key: str) -> bool:
        """Mock connection to NBFC API."""
        if business_id:
            self.connected = True
            return True
        return False
    
    def get_credit_assessment(self, business_data: Dict) -> Dict:
        """Get NBFC's credit assessment for the business."""
        gstin = business_data.get('gstin', '')
        annual_turnover = business_data.get('annual_turnover', 0)
        
        # Mock credit assessment
        base_score = 500
        if annual_turnover > 10000000: base_score += 100
        if annual_turnover > 50000000: base_score += 100
        if gstin: base_score += 50
        
        return {
            'assessment_date': datetime.now().isoformat(),
            'credit_score': min(base_score + random.randint(0, 100), 900),
            'credit_limit': annual_turnover * 0.2,
            'risk_grade': random.choice(['A', 'B', 'C']),
            'status': 'Approved' if base_score > 600 else 'Under Review'
        }
    
    def get_invoice_financing_options(self, invoices: List[Dict]) -> Dict:
        """Get invoice financing/factoring options."""
        total_value = sum(inv.get('total_amount', 0) for inv in invoices)
        eligible_value = total_value * 0.8  # 80% advance
        
        return {
            'product_name': 'Invoice Financing',
            'provider': self.NBFC_NAME,
            'invoices_submitted': len(invoices),
            'total_invoice_value': total_value,
            'eligible_amount': eligible_value,
            'advance_percentage': 80,
            'interest_rate': '14% - 18% p.a.',
            'processing_time': '24-48 hours',
            'features': [
                'No collateral required',
                'Non-recourse option available',
                'Digital invoice submission'
            ]
        }
    
    def get_working_capital_products(self, profile: Dict) -> List[Dict]:
        """Get working capital loan products."""
        turnover = profile.get('annual_turnover', 0)
        
        products = [
            {
                'product_name': 'Flexi Working Capital',
                'provider': self.NBFC_NAME,
                'max_amount': min(turnover * 0.15, 25000000),
                'interest_rate': '15% - 18% p.a.',
                'tenure': 'Up to 24 months',
                'processing_fee': '2% of loan amount',
                'features': [
                    'Minimal documentation',
                    'Approval within 48 hours',
                    'No collateral up to Rs. 25 Lakh',
                    'Flexible repayment'
                ]
            },
            {
                'product_name': 'Supply Chain Finance',
                'provider': self.NBFC_NAME,
                'max_amount': min(turnover * 0.2, 50000000),
                'interest_rate': '12% - 15% p.a.',
                'tenure': 'Up to 90 days per transaction',
                'processing_fee': '1.5% of limit',
                'features': [
                    'Pay suppliers early',
                    'Extend payment terms',
                    'Digital platform'
                ]
            },
            {
                'product_name': 'Merchant Cash Advance',
                'provider': self.NBFC_NAME,
                'max_amount': min(turnover * 0.1, 10000000),
                'interest_rate': 'Factor rate 1.2 - 1.4',
                'tenure': '6-12 months',
                'processing_fee': 'Included in factor rate',
                'features': [
                    'Based on card/UPI collections',
                    'Daily repayment from sales',
                    'No fixed EMI'
                ]
            }
        ]
        
        return products
    
    def apply_for_loan(self, product_name: str, amount: float, 
                      business_data: Dict) -> Dict:
        """Submit loan application."""
        return {
            'application_id': f"APP{random.randint(100000, 999999)}",
            'product': product_name,
            'requested_amount': amount,
            'status': 'Submitted',
            'next_steps': [
                'Document verification (1-2 days)',
                'Credit assessment (1 day)',
                'Approval decision (1 day)',
                'Disbursement (Same day after approval)'
            ],
            'estimated_decision_date': 'Within 3-5 business days'
        }


nbfc_api = NBFCAPI()
