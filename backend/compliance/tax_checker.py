"""
Tax compliance checker module.
"""
from typing import Dict, List
from datetime import datetime, date
from compliance.gst_integration import gst_integration


class TaxChecker:
    """Checks tax compliance for businesses."""
    
    def check_all_compliance(self, business_data: Dict, tax_records: List[Dict]) -> Dict:
        """Comprehensive tax compliance check."""
        results = {
            'check_date': datetime.utcnow().isoformat(),
            'gst_compliance': self._check_gst_compliance(business_data),
            'tds_compliance': self._check_tds_compliance(tax_records),
            'issues': [],
            'recommendations': []
        }
        
        # Aggregate issues
        for check in ['gst_compliance', 'tds_compliance']:
            if results[check].get('issues'):
                results['issues'].extend(results[check]['issues'])
        
        # Overall status
        results['overall_status'] = 'Compliant' if not results['issues'] else 'Non-Compliant'
        results['compliance_score'] = self._calculate_score(results)
        
        return results
    
    def _check_gst_compliance(self, business_data: Dict) -> Dict:
        gstin = business_data.get('gstin')
        if not gstin:
            return {'status': 'Not Applicable', 'reason': 'No GSTIN registered'}
        
        return gst_integration.check_compliance(gstin)
    
    def _check_tds_compliance(self, tax_records: List[Dict]) -> Dict:
        """Check TDS compliance."""
        tds_records = [r for r in tax_records if r.get('tax_type') == 'tds']
        
        issues = []
        for record in tds_records:
            if not record.get('is_filed'):
                issues.append(f"TDS return pending for {record.get('period', 'unknown period')}")
        
        return {
            'status': 'Compliant' if not issues else 'Issues Found',
            'records_checked': len(tds_records),
            'issues': issues
        }
    
    def _calculate_score(self, results: Dict) -> float:
        base_score = 100
        deductions = len(results.get('issues', [])) * 10
        return max(0, base_score - deductions)
    
    def get_tax_optimization_suggestions(self, financial_data: Dict) -> List[Dict]:
        """Suggest tax optimization strategies."""
        suggestions = []
        
        income = financial_data.get('income_statement', {})
        
        # Check for common optimization opportunities
        if income.get('depreciation', 0) == 0 and income.get('fixed_assets', 0) > 0:
            suggestions.append({
                'category': 'Depreciation',
                'suggestion': 'Claim depreciation on fixed assets',
                'potential_savings': 'Up to 15% of asset value annually'
            })
        
        if income.get('rd_expenses', 0) > 0:
            suggestions.append({
                'category': 'R&D Deduction',
                'suggestion': 'Claim weighted deduction on R&D expenses',
                'potential_savings': 'Up to 150% of R&D expenses'
            })
        
        suggestions.append({
            'category': 'Input Tax Credit',
            'suggestion': 'Ensure all eligible ITC is claimed',
            'potential_savings': 'Varies based on purchases'
        })
        
        return suggestions


tax_checker = TaxChecker()
