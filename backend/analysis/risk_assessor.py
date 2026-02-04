"""
Risk assessment module for financial analysis.
Identifies and evaluates various financial risks.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class RiskCategory(Enum):
    LIQUIDITY = "liquidity"
    CREDIT = "credit"
    MARKET = "market"
    OPERATIONAL = "operational"
    COMPLIANCE = "compliance"
    CONCENTRATION = "concentration"
    CASH_FLOW = "cash_flow"


class RiskSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RiskFactor:
    id: str
    category: RiskCategory
    name: str
    description: str
    severity: RiskSeverity
    probability: float
    impact_score: float
    indicators: List[str] = field(default_factory=list)
    mitigation_suggestions: List[str] = field(default_factory=list)
    
    @property
    def risk_score(self) -> float:
        return self.probability * self.impact_score


class RiskAssessor:
    """Assesses financial risks for SMEs."""
    
    THRESHOLDS = {
        'current_ratio': {'low': 2.0, 'medium': 1.5, 'high': 1.0, 'critical': 0.5},
        'debt_to_equity': {'low': 0.5, 'medium': 1.0, 'high': 2.0, 'critical': 3.0},
        'interest_coverage': {'critical': 1.0, 'high': 2.0, 'medium': 3.0, 'low': 5.0},
        'dso': {'low': 30, 'medium': 45, 'high': 60, 'critical': 90},
    }
    
    def __init__(self):
        self.risks: List[RiskFactor] = []
    
    def assess_all_risks(self, financial_data: Dict, metrics: Dict, historical_data: Optional[Dict] = None) -> Dict:
        self.risks = []
        self._assess_liquidity_risks(financial_data, metrics)
        self._assess_credit_risks(financial_data, metrics)
        self._assess_cash_flow_risks(financial_data, metrics)
        self._assess_operational_risks(financial_data, metrics)
        risk_profile = self._calculate_risk_profile()
        
        return {
            'assessment_date': datetime.utcnow().isoformat(),
            'overall_risk_level': risk_profile['overall_level'],
            'overall_risk_score': risk_profile['overall_score'],
            'risk_profile': risk_profile,
            'risks': [self._risk_to_dict(r) for r in self.risks],
            'recommendations': self._generate_recommendations()
        }
    
    def _assess_liquidity_risks(self, financial_data: Dict, metrics: Dict) -> None:
        liquidity_metrics = metrics.get('liquidity', [])
        current_ratio = self._get_metric_value(liquidity_metrics, 'Current Ratio')
        
        if current_ratio is not None and current_ratio < self.THRESHOLDS['current_ratio']['critical']:
            self.risks.append(RiskFactor(
                id='LIQ001', category=RiskCategory.LIQUIDITY,
                name='Critical Liquidity Shortage',
                description=f'Current ratio of {current_ratio:.2f} indicates severe liquidity issues',
                severity=RiskSeverity.CRITICAL, probability=0.9, impact_score=90,
                indicators=['Current ratio below 0.5'],
                mitigation_suggestions=['Negotiate payment terms', 'Accelerate collections', 'Consider emergency financing']
            ))
    
    def _assess_credit_risks(self, financial_data: Dict, metrics: Dict) -> None:
        solvency_metrics = metrics.get('solvency', [])
        debt_to_equity = self._get_metric_value(solvency_metrics, 'Debt to Equity Ratio')
        
        if debt_to_equity is not None and debt_to_equity > self.THRESHOLDS['debt_to_equity']['critical']:
            self.risks.append(RiskFactor(
                id='CRD001', category=RiskCategory.CREDIT,
                name='Excessive Leverage',
                description=f'Debt to equity of {debt_to_equity:.2f} indicates high leverage',
                severity=RiskSeverity.CRITICAL, probability=0.85, impact_score=85,
                indicators=['D/E ratio above 3.0'],
                mitigation_suggestions=['Prioritize debt repayment', 'Consider equity infusion']
            ))
    
    def _assess_cash_flow_risks(self, financial_data: Dict, metrics: Dict) -> None:
        cash_flow_metrics = metrics.get('cash_flow', [])
        fcf = self._get_metric_value(cash_flow_metrics, 'Free Cash Flow')
        
        if fcf is not None and fcf < 0:
            self.risks.append(RiskFactor(
                id='CF001', category=RiskCategory.CASH_FLOW,
                name='Negative Free Cash Flow',
                description='Business is burning cash',
                severity=RiskSeverity.HIGH, probability=0.7, impact_score=70,
                indicators=['Negative FCF'],
                mitigation_suggestions=['Review capex', 'Improve efficiency']
            ))
    
    def _assess_operational_risks(self, financial_data: Dict, metrics: Dict) -> None:
        profitability_metrics = metrics.get('profitability', [])
        net_margin = self._get_metric_value(profitability_metrics, 'Net Profit Margin')
        
        if net_margin is not None and net_margin < 0:
            self.risks.append(RiskFactor(
                id='OPS001', category=RiskCategory.OPERATIONAL,
                name='Operating Losses',
                description='Business is operating at a loss',
                severity=RiskSeverity.HIGH, probability=0.8, impact_score=75,
                indicators=['Negative net margin'],
                mitigation_suggestions=['Review costs', 'Adjust pricing']
            ))
    
    def _get_metric_value(self, metrics: List, metric_name: str) -> Optional[float]:
        for metric in metrics:
            if hasattr(metric, 'name') and metric.name == metric_name:
                return metric.value
            elif isinstance(metric, dict) and metric.get('name') == metric_name:
                return metric.get('value')
        return None
    
    def _calculate_risk_profile(self) -> Dict:
        if not self.risks:
            return {'overall_level': 'low', 'overall_score': 10, 'critical_count': 0, 'high_count': 0}
        
        critical = sum(1 for r in self.risks if r.severity == RiskSeverity.CRITICAL)
        high = sum(1 for r in self.risks if r.severity == RiskSeverity.HIGH)
        avg_score = sum(r.risk_score for r in self.risks) / len(self.risks)
        
        if critical > 0: overall_level = 'critical'
        elif high > 0: overall_level = 'high'
        elif avg_score > 30: overall_level = 'medium'
        else: overall_level = 'low'
        
        return {'overall_level': overall_level, 'overall_score': round(avg_score, 1), 
                'critical_count': critical, 'high_count': high}
    
    def _generate_recommendations(self) -> List[Dict]:
        recommendations = []
        for risk in sorted(self.risks, key=lambda r: r.risk_score, reverse=True)[:5]:
            for suggestion in risk.mitigation_suggestions[:2]:
                recommendations.append({'action': suggestion, 'priority': risk.severity.value, 'related_risk': risk.name})
        return recommendations
    
    def _risk_to_dict(self, risk: RiskFactor) -> Dict:
        return {
            'id': risk.id, 'category': risk.category.value, 'name': risk.name,
            'description': risk.description, 'severity': risk.severity.value,
            'risk_score': risk.risk_score, 'mitigation_suggestions': risk.mitigation_suggestions
        }


risk_assessor = RiskAssessor()
