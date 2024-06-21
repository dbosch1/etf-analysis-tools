import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
from io import StringIO
import logging
import pandas as pd

def getSustainabilityScores(etfTicker):
    """
    Get the ESG scores for the holdings of an ETF.

    Parameters:
    etfTicker (str): The ticker of the ETF.

    Returns:
    tuple: A tuple containing:
        - etfEsgScore (float): The average ESG score of the ETF.
        - holdingsDf (pd.DataFrame): DataFrame of ETF holdings with an additional 'ESG Score' column.
    
    Raises:
    ValueError: If the provided ticker is not available in the package.
    Exception: If the ETF holdings page fails to load or the holdings table is not found.
    """
    holdingsDf, _ = getEtfHoldings(etfTicker)
    esgScores = {
        'AAPL': 80, 'MSFT': 85, 'AMZN': 75, 'GOOGL': 90,
        'GOOG': 90, 'LRCX': 70, 'AVGO': 65, 'ASML': 88, 'TT': 82
    }
    tickerColumn = 'Symbol Symbol'
    holdingsDf['ESG Score'] = holdingsDf[tickerColumn].apply(lambda x: esgScores.get(x, 50))
    etfEsgScore = holdingsDf['ESG Score'].mean()

    return etfEsgScore, holdingsDf

def optimizeSustainablePortfolio(etfTicker, sustainabilityWeight=0.5, returnsWeight=0.5):
    """
    Optimize the portfolio based on returns and sustainability scores.

    Parameters:
    etfTicker (str): The ticker of the ETF.
    sustainabilityWeight (float): Weight for sustainability score (default is 0.5).
    returnsWeight (float): Weight for returns (default is 0.5).

    Returns:
    pd.DataFrame: Optimized holdings sorted by combined score, with columns for weights and combined scores. 
    float: Portfolio returns.
    float: Portfolio volatility.

    Raises:
    ValueError: If the sum of sustainabilityWeight and returnsWeight is not 1.0.
    """
    if sustainabilityWeight + returnsWeight != 1.0:
        raise ValueError("Weights must sum to 1.0")

    holdings, financialDataDict = getEtfHoldings(etfTicker)
    _, holdingsWithEsg = getSustainabilityScores(etfTicker)
    
    returns = []
    volatilities = []
    combinedScores = []
    weights = []

    for idx, row in holdingsWithEsg.iterrows():
        ticker = row['Symbol Symbol']
        if not financialDataDict[ticker].empty:
            dailyReturns = financialDataDict[ticker]['Close'].pct_change().dropna()
            meanReturn = dailyReturns.mean()
            stdReturn = dailyReturns.std()

            combinedScore = returnsWeight * meanReturn + sustainabilityWeight * row['ESG Score']
            combinedScores.append(combinedScore)
            returns.append(meanReturn)
            volatilities.append(stdReturn)
        else:
            combinedScores.append(0)
            returns.append(0)
            volatilities.append(0)

    totalScore = sum(combinedScores)
    weights = [score / totalScore for score in combinedScores]

    portfolioReturns = sum([w * r for w, r in zip(weights, returns)]) * 100
    portfolioVolatility = (sum([w * v for w, v in zip(weights, volatilities)]) ** 0.5) * 100

    optimizedHoldings = holdingsWithEsg.copy()
    optimizedHoldings['Weight'] = weights
    optimizedHoldings['Combined Score'] = combinedScores

    sortedHoldings = optimizedHoldings.sort_values(by='Combined Score', ascending=False)
    return sortedHoldings, portfolioReturns, portfolioVolatility

def compareEsgEtfRatings(etfTickers):
    """
    Compare the mean ESG ratings of multiple ETFs.

    Parameters:
    etfTickers (list): List of ETF tickers to compare.

    Returns:
    pd.DataFrame: DataFrame comparing the mean ESG ratings of the given ETFs, ordered from best to worst ESG rating.
    """
    etfEsgMeans = {}
    for etfTicker in etfTickers:
        _, holdingsWithEsg = getSustainabilityScores(etfTicker)
        meanEsg = holdingsWithEsg['ESG Score'].mean()
        etfEsgMeans[etfTicker] = meanEsg

    esgMeansDf = pd.DataFrame.from_dict(etfEsgMeans, orient='index', columns=['Mean ESG Rating'])
    esgMeansDf = esgMeansDf.transpose()
    esgMeansDf = esgMeansDf.sort_values(by='Mean ESG Rating', axis=1, ascending=False)

    print(esgMeansDf)
    return esgMeansDf
