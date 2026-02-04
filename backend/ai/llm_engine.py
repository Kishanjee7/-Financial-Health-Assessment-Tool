"""
OpenAI/LLM integration for generating insights and recommendations.
"""
from typing import Dict, List, Optional
from openai import OpenAI
from config import settings


class LLMEngine:
    """AI-powered insights and recommendations engine."""
    
    def __init__(self):
        self.client = None
        self.model = settings.OPENAI_MODEL
        if settings.OPENAI_API_KEY:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def generate_insights(self, financial_data: Dict, metrics: Dict, 
                         risk_assessment: Dict, language: str = 'en') -> Dict:
        """Generate AI-powered financial insights."""
        if not self.client:
            return self._generate_fallback_insights(financial_data, metrics, risk_assessment)
        
        prompt = self._build_insights_prompt(financial_data, metrics, risk_assessment, language)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt(language)},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return {
                'summary': response.choices[0].message.content,
                'generated': True,
                'model': self.model
            }
        except Exception as e:
            return self._generate_fallback_insights(financial_data, metrics, risk_assessment)
    
    def generate_recommendations(self, metrics: Dict, risk_assessment: Dict,
                                  industry: str, language: str = 'en') -> List[Dict]:
        """Generate actionable recommendations."""
        if not self.client:
            return self._generate_fallback_recommendations(metrics, risk_assessment)
        
        prompt = self._build_recommendations_prompt(metrics, risk_assessment, industry)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a financial advisor for SMEs. Provide specific, actionable recommendations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse recommendations from response
            content = response.choices[0].message.content
            return self._parse_recommendations(content)
        except Exception:
            return self._generate_fallback_recommendations(metrics, risk_assessment)
    
    def suggest_financial_products(self, credit_score: Dict, financial_needs: Dict,
                                    industry: str) -> List[Dict]:
        """Suggest suitable financial products from banks/NBFCs."""
        products = []
        score = credit_score.get('score', 500)
        
        # Working capital loans
        if financial_needs.get('working_capital_gap', 0) > 0:
            if score >= 700:
                products.append({
                    'type': 'Working Capital Loan',
                    'provider_type': 'Bank',
                    'interest_range': '10-12% p.a.',
                    'eligibility': 'High',
                    'features': ['Competitive rates', 'Flexible tenures', 'Collateral options']
                })
            else:
                products.append({
                    'type': 'Working Capital Loan',
                    'provider_type': 'NBFC',
                    'interest_range': '14-18% p.a.',
                    'eligibility': 'Moderate',
                    'features': ['Faster approval', 'Minimal documentation', 'No collateral']
                })
        
        # Invoice financing
        if financial_needs.get('receivables', 0) > 0:
            products.append({
                'type': 'Invoice Financing',
                'provider_type': 'Bank/NBFC',
                'interest_range': '12-16% p.a.',
                'eligibility': 'Based on invoice quality',
                'features': ['Immediate liquidity', 'Non-recourse options', 'Pay only for used limit']
            })
        
        # Term loans
        if financial_needs.get('expansion_plans', False):
            products.append({
                'type': 'Term Loan',
                'provider_type': 'Bank',
                'interest_range': '11-14% p.a.',
                'eligibility': 'High' if score >= 650 else 'Moderate',
                'features': ['Long tenure', 'Fixed EMI', 'Tax benefits on interest']
            })
        
        return products
    
    def _get_system_prompt(self, language: str) -> str:
        base = """You are an expert financial analyst for small and medium enterprises (SMEs). 
        Analyze the financial data provided and give clear, actionable insights.
        Focus on practical advice that business owners can understand and implement."""
        
        if language == 'hi':
            base += "\nRespond in Hindi using Devanagari script."
        return base
    
    def _build_insights_prompt(self, financial_data: Dict, metrics: Dict, 
                               risk_assessment: Dict, language: str) -> str:
        return f"""Analyze this SME's financial health:

Health Score: {metrics.get('health_score', {}).get('overall_score', 'N/A')}/100
Risk Level: {risk_assessment.get('overall_risk_level', 'Unknown')}

Key Metrics:
- Current Ratio: {self._get_metric(metrics, 'liquidity', 'Current Ratio')}
- Net Profit Margin: {self._get_metric(metrics, 'profitability', 'Net Profit Margin')}
- Debt to Equity: {self._get_metric(metrics, 'solvency', 'Debt to Equity Ratio')}

Key Risks: {[r.get('name') for r in risk_assessment.get('risks', [])[:3]]}

Provide a concise executive summary (3-4 paragraphs) covering:
1. Overall financial health assessment
2. Key strengths and concerns
3. Priority areas for improvement
4. Outlook and recommendations"""
    
    def _build_recommendations_prompt(self, metrics: Dict, risk_assessment: Dict, industry: str) -> str:
        return f"""Based on this {industry} business's financial analysis:

Risk Level: {risk_assessment.get('overall_risk_level', 'Unknown')}
Top Risks: {[r.get('name') for r in risk_assessment.get('risks', [])[:5]]}

Provide 5 specific, actionable recommendations to improve financial health.
Format each as: [Priority: High/Medium/Low] - Recommendation
Focus on practical steps the business can take within 3-6 months."""
    
    def _get_metric(self, metrics: Dict, category: str, name: str) -> str:
        for m in metrics.get(category, []):
            metric_name = m.name if hasattr(m, 'name') else m.get('name', '')
            value = m.value if hasattr(m, 'value') else m.get('value')
            if metric_name == name and value is not None:
                return f"{value:.2f}"
        return "N/A"
    
    def _parse_recommendations(self, content: str) -> List[Dict]:
        recommendations = []
        lines = content.strip().split('\n')
        for line in lines:
            if line.strip() and '-' in line:
                recommendations.append({
                    'recommendation': line.strip(),
                    'source': 'ai_generated'
                })
        return recommendations[:10]
    
    def _generate_fallback_insights(self, financial_data: Dict, metrics: Dict, 
                                    risk_assessment: Dict) -> Dict:
        """Generate insights without AI when API is not available."""
        health_score = metrics.get('health_score', {}).get('overall_score', 50)
        risk_level = risk_assessment.get('overall_risk_level', 'medium')
        
        if health_score >= 70:
            summary = "The business demonstrates strong financial health with solid fundamentals."
        elif health_score >= 50:
            summary = "The business shows moderate financial stability with areas for improvement."
        else:
            summary = "The business faces financial challenges requiring immediate attention."
        
        summary += f" Overall risk level is {risk_level}."
        
        return {'summary': summary, 'generated': False, 'model': 'fallback'}
    
    def _generate_fallback_recommendations(self, metrics: Dict, 
                                           risk_assessment: Dict) -> List[Dict]:
        """Generate basic recommendations without AI."""
        recommendations = []
        risks = risk_assessment.get('risks', [])
        
        for risk in risks[:5]:
            for suggestion in risk.get('mitigation_suggestions', [])[:1]:
                recommendations.append({
                    'recommendation': suggestion,
                    'priority': risk.get('severity', 'medium'),
                    'source': 'rule_based'
                })
        
        return recommendations


llm_engine = LLMEngine()
