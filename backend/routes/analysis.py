"""
Analysis routes for financial analysis endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from datetime import datetime

from analysis import (
    metrics_calculator, MetricsCalculator,
    risk_assessor, 
    creditworthiness_assessor,
    financial_forecaster,
    industry_benchmarker, IndustryBenchmarker
)
from ai import llm_engine
from i18n import translator

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.post("/full")
async def full_analysis(
    financial_data: dict,
    industry: str = "services",
    language: str = "en"
):
    """Perform comprehensive financial analysis."""
    try:
        # Initialize with industry context
        calculator = MetricsCalculator(industry)
        
        # Calculate metrics
        metrics = calculator.calculate_all_metrics(financial_data)
        health_score = calculator.calculate_health_score(metrics)
        
        # Risk assessment
        risk_result = risk_assessor.assess_all_risks(financial_data, metrics)
        
        # Credit assessment
        credit_score = creditworthiness_assessor.assess_creditworthiness(
            financial_data, metrics
        )
        
        # Industry benchmarking
        benchmarker = IndustryBenchmarker(industry)
        benchmark_result = benchmarker.compare_metrics(metrics)
        
        # AI insights
        ai_insights = llm_engine.generate_insights(
            financial_data, metrics, risk_result, language
        )
        
        # Recommendations
        recommendations = llm_engine.generate_recommendations(
            metrics, risk_result, industry, language
        )
        
        return {
            'analysis_id': str(datetime.utcnow().timestamp()),
            'timestamp': datetime.utcnow().isoformat(),
            'health_score': health_score,
            'metrics': {k: [_metric_to_dict(m) for m in v] for k, v in metrics.items()},
            'risk_assessment': risk_result,
            'creditworthiness': {
                'score': credit_score.score,
                'rating': credit_score.rating.value,
                'factors': credit_score.factors,
                'strengths': credit_score.strengths,
                'weaknesses': credit_score.weaknesses
            },
            'industry_benchmark': benchmark_result,
            'ai_insights': ai_insights,
            'recommendations': recommendations,
            'language': language
        }
        
    except Exception as e:
        raise HTTPException(500, f"Analysis error: {str(e)}")


@router.post("/metrics")
async def calculate_metrics(
    financial_data: dict,
    industry: str = "services"
):
    """Calculate financial metrics."""
    calculator = MetricsCalculator(industry)
    metrics = calculator.calculate_all_metrics(financial_data)
    health_score = calculator.calculate_health_score(metrics)
    
    return {
        'metrics': {k: [_metric_to_dict(m) for m in v] for k, v in metrics.items()},
        'health_score': health_score
    }


@router.post("/risk")
async def assess_risk(
    financial_data: dict,
    metrics: Optional[dict] = None
):
    """Perform risk assessment."""
    if not metrics:
        calculator = MetricsCalculator()
        metrics = calculator.calculate_all_metrics(financial_data)
    
    return risk_assessor.assess_all_risks(financial_data, metrics)


@router.post("/credit-score")
async def assess_creditworthiness(
    financial_data: dict,
    business_info: Optional[dict] = None
):
    """Assess creditworthiness and generate credit score."""
    calculator = MetricsCalculator()
    metrics = calculator.calculate_all_metrics(financial_data)
    
    score = creditworthiness_assessor.assess_creditworthiness(
        financial_data, metrics, business_info
    )
    
    return {
        'score': score.score,
        'rating': score.rating.value,
        'factors': score.factors,
        'strengths': score.strengths,
        'weaknesses': score.weaknesses,
        'recommendations': score.recommendations
    }


@router.post("/forecast")
async def generate_forecast(
    financial_data: dict,
    periods: int = 12
):
    """Generate financial forecasts."""
    return financial_forecaster.generate_forecast(financial_data, periods)


@router.post("/benchmark")
async def benchmark_analysis(
    metrics: dict,
    industry: str = "services"
):
    """Compare metrics against industry benchmarks."""
    benchmarker = IndustryBenchmarker(industry)
    return benchmarker.compare_metrics(metrics)


def _metric_to_dict(metric) -> dict:
    """Convert MetricResult to dictionary."""
    if hasattr(metric, 'name'):
        return {
            'name': metric.name,
            'value': metric.value,
            'category': metric.category.value if hasattr(metric.category, 'value') else str(metric.category),
            'benchmark': metric.benchmark,
            'rating': metric.rating,
            'interpretation': metric.interpretation,
            'formula': metric.formula
        }
    return metric
