"""
Creditworthiness assessment module.
Evaluates credit score based on financial health indicators.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class CreditRating(Enum):
    AAA = "AAA"  # Excellent
    AA = "AA"    # Very Good
    A = "A"      # Good
    BBB = "BBB"  # Adequate
    BB = "BB"    # Speculative
    B = "B"      # Highly Speculative
    CCC = "CCC"  # Substantial Risk
    D = "D"      # Default


@dataclass
class CreditScore:
    score: int  # 300-900
    rating: CreditRating
    factors: Dict[str, float]
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]


class CreditworthinessAssessor:
    """Evaluates creditworthiness of SMEs."""
    
    # Score weights
    WEIGHTS = {
        'payment_history': 0.25,
        'debt_utilization': 0.20,
        'business_stability': 0.15,
        'revenue_trend': 0.15,
        'profitability': 0.10,
        'liquidity': 0.10,
        'collateral': 0.05
    }
    
    def assess_creditworthiness(self, financial_data: Dict, metrics: Dict, 
                                 business_info: Optional[Dict] = None) -> CreditScore:
        factors = {}
        
        # Payment history (simulated)
        factors['payment_history'] = self._assess_payment_history(financial_data)
        
        # Debt utilization
        factors['debt_utilization'] = self._assess_debt_utilization(metrics)
        
        # Business stability
        factors['business_stability'] = self._assess_business_stability(business_info)
        
        # Revenue trend
        factors['revenue_trend'] = self._assess_revenue_trend(financial_data)
        
        # Profitability
        factors['profitability'] = self._assess_profitability(metrics)
        
        # Liquidity
        factors['liquidity'] = self._assess_liquidity(metrics)
        
        # Calculate weighted score
        weighted_score = sum(factors[k] * self.WEIGHTS[k] for k in self.WEIGHTS if k in factors)
        
        # Convert to 300-900 scale
        credit_score = int(300 + (weighted_score * 6))
        credit_score = max(300, min(900, credit_score))
        
        rating = self._get_rating(credit_score)
        strengths, weaknesses = self._identify_strengths_weaknesses(factors)
        recommendations = self._generate_recommendations(factors, rating)
        
        return CreditScore(
            score=credit_score,
            rating=rating,
            factors=factors,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations
        )
    
    def _assess_payment_history(self, financial_data: Dict) -> float:
        # Check for payment-related indicators
        payables = financial_data.get('balance_sheet', {}).get('accounts_payable', 0)
        overdue = financial_data.get('overdue_payables', 0)
        
        if payables > 0:
            overdue_ratio = overdue / payables if payables else 0
            return max(0, 100 - (overdue_ratio * 200))
        return 70  # Default score
    
    def _assess_debt_utilization(self, metrics: Dict) -> float:
        solvency = metrics.get('solvency', [])
        for m in solvency:
            name = m.name if hasattr(m, 'name') else m.get('name', '')
            value = m.value if hasattr(m, 'value') else m.get('value')
            if name == 'Debt to Equity Ratio' and value is not None:
                if value < 0.5: return 100
                elif value < 1.0: return 80
                elif value < 2.0: return 60
                elif value < 3.0: return 40
                else: return 20
        return 50
    
    def _assess_business_stability(self, business_info: Optional[Dict]) -> float:
        if not business_info:
            return 50
        
        years = business_info.get('years_in_business', 0)
        if years >= 10: return 100
        elif years >= 5: return 80
        elif years >= 3: return 60
        elif years >= 1: return 40
        return 20
    
    def _assess_revenue_trend(self, financial_data: Dict) -> float:
        current = financial_data.get('current_period', {}).get('revenue', 0)
        previous = financial_data.get('previous_period', {}).get('revenue', 0)
        
        if previous > 0:
            growth = (current - previous) / previous
            if growth > 0.20: return 100
            elif growth > 0.10: return 80
            elif growth > 0: return 60
            elif growth > -0.10: return 40
            else: return 20
        return 50
    
    def _assess_profitability(self, metrics: Dict) -> float:
        profitability = metrics.get('profitability', [])
        for m in profitability:
            name = m.name if hasattr(m, 'name') else m.get('name', '')
            value = m.value if hasattr(m, 'value') else m.get('value')
            if name == 'Net Profit Margin' and value is not None:
                if value > 0.15: return 100
                elif value > 0.10: return 80
                elif value > 0.05: return 60
                elif value > 0: return 40
                else: return 20
        return 50
    
    def _assess_liquidity(self, metrics: Dict) -> float:
        liquidity = metrics.get('liquidity', [])
        for m in liquidity:
            name = m.name if hasattr(m, 'name') else m.get('name', '')
            value = m.value if hasattr(m, 'value') else m.get('value')
            if name == 'Current Ratio' and value is not None:
                if value > 2.0: return 100
                elif value > 1.5: return 80
                elif value > 1.0: return 60
                elif value > 0.5: return 40
                else: return 20
        return 50
    
    def _get_rating(self, score: int) -> CreditRating:
        if score >= 800: return CreditRating.AAA
        elif score >= 750: return CreditRating.AA
        elif score >= 700: return CreditRating.A
        elif score >= 650: return CreditRating.BBB
        elif score >= 600: return CreditRating.BB
        elif score >= 500: return CreditRating.B
        elif score >= 400: return CreditRating.CCC
        else: return CreditRating.D
    
    def _identify_strengths_weaknesses(self, factors: Dict) -> tuple:
        strengths = [k.replace('_', ' ').title() for k, v in factors.items() if v >= 70]
        weaknesses = [k.replace('_', ' ').title() for k, v in factors.items() if v < 50]
        return strengths, weaknesses
    
    def _generate_recommendations(self, factors: Dict, rating: CreditRating) -> List[str]:
        recommendations = []
        if factors.get('debt_utilization', 100) < 50:
            recommendations.append("Reduce debt levels to improve creditworthiness")
        if factors.get('liquidity', 100) < 50:
            recommendations.append("Improve liquidity position")
        if factors.get('profitability', 100) < 50:
            recommendations.append("Focus on improving profitability margins")
        if rating.value in ['CCC', 'D']:
            recommendations.append("Seek professional financial advisory")
        return recommendations


creditworthiness_assessor = CreditworthinessAssessor()
