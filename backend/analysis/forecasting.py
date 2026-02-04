"""
Financial forecasting module.
Provides revenue, expense, and cash flow projections.
"""
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import numpy as np
from enum import Enum


class ForecastScenario(Enum):
    PESSIMISTIC = "pessimistic"
    BASE = "base"
    OPTIMISTIC = "optimistic"


@dataclass
class ForecastResult:
    metric: str
    periods: List[str]
    base_forecast: List[float]
    pessimistic_forecast: List[float]
    optimistic_forecast: List[float]
    confidence_interval: float
    assumptions: List[str]


class FinancialForecaster:
    """Generates financial forecasts for SMEs."""
    
    def __init__(self):
        self.forecast_periods = 12  # Default to 12 months
    
    def generate_forecast(self, financial_data: Dict, periods: int = 12) -> Dict:
        self.forecast_periods = periods
        
        results = {
            'forecast_date': datetime.utcnow().isoformat(),
            'periods': periods,
            'revenue_forecast': self._forecast_revenue(financial_data),
            'expense_forecast': self._forecast_expenses(financial_data),
            'cash_flow_forecast': self._forecast_cash_flow(financial_data),
            'working_capital_forecast': self._forecast_working_capital(financial_data)
        }
        
        return results
    
    def _forecast_revenue(self, financial_data: Dict) -> Dict:
        historical = financial_data.get('historical_revenue', [])
        current_revenue = financial_data.get('income_statement', {}).get('revenue', 0)
        
        if not historical and current_revenue:
            historical = [current_revenue * 0.9, current_revenue * 0.95, current_revenue]
        
        if not historical:
            return {'error': 'Insufficient data for revenue forecast'}
        
        # Calculate growth rate
        if len(historical) >= 2:
            growth_rate = (historical[-1] - historical[0]) / historical[0] / len(historical)
        else:
            growth_rate = 0.05  # Default 5% growth
        
        # Generate forecasts
        base_forecast = []
        last_value = historical[-1] if historical else current_revenue
        
        for i in range(self.forecast_periods):
            monthly_growth = 1 + (growth_rate / 12)
            projected = last_value * (monthly_growth ** (i + 1))
            base_forecast.append(round(projected, 2))
        
        # Scenario variations
        pessimistic = [v * 0.85 for v in base_forecast]
        optimistic = [v * 1.15 for v in base_forecast]
        
        periods = self._generate_period_labels()
        
        return {
            'periods': periods,
            'values': {'base': base_forecast, 'pessimistic': pessimistic, 'optimistic': optimistic},
            'growth_rate': round(growth_rate * 100, 1),
            'assumptions': [f'{round(growth_rate*100, 1)}% annual growth rate based on historical trend']
        }
    
    def _forecast_expenses(self, financial_data: Dict) -> Dict:
        income_stmt = financial_data.get('income_statement', {})
        current_expenses = income_stmt.get('total_expenses', 0) or income_stmt.get('expenses', 0)
        revenue = income_stmt.get('revenue', 0)
        
        if not current_expenses:
            return {'error': 'Insufficient expense data'}
        
        # Expense to revenue ratio
        expense_ratio = current_expenses / revenue if revenue else 0.8
        
        # Get revenue forecast to project expenses
        revenue_forecast = self._forecast_revenue(financial_data)
        if 'error' in revenue_forecast:
            base_forecast = [current_expenses / 12] * self.forecast_periods
        else:
            base_forecast = [v * expense_ratio for v in revenue_forecast['values']['base']]
        
        return {
            'periods': self._generate_period_labels(),
            'values': {
                'base': [round(v, 2) for v in base_forecast],
                'pessimistic': [round(v * 1.10, 2) for v in base_forecast],
                'optimistic': [round(v * 0.95, 2) for v in base_forecast]
            },
            'expense_ratio': round(expense_ratio * 100, 1),
            'assumptions': [f'Expense ratio of {round(expense_ratio*100, 1)}% maintained']
        }
    
    def _forecast_cash_flow(self, financial_data: Dict) -> Dict:
        revenue_forecast = self._forecast_revenue(financial_data)
        expense_forecast = self._forecast_expenses(financial_data)
        
        if 'error' in revenue_forecast or 'error' in expense_forecast:
            return {'error': 'Insufficient data for cash flow forecast'}
        
        rev_base = revenue_forecast['values']['base']
        exp_base = expense_forecast['values']['base']
        
        # Net cash flow (simplified: revenue - expenses)
        base_cash_flow = [round(r - e, 2) for r, e in zip(rev_base, exp_base)]
        
        return {
            'periods': self._generate_period_labels(),
            'values': {
                'base': base_cash_flow,
                'pessimistic': [round(v * 0.7, 2) for v in base_cash_flow],
                'optimistic': [round(v * 1.3, 2) for v in base_cash_flow]
            },
            'cumulative': [round(sum(base_cash_flow[:i+1]), 2) for i in range(len(base_cash_flow))]
        }
    
    def _forecast_working_capital(self, financial_data: Dict) -> Dict:
        balance_sheet = financial_data.get('balance_sheet', {})
        current_assets = balance_sheet.get('current_assets', 0)
        current_liabilities = balance_sheet.get('current_liabilities', 0)
        working_capital = current_assets - current_liabilities
        
        if not current_assets:
            return {'error': 'Insufficient balance sheet data'}
        
        # Simple growth projection
        growth_rate = 0.03  # 3% monthly growth assumption
        base_forecast = [round(working_capital * ((1 + growth_rate) ** (i+1)), 2) 
                        for i in range(self.forecast_periods)]
        
        return {
            'periods': self._generate_period_labels(),
            'values': {
                'base': base_forecast,
                'pessimistic': [round(v * 0.9, 2) for v in base_forecast],
                'optimistic': [round(v * 1.1, 2) for v in base_forecast]
            },
            'current_working_capital': working_capital
        }
    
    def _generate_period_labels(self) -> List[str]:
        start = datetime.now()
        return [(start + timedelta(days=30*i)).strftime('%b %Y') for i in range(1, self.forecast_periods + 1)]


financial_forecaster = FinancialForecaster()
