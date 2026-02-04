"""
Industry benchmarking module.
Compares business metrics against industry standards.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class IndustryType(Enum):
    MANUFACTURING = "manufacturing"
    RETAIL = "retail"
    AGRICULTURE = "agriculture"
    SERVICES = "services"
    LOGISTICS = "logistics"
    ECOMMERCE = "ecommerce"
    HEALTHCARE = "healthcare"
    CONSTRUCTION = "construction"
    OTHER = "other"


@dataclass
class BenchmarkComparison:
    metric: str
    company_value: float
    industry_avg: float
    industry_best: float
    percentile: int
    status: str  # above_average, average, below_average


class IndustryBenchmarker:
    """Provides industry-specific benchmarking for financial metrics."""
    
    # Industry benchmark data (simplified for demo)
    BENCHMARKS = {
        'manufacturing': {
            'current_ratio': {'avg': 1.5, 'best': 2.5, 'poor': 1.0},
            'gross_margin': {'avg': 0.25, 'best': 0.40, 'poor': 0.15},
            'net_margin': {'avg': 0.08, 'best': 0.15, 'poor': 0.03},
            'debt_to_equity': {'avg': 1.0, 'best': 0.5, 'poor': 2.0},
            'inventory_turnover': {'avg': 6.0, 'best': 10.0, 'poor': 3.0},
            'roa': {'avg': 0.06, 'best': 0.12, 'poor': 0.02},
        },
        'retail': {
            'current_ratio': {'avg': 1.2, 'best': 2.0, 'poor': 0.8},
            'gross_margin': {'avg': 0.30, 'best': 0.45, 'poor': 0.20},
            'net_margin': {'avg': 0.05, 'best': 0.10, 'poor': 0.02},
            'debt_to_equity': {'avg': 0.8, 'best': 0.4, 'poor': 1.5},
            'inventory_turnover': {'avg': 8.0, 'best': 15.0, 'poor': 4.0},
            'roa': {'avg': 0.05, 'best': 0.10, 'poor': 0.01},
        },
        'services': {
            'current_ratio': {'avg': 1.5, 'best': 2.5, 'poor': 1.0},
            'gross_margin': {'avg': 0.40, 'best': 0.60, 'poor': 0.25},
            'net_margin': {'avg': 0.15, 'best': 0.25, 'poor': 0.05},
            'debt_to_equity': {'avg': 0.5, 'best': 0.2, 'poor': 1.0},
            'receivables_turnover': {'avg': 10.0, 'best': 15.0, 'poor': 6.0},
            'roa': {'avg': 0.10, 'best': 0.20, 'poor': 0.03},
        },
        'ecommerce': {
            'current_ratio': {'avg': 1.3, 'best': 2.0, 'poor': 0.8},
            'gross_margin': {'avg': 0.35, 'best': 0.50, 'poor': 0.20},
            'net_margin': {'avg': 0.06, 'best': 0.12, 'poor': 0.00},
            'debt_to_equity': {'avg': 0.7, 'best': 0.3, 'poor': 1.5},
            'inventory_turnover': {'avg': 10.0, 'best': 20.0, 'poor': 5.0},
            'roa': {'avg': 0.08, 'best': 0.15, 'poor': 0.02},
        },
        'logistics': {
            'current_ratio': {'avg': 1.2, 'best': 1.8, 'poor': 0.8},
            'gross_margin': {'avg': 0.20, 'best': 0.30, 'poor': 0.10},
            'net_margin': {'avg': 0.05, 'best': 0.10, 'poor': 0.02},
            'debt_to_equity': {'avg': 1.2, 'best': 0.6, 'poor': 2.5},
            'asset_turnover': {'avg': 1.5, 'best': 2.5, 'poor': 0.8},
            'roa': {'avg': 0.04, 'best': 0.08, 'poor': 0.01},
        },
        'agriculture': {
            'current_ratio': {'avg': 1.4, 'best': 2.0, 'poor': 0.9},
            'gross_margin': {'avg': 0.20, 'best': 0.35, 'poor': 0.10},
            'net_margin': {'avg': 0.06, 'best': 0.12, 'poor': 0.02},
            'debt_to_equity': {'avg': 0.8, 'best': 0.4, 'poor': 1.5},
            'inventory_turnover': {'avg': 4.0, 'best': 8.0, 'poor': 2.0},
            'roa': {'avg': 0.05, 'best': 0.10, 'poor': 0.02},
        }
    }
    
    def __init__(self, industry: str = 'other'):
        self.industry = industry.lower()
        self.benchmarks = self.BENCHMARKS.get(self.industry, self.BENCHMARKS.get('services'))
    
    def compare_metrics(self, metrics: Dict) -> Dict:
        comparisons = []
        
        metric_mapping = {
            'Current Ratio': 'current_ratio',
            'Gross Profit Margin': 'gross_margin',
            'Net Profit Margin': 'net_margin',
            'Debt to Equity Ratio': 'debt_to_equity',
            'Inventory Turnover': 'inventory_turnover',
            'Return on Assets (ROA)': 'roa',
            'Receivables Turnover': 'receivables_turnover',
            'Asset Turnover': 'asset_turnover'
        }
        
        for category, metric_list in metrics.items():
            for metric in metric_list:
                name = metric.name if hasattr(metric, 'name') else metric.get('name', '')
                value = metric.value if hasattr(metric, 'value') else metric.get('value')
                
                if name in metric_mapping and value is not None:
                    benchmark_key = metric_mapping[name]
                    if benchmark_key in self.benchmarks:
                        comparison = self._compare_single(name, value, self.benchmarks[benchmark_key])
                        comparisons.append(comparison)
        
        return {
            'industry': self.industry,
            'comparisons': [self._comparison_to_dict(c) for c in comparisons],
            'summary': self._generate_summary(comparisons),
            'overall_ranking': self._calculate_ranking(comparisons)
        }
    
    def _compare_single(self, name: str, value: float, benchmark: Dict) -> BenchmarkComparison:
        avg = benchmark['avg']
        best = benchmark['best']
        poor = benchmark['poor']
        
        # Determine if higher is better
        higher_better = name not in ['Debt to Equity Ratio']
        
        # Calculate percentile (simplified)
        if higher_better:
            if value >= best: percentile = 90
            elif value >= avg: percentile = 50 + int(40 * (value - avg) / (best - avg))
            elif value >= poor: percentile = 10 + int(40 * (value - poor) / (avg - poor))
            else: percentile = 10
        else:
            if value <= best: percentile = 90
            elif value <= avg: percentile = 50 + int(40 * (avg - value) / (avg - best))
            elif value <= poor: percentile = 10 + int(40 * (poor - value) / (poor - avg))
            else: percentile = 10
        
        # Determine status
        if percentile >= 70: status = 'above_average'
        elif percentile >= 40: status = 'average'
        else: status = 'below_average'
        
        return BenchmarkComparison(
            metric=name, company_value=value, industry_avg=avg,
            industry_best=best, percentile=percentile, status=status
        )
    
    def _comparison_to_dict(self, c: BenchmarkComparison) -> Dict:
        return {
            'metric': c.metric, 'company_value': c.company_value,
            'industry_avg': c.industry_avg, 'industry_best': c.industry_best,
            'percentile': c.percentile, 'status': c.status
        }
    
    def _generate_summary(self, comparisons: List[BenchmarkComparison]) -> Dict:
        above = sum(1 for c in comparisons if c.status == 'above_average')
        below = sum(1 for c in comparisons if c.status == 'below_average')
        return {
            'above_average_count': above,
            'below_average_count': below,
            'total_compared': len(comparisons)
        }
    
    def _calculate_ranking(self, comparisons: List[BenchmarkComparison]) -> str:
        if not comparisons:
            return 'insufficient_data'
        avg_percentile = sum(c.percentile for c in comparisons) / len(comparisons)
        if avg_percentile >= 75: return 'top_quartile'
        elif avg_percentile >= 50: return 'above_median'
        elif avg_percentile >= 25: return 'below_median'
        else: return 'bottom_quartile'


industry_benchmarker = IndustryBenchmarker()
