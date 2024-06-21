# __init__.py

from .dataFetching import listAvailableTickers, getEtfHoldings
from .riskAnalysis import calculateRiskMetrics, compareEtfPerformance, calculateVaR, calculateCVaR, calculateAlphaBeta
from .sustainableInvestors import getSustainabilityScores, optimizeSustainablePortfolio, compareEsgEtfRatings
from .dataVisualization import plotOptimizedPortfolioWeights, plotPortfolioPerformance, plotRiskMetrics

__all__ = [
    'listAvailableTickers',
    'getEtfHoldings',
    'calculateRiskMetrics',
    'compareEtfPerformance',
    'calculateVaR',
    'calculateCVaR',
    'calculateAlphaBeta',
    'getSustainabilityScores',
    'optimizeSustainablePortfolio',
    'compareEsgEtfRatings',
    'plotOptimizedPortfolioWeights',
    'plotPortfolioPerformance',
    'plotRiskMetrics'
]
