import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plotOptimizedPortfolioWeights(optimizedSustainableHoldings):
    """
    Plot the weights of the optimized portfolio.

    Parameters:
    optimizedHoldings (pd.DataFrame): DataFrame of optimized holdings with a 'Weight' column.

    Returns:
    None: Displays the plot.
    """
    plt.figure(figsize=(12, 8))
    optimizedSustainableHoldings = optimizedSustainableHoldings[0].sort_values(by='Weight', ascending=False)
    sns.barplot(x='Symbol Symbol', y='Weight', data=optimizedSustainableHoldings, palette='viridis')
    plt.title('Optimized Sustainable Portfolio Weights')
    plt.xlabel('Holdings')
    plt.ylabel('Weight')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

def plotPortfolioPerformance(performanceDf):
    """
    Plot the cumulative returns of multiple ETFs over a specified period.

    Parameters:
    performanceDf (pd.DataFrame): DataFrame with ETF tickers as index and 'Cumulative Return' as column.

    Returns:
    None: Displays the plot.
    """
    plt.figure(figsize=(12, 6))
    sns.barplot(x=performanceDf.index, y='Cumulative Return', data=performanceDf, palette='muted')
    plt.title('ETF Performance Comparison')
    plt.xlabel('ETF Tickers')
    plt.ylabel('Cumulative Return (%)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

def plotRiskMetrics(riskMetrics):
    """
    Plot the risk metrics of an ETF.

    Parameters:
    riskMetrics (dict): Dictionary with risk metrics such as Beta, Sharpe Ratio, and Maximum Drawdown.

    Returns:
    None: Displays the plot.
    """
    metrics = list(riskMetrics.keys())
    values = list(riskMetrics.values())

    plt.figure(figsize=(10, 6))
    sns.barplot(x=metrics, y=values, palette='coolwarm')
    plt.title('Risk Metrics')
    plt.xlabel('Metrics')
    plt.ylabel('Values')
    plt.grid(True)
    plt.show()
