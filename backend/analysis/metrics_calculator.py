"""
Financial metrics calculator.
Calculates key financial ratios and health indicators.
"""
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
import math


class MetricCategory(Enum):
    """Categories of financial metrics."""
    LIQUIDITY = "liquidity"
    PROFITABILITY = "profitability"
    SOLVENCY = "solvency"
    EFFICIENCY = "efficiency"
    GROWTH = "growth"
    CASH_FLOW = "cash_flow"


@dataclass
class MetricResult:
    """Result of a metric calculation."""
    name: str
    value: Optional[float]
    category: MetricCategory
    benchmark: Optional[float] = None
    rating: Optional[str] = None  # excellent, good, fair, poor
    interpretation: Optional[str] = None
    formula: Optional[str] = None


class MetricsCalculator:
    """
    Calculates comprehensive financial metrics for SME analysis.
    All ratios are calculated following standard accounting practices.
    """
    
    # Industry benchmarks (simplified averages)
    BENCHMARKS = {
        'manufacturing': {
            'current_ratio': 1.5,
            'quick_ratio': 1.0,
            'gross_margin': 0.25,
            'net_margin': 0.08,
            'debt_to_equity': 1.0,
            'inventory_turnover': 6.0,
            'receivables_turnover': 8.0,
        },
        'retail': {
            'current_ratio': 1.2,
            'quick_ratio': 0.5,
            'gross_margin': 0.30,
            'net_margin': 0.05,
            'debt_to_equity': 0.8,
            'inventory_turnover': 8.0,
            'receivables_turnover': 20.0,
        },
        'services': {
            'current_ratio': 1.5,
            'quick_ratio': 1.2,
            'gross_margin': 0.40,
            'net_margin': 0.15,
            'debt_to_equity': 0.5,
            'inventory_turnover': None,
            'receivables_turnover': 10.0,
        },
        'ecommerce': {
            'current_ratio': 1.3,
            'quick_ratio': 0.8,
            'gross_margin': 0.35,
            'net_margin': 0.06,
            'debt_to_equity': 0.7,
            'inventory_turnover': 10.0,
            'receivables_turnover': 15.0,
        },
        'default': {
            'current_ratio': 1.5,
            'quick_ratio': 1.0,
            'gross_margin': 0.30,
            'net_margin': 0.10,
            'debt_to_equity': 1.0,
            'inventory_turnover': 6.0,
            'receivables_turnover': 10.0,
        }
    }
    
    def __init__(self, industry: str = 'default'):
        """
        Initialize calculator with industry context.
        
        Args:
            industry: Industry type for benchmark comparison
        """
        self.industry = industry.lower() if industry else 'default'
        self.benchmarks = self.BENCHMARKS.get(self.industry, self.BENCHMARKS['default'])
    
    def calculate_all_metrics(self, financial_data: Dict) -> Dict[str, List[MetricResult]]:
        """
        Calculate all available financial metrics.
        
        Args:
            financial_data: Dictionary containing financial statement data
        
        Returns:
            Dictionary categorized by metric type
        """
        results = {
            'liquidity': [],
            'profitability': [],
            'solvency': [],
            'efficiency': [],
            'growth': [],
            'cash_flow': []
        }
        
        # Extract key financial figures
        balance_sheet = financial_data.get('balance_sheet', {})
        income_statement = financial_data.get('income_statement', {})
        cash_flow = financial_data.get('cash_flow', {})
        
        # Calculate liquidity ratios
        results['liquidity'] = self._calculate_liquidity_ratios(balance_sheet)
        
        # Calculate profitability ratios
        results['profitability'] = self._calculate_profitability_ratios(
            income_statement, balance_sheet
        )
        
        # Calculate solvency ratios
        results['solvency'] = self._calculate_solvency_ratios(
            balance_sheet, income_statement
        )
        
        # Calculate efficiency ratios
        results['efficiency'] = self._calculate_efficiency_ratios(
            balance_sheet, income_statement
        )
        
        # Calculate growth metrics
        results['growth'] = self._calculate_growth_metrics(financial_data)
        
        # Calculate cash flow metrics
        results['cash_flow'] = self._calculate_cash_flow_metrics(
            cash_flow, income_statement
        )
        
        return results
    
    def _calculate_liquidity_ratios(self, balance_sheet: Dict) -> List[MetricResult]:
        """Calculate liquidity ratios."""
        results = []
        
        current_assets = balance_sheet.get('current_assets', 0)
        current_liabilities = balance_sheet.get('current_liabilities', 0)
        inventory = balance_sheet.get('inventory', 0)
        cash = balance_sheet.get('cash', 0)
        
        # Current Ratio
        current_ratio = self._safe_divide(current_assets, current_liabilities)
        results.append(MetricResult(
            name="Current Ratio",
            value=current_ratio,
            category=MetricCategory.LIQUIDITY,
            benchmark=self.benchmarks.get('current_ratio'),
            rating=self._rate_metric(current_ratio, self.benchmarks.get('current_ratio'), higher_is_better=True),
            interpretation=self._interpret_current_ratio(current_ratio),
            formula="Current Assets / Current Liabilities"
        ))
        
        # Quick Ratio (Acid Test)
        quick_ratio = self._safe_divide(current_assets - inventory, current_liabilities)
        results.append(MetricResult(
            name="Quick Ratio",
            value=quick_ratio,
            category=MetricCategory.LIQUIDITY,
            benchmark=self.benchmarks.get('quick_ratio'),
            rating=self._rate_metric(quick_ratio, self.benchmarks.get('quick_ratio'), higher_is_better=True),
            interpretation=self._interpret_quick_ratio(quick_ratio),
            formula="(Current Assets - Inventory) / Current Liabilities"
        ))
        
        # Cash Ratio
        cash_ratio = self._safe_divide(cash, current_liabilities)
        results.append(MetricResult(
            name="Cash Ratio",
            value=cash_ratio,
            category=MetricCategory.LIQUIDITY,
            benchmark=0.2,
            rating=self._rate_metric(cash_ratio, 0.2, higher_is_better=True),
            interpretation="Measures ability to pay off short-term debt with cash",
            formula="Cash / Current Liabilities"
        ))
        
        # Working Capital
        working_capital = current_assets - current_liabilities
        results.append(MetricResult(
            name="Working Capital",
            value=working_capital,
            category=MetricCategory.LIQUIDITY,
            rating="good" if working_capital > 0 else "poor",
            interpretation="Positive working capital indicates healthy short-term financial position",
            formula="Current Assets - Current Liabilities"
        ))
        
        return results
    
    def _calculate_profitability_ratios(
        self, 
        income_statement: Dict, 
        balance_sheet: Dict
    ) -> List[MetricResult]:
        """Calculate profitability ratios."""
        results = []
        
        revenue = income_statement.get('revenue', 0) or income_statement.get('total_revenue', 0)
        gross_profit = income_statement.get('gross_profit', 0)
        operating_income = income_statement.get('operating_income', 0)
        net_income = income_statement.get('net_income', 0) or income_statement.get('net_profit', 0)
        cogs = income_statement.get('cost_of_goods_sold', 0) or income_statement.get('cogs', 0)
        
        total_assets = balance_sheet.get('total_assets', 0)
        total_equity = balance_sheet.get('total_equity', 0) or balance_sheet.get('shareholders_equity', 0)
        
        # Gross Profit Margin
        gross_margin = self._safe_divide(gross_profit, revenue)
        if gross_margin is None and revenue and cogs:
            gross_margin = self._safe_divide(revenue - cogs, revenue)
        
        results.append(MetricResult(
            name="Gross Profit Margin",
            value=gross_margin,
            category=MetricCategory.PROFITABILITY,
            benchmark=self.benchmarks.get('gross_margin'),
            rating=self._rate_metric(gross_margin, self.benchmarks.get('gross_margin'), higher_is_better=True),
            interpretation="Percentage of revenue retained after direct costs",
            formula="Gross Profit / Revenue"
        ))
        
        # Operating Profit Margin
        operating_margin = self._safe_divide(operating_income, revenue)
        results.append(MetricResult(
            name="Operating Profit Margin",
            value=operating_margin,
            category=MetricCategory.PROFITABILITY,
            benchmark=0.15,
            rating=self._rate_metric(operating_margin, 0.15, higher_is_better=True),
            interpretation="Operational efficiency indicator",
            formula="Operating Income / Revenue"
        ))
        
        # Net Profit Margin
        net_margin = self._safe_divide(net_income, revenue)
        results.append(MetricResult(
            name="Net Profit Margin",
            value=net_margin,
            category=MetricCategory.PROFITABILITY,
            benchmark=self.benchmarks.get('net_margin'),
            rating=self._rate_metric(net_margin, self.benchmarks.get('net_margin'), higher_is_better=True),
            interpretation="Bottom-line profitability as percentage of revenue",
            formula="Net Income / Revenue"
        ))
        
        # Return on Assets (ROA)
        roa = self._safe_divide(net_income, total_assets)
        results.append(MetricResult(
            name="Return on Assets (ROA)",
            value=roa,
            category=MetricCategory.PROFITABILITY,
            benchmark=0.05,
            rating=self._rate_metric(roa, 0.05, higher_is_better=True),
            interpretation="How efficiently assets generate profit",
            formula="Net Income / Total Assets"
        ))
        
        # Return on Equity (ROE)
        roe = self._safe_divide(net_income, total_equity)
        results.append(MetricResult(
            name="Return on Equity (ROE)",
            value=roe,
            category=MetricCategory.PROFITABILITY,
            benchmark=0.15,
            rating=self._rate_metric(roe, 0.15, higher_is_better=True),
            interpretation="Return generated for shareholders",
            formula="Net Income / Shareholders' Equity"
        ))
        
        return results
    
    def _calculate_solvency_ratios(
        self, 
        balance_sheet: Dict, 
        income_statement: Dict
    ) -> List[MetricResult]:
        """Calculate solvency/leverage ratios."""
        results = []
        
        total_debt = balance_sheet.get('total_debt', 0) or balance_sheet.get('total_liabilities', 0)
        total_equity = balance_sheet.get('total_equity', 0) or balance_sheet.get('shareholders_equity', 0)
        total_assets = balance_sheet.get('total_assets', 0)
        operating_income = income_statement.get('operating_income', 0) or income_statement.get('ebit', 0)
        interest_expense = income_statement.get('interest_expense', 0)
        
        # Debt to Equity Ratio
        debt_to_equity = self._safe_divide(total_debt, total_equity)
        results.append(MetricResult(
            name="Debt to Equity Ratio",
            value=debt_to_equity,
            category=MetricCategory.SOLVENCY,
            benchmark=self.benchmarks.get('debt_to_equity'),
            rating=self._rate_metric(debt_to_equity, self.benchmarks.get('debt_to_equity'), higher_is_better=False),
            interpretation="Financial leverage indicator",
            formula="Total Debt / Total Equity"
        ))
        
        # Debt Ratio
        debt_ratio = self._safe_divide(total_debt, total_assets)
        results.append(MetricResult(
            name="Debt Ratio",
            value=debt_ratio,
            category=MetricCategory.SOLVENCY,
            benchmark=0.5,
            rating=self._rate_metric(debt_ratio, 0.5, higher_is_better=False),
            interpretation="Percentage of assets financed by debt",
            formula="Total Debt / Total Assets"
        ))
        
        # Interest Coverage Ratio
        interest_coverage = self._safe_divide(operating_income, interest_expense)
        results.append(MetricResult(
            name="Interest Coverage Ratio",
            value=interest_coverage,
            category=MetricCategory.SOLVENCY,
            benchmark=3.0,
            rating=self._rate_metric(interest_coverage, 3.0, higher_is_better=True),
            interpretation="Ability to pay interest on debt",
            formula="Operating Income / Interest Expense"
        ))
        
        # Equity Ratio
        equity_ratio = self._safe_divide(total_equity, total_assets)
        results.append(MetricResult(
            name="Equity Ratio",
            value=equity_ratio,
            category=MetricCategory.SOLVENCY,
            benchmark=0.5,
            rating=self._rate_metric(equity_ratio, 0.5, higher_is_better=True),
            interpretation="Portion of assets funded by equity",
            formula="Total Equity / Total Assets"
        ))
        
        return results
    
    def _calculate_efficiency_ratios(
        self, 
        balance_sheet: Dict, 
        income_statement: Dict
    ) -> List[MetricResult]:
        """Calculate efficiency/activity ratios."""
        results = []
        
        revenue = income_statement.get('revenue', 0) or income_statement.get('total_revenue', 0)
        cogs = income_statement.get('cost_of_goods_sold', 0) or income_statement.get('cogs', 0)
        inventory = balance_sheet.get('inventory', 0)
        receivables = balance_sheet.get('accounts_receivable', 0) or balance_sheet.get('receivables', 0)
        payables = balance_sheet.get('accounts_payable', 0) or balance_sheet.get('payables', 0)
        total_assets = balance_sheet.get('total_assets', 0)
        
        # Inventory Turnover
        if inventory > 0:
            inventory_turnover = self._safe_divide(cogs if cogs else revenue, inventory)
            results.append(MetricResult(
                name="Inventory Turnover",
                value=inventory_turnover,
                category=MetricCategory.EFFICIENCY,
                benchmark=self.benchmarks.get('inventory_turnover'),
                rating=self._rate_metric(inventory_turnover, self.benchmarks.get('inventory_turnover'), higher_is_better=True),
                interpretation="Times inventory is sold and replaced per year",
                formula="COGS / Average Inventory"
            ))
            
            # Days Inventory Outstanding
            if inventory_turnover:
                dio = 365 / inventory_turnover
                results.append(MetricResult(
                    name="Days Inventory Outstanding",
                    value=dio,
                    category=MetricCategory.EFFICIENCY,
                    benchmark=60,
                    rating=self._rate_metric(dio, 60, higher_is_better=False),
                    interpretation="Average days to sell inventory",
                    formula="365 / Inventory Turnover"
                ))
        
        # Receivables Turnover
        receivables_turnover = self._safe_divide(revenue, receivables)
        results.append(MetricResult(
            name="Receivables Turnover",
            value=receivables_turnover,
            category=MetricCategory.EFFICIENCY,
            benchmark=self.benchmarks.get('receivables_turnover'),
            rating=self._rate_metric(receivables_turnover, self.benchmarks.get('receivables_turnover'), higher_is_better=True),
            interpretation="Efficiency in collecting receivables",
            formula="Revenue / Accounts Receivable"
        ))
        
        # Days Sales Outstanding
        if receivables_turnover:
            dso = 365 / receivables_turnover
            results.append(MetricResult(
                name="Days Sales Outstanding",
                value=dso,
                category=MetricCategory.EFFICIENCY,
                benchmark=45,
                rating=self._rate_metric(dso, 45, higher_is_better=False),
                interpretation="Average days to collect payment",
                formula="365 / Receivables Turnover"
            ))
        
        # Payables Turnover
        payables_turnover = self._safe_divide(cogs if cogs else revenue * 0.7, payables)
        if payables_turnover:
            results.append(MetricResult(
                name="Payables Turnover",
                value=payables_turnover,
                category=MetricCategory.EFFICIENCY,
                benchmark=8.0,
                interpretation="How quickly company pays suppliers",
                formula="COGS / Accounts Payable"
            ))
            
            # Days Payables Outstanding
            dpo = 365 / payables_turnover
            results.append(MetricResult(
                name="Days Payables Outstanding",
                value=dpo,
                category=MetricCategory.EFFICIENCY,
                benchmark=45,
                interpretation="Average days to pay suppliers",
                formula="365 / Payables Turnover"
            ))
        
        # Asset Turnover
        asset_turnover = self._safe_divide(revenue, total_assets)
        results.append(MetricResult(
            name="Asset Turnover",
            value=asset_turnover,
            category=MetricCategory.EFFICIENCY,
            benchmark=1.0,
            rating=self._rate_metric(asset_turnover, 1.0, higher_is_better=True),
            interpretation="Revenue generated per rupee of assets",
            formula="Revenue / Total Assets"
        ))
        
        return results
    
    def _calculate_growth_metrics(self, financial_data: Dict) -> List[MetricResult]:
        """Calculate growth metrics from historical data."""
        results = []
        
        current = financial_data.get('current_period', {})
        previous = financial_data.get('previous_period', {})
        
        if current and previous:
            # Revenue Growth
            current_revenue = current.get('revenue', 0)
            previous_revenue = previous.get('revenue', 0)
            revenue_growth = self._calculate_growth_rate(previous_revenue, current_revenue)
            
            results.append(MetricResult(
                name="Revenue Growth Rate",
                value=revenue_growth,
                category=MetricCategory.GROWTH,
                benchmark=0.10,
                rating=self._rate_metric(revenue_growth, 0.10, higher_is_better=True),
                interpretation="Year-over-year revenue growth",
                formula="(Current Revenue - Previous Revenue) / Previous Revenue"
            ))
            
            # Profit Growth
            current_profit = current.get('net_income', 0)
            previous_profit = previous.get('net_income', 0)
            profit_growth = self._calculate_growth_rate(previous_profit, current_profit)
            
            results.append(MetricResult(
                name="Net Profit Growth Rate",
                value=profit_growth,
                category=MetricCategory.GROWTH,
                benchmark=0.10,
                rating=self._rate_metric(profit_growth, 0.10, higher_is_better=True),
                interpretation="Year-over-year profit growth",
                formula="(Current Profit - Previous Profit) / Previous Profit"
            ))
        
        return results
    
    def _calculate_cash_flow_metrics(
        self, 
        cash_flow: Dict, 
        income_statement: Dict
    ) -> List[MetricResult]:
        """Calculate cash flow related metrics."""
        results = []
        
        operating_cash_flow = cash_flow.get('operating_cash_flow', 0)
        investing_cash_flow = cash_flow.get('investing_cash_flow', 0)
        financing_cash_flow = cash_flow.get('financing_cash_flow', 0)
        net_income = income_statement.get('net_income', 0)
        revenue = income_statement.get('revenue', 0)
        
        # Operating Cash Flow Ratio
        if operating_cash_flow and revenue:
            ocf_ratio = operating_cash_flow / revenue
            results.append(MetricResult(
                name="Operating Cash Flow Ratio",
                value=ocf_ratio,
                category=MetricCategory.CASH_FLOW,
                benchmark=0.10,
                rating=self._rate_metric(ocf_ratio, 0.10, higher_is_better=True),
                interpretation="Cash generated from operations per rupee of sales",
                formula="Operating Cash Flow / Revenue"
            ))
        
        # Cash Flow Quality
        if operating_cash_flow and net_income:
            cash_quality = operating_cash_flow / net_income if net_income != 0 else None
            if cash_quality:
                results.append(MetricResult(
                    name="Cash Flow Quality",
                    value=cash_quality,
                    category=MetricCategory.CASH_FLOW,
                    benchmark=1.0,
                    rating=self._rate_metric(cash_quality, 1.0, higher_is_better=True),
                    interpretation="Quality of earnings - cash vs accrual profit",
                    formula="Operating Cash Flow / Net Income"
                ))
        
        # Free Cash Flow
        capex = abs(investing_cash_flow) if investing_cash_flow < 0 else 0
        free_cash_flow = operating_cash_flow - capex
        results.append(MetricResult(
            name="Free Cash Flow",
            value=free_cash_flow,
            category=MetricCategory.CASH_FLOW,
            rating="good" if free_cash_flow > 0 else "poor",
            interpretation="Cash available after capital expenditures",
            formula="Operating Cash Flow - Capital Expenditures"
        ))
        
        return results
    
    def calculate_health_score(self, metrics: Dict[str, List[MetricResult]]) -> Dict:
        """
        Calculate overall financial health score (0-100).
        
        Args:
            metrics: Dictionary of calculated metrics
        
        Returns:
            Health score breakdown
        """
        weights = {
            'liquidity': 0.25,
            'profitability': 0.25,
            'solvency': 0.20,
            'efficiency': 0.15,
            'cash_flow': 0.15
        }
        
        category_scores = {}
        
        for category, weight in weights.items():
            category_metrics = metrics.get(category, [])
            if category_metrics:
                # Calculate average rating score for category
                rating_scores = []
                for metric in category_metrics:
                    if metric.rating:
                        score = {'excellent': 100, 'good': 75, 'fair': 50, 'poor': 25}.get(metric.rating, 50)
                        rating_scores.append(score)
                
                if rating_scores:
                    category_scores[category] = sum(rating_scores) / len(rating_scores)
                else:
                    category_scores[category] = 50  # Default neutral score
            else:
                category_scores[category] = 50
        
        # Calculate weighted overall score
        overall_score = sum(
            category_scores.get(cat, 50) * weight 
            for cat, weight in weights.items()
        )
        
        return {
            'overall_score': round(overall_score, 1),
            'category_scores': category_scores,
            'rating': self._get_overall_rating(overall_score),
            'interpretation': self._get_score_interpretation(overall_score)
        }
    
    def _safe_divide(self, numerator: float, denominator: float) -> Optional[float]:
        """Safely divide two numbers, returning None if division is not possible."""
        if denominator is None or denominator == 0:
            return None
        if numerator is None:
            return None
        return numerator / denominator
    
    def _calculate_growth_rate(self, old_value: float, new_value: float) -> Optional[float]:
        """Calculate percentage growth rate."""
        if old_value is None or old_value == 0:
            return None
        if new_value is None:
            return None
        return (new_value - old_value) / abs(old_value)
    
    def _rate_metric(
        self, 
        value: Optional[float], 
        benchmark: Optional[float], 
        higher_is_better: bool = True
    ) -> Optional[str]:
        """Rate a metric value against benchmark."""
        if value is None or benchmark is None:
            return None
        
        ratio = value / benchmark if benchmark != 0 else 1
        
        if higher_is_better:
            if ratio >= 1.2:
                return "excellent"
            elif ratio >= 0.9:
                return "good"
            elif ratio >= 0.6:
                return "fair"
            else:
                return "poor"
        else:
            if ratio <= 0.8:
                return "excellent"
            elif ratio <= 1.1:
                return "good"
            elif ratio <= 1.5:
                return "fair"
            else:
                return "poor"
    
    def _interpret_current_ratio(self, value: Optional[float]) -> str:
        if value is None:
            return "Unable to calculate"
        if value >= 2.0:
            return "Excellent liquidity - strong ability to meet short-term obligations"
        elif value >= 1.5:
            return "Good liquidity - comfortable margin for short-term payments"
        elif value >= 1.0:
            return "Adequate liquidity - can meet current obligations"
        else:
            return "Low liquidity - may struggle to meet short-term obligations"
    
    def _interpret_quick_ratio(self, value: Optional[float]) -> str:
        if value is None:
            return "Unable to calculate"
        if value >= 1.5:
            return "Strong liquidity without relying on inventory"
        elif value >= 1.0:
            return "Good ability to meet obligations without selling inventory"
        elif value >= 0.5:
            return "Moderate liquidity - some reliance on inventory"
        else:
            return "Low quick liquidity - heavily dependent on inventory sales"
    
    def _get_overall_rating(self, score: float) -> str:
        if score >= 80:
            return "Excellent"
        elif score >= 65:
            return "Good"
        elif score >= 50:
            return "Fair"
        elif score >= 35:
            return "Needs Attention"
        else:
            return "Critical"
    
    def _get_score_interpretation(self, score: float) -> str:
        if score >= 80:
            return "The business demonstrates strong financial health across all key indicators."
        elif score >= 65:
            return "The business is financially healthy with some areas for potential improvement."
        elif score >= 50:
            return "The business shows moderate financial stability but requires attention in several areas."
        elif score >= 35:
            return "The business faces financial challenges that need to be addressed promptly."
        else:
            return "The business is in critical financial condition requiring immediate action."


# Create global instance
metrics_calculator = MetricsCalculator()
