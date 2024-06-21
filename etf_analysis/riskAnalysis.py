import yfinance as yf
import pandas as pd
import numpy as np

def calculateRiskMetrics(etfTicker):
    """
    Calculate risk metrics (Beta, Sharpe Ratio, Maximum Drawdown) for the ETF.

    Parameters:
    etfTicker (str): The ticker of the ETF.

    Returns:
    dict: A dictionary with risk metrics such as Beta, Sharpe Ratio, and Maximum Drawdown, with keys as metric names and values as their respective calculations.

    Raises:
    ValueError: If the provided ticker is not available in the package.
    Exception: If there is an error in fetching financial data.
    """
    stock = yf.Ticker(etfTicker)
    financialData = stock.history(period="1y")
    dailyReturns = financialData['Close'].pct_change().dropna()

    marketData = yf.Ticker('^GSPC').history(period="1y")
    marketReturns = marketData['Close'].pct_change().dropna()
    beta = dailyReturns.cov(marketReturns) / marketReturns.var()
    sharpeRatio = (dailyReturns.mean() / dailyReturns.std()) * (252 ** 0.5)
    maxDrawdown = (financialData['Close'] / financialData['Close'].cummax() - 1).min()

    riskMetrics = {
        'Beta': beta,
        'Sharpe Ratio': sharpeRatio,
        'Maximum Drawdown': maxDrawdown
    }

    print(f"Risk Metrics for {etfTicker}:")
    for metric, value in riskMetrics.items():
        print(f"{metric}: {value:.4f}")

    return riskMetrics

def compareEtfPerformance(etfTickers, period='1y'):
    """
    Compare the performance of multiple ETFs over a specified period.

    Parameters:
    etfTickers (list): List of ETF tickers to compare.
    period (str): The period over which to compare performance (default is '1y').

    Returns:
    pd.DataFrame: DataFrame with the performance of each ETF, ordered from best to worst cumulative return.
    """
    performanceData = {}
    for etfTicker in etfTickers:
        stock = yf.Ticker(etfTicker)
        financialData = stock.history(period=period)
        cumulativeReturn = (financialData['Close'][-1] / financialData['Close'][0] - 1) * 100
        performanceData[etfTicker] = cumulativeReturn

    performanceDf = pd.DataFrame.from_dict(performanceData, orient='index', columns=['Cumulative Return'])
    performanceDf = performanceDf.sort_values(by='Cumulative Return', ascending=False)
    
    return performanceDf

def calculateVaR(etfTicker, confidenceLevel=0.95):
    """
    Calculate Value at Risk (VaR) for a given confidence level.

    Parameters:
    etfTicker (str): The ticker of the ETF.
    confidenceLevel (float): Confidence level for VaR (default is 0.95).

    Returns:
    float: VaR value.
    """
    stock = yf.Ticker(etfTicker)
    dailyReturns = stock.history(period="1y")['Close'].pct_change().dropna()
    VaR = np.percentile(dailyReturns, (1 - confidenceLevel) * 100)
    return VaR

def calculateCVaR(etfTicker, confidenceLevel=0.95):
    """
    Calculate Conditional Value at Risk (CVaR) for a given confidence level.

    Parameters:
    etfTicker (str): The ticker of the ETF.
    confidenceLevel (float): Confidence level for CVaR (default is 0.95).

    Returns:
    float: CVaR value.
    """
    stock = yf.Ticker(etfTicker)
    dailyReturns = stock.history(period="1y")['Close'].pct_change().dropna()
    VaR = calculateVaR(etfTicker, confidenceLevel)
    CVaR = dailyReturns[dailyReturns <= VaR].mean()
    return CVaR

def calculateAlphaBeta(etfTicker, benchmarkTicker='^GSPC'):
    """
    Calculate Alpha and Beta of the ETF relative to a benchmark.

    Parameters:
    etfTicker (str): The ticker of the ETF.
    benchmarkTicker (str): The ticker of the benchmark index (default is '^GSPC').

    Returns:
    dict: A dictionary with Alpha and Beta values.
    """
    etf = yf.Ticker(etfTicker)
    benchmark = yf.Ticker(benchmarkTicker)

    etfData = etf.history(period="1y")
    benchmarkData = benchmark.history(period="1y")

    etfReturns = etfData['Close'].pct_change().dropna()
    benchmarkReturns = benchmarkData['Close'].pct_change().dropna()

    beta = etfReturns.cov(benchmarkReturns) / benchmarkReturns.var()
    alpha = etfReturns.mean() - beta * benchmarkReturns.mean()

    alphaBeta = {
        'Alpha': alpha,
        'Beta': beta
    }

    return alphaBeta
