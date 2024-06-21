import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
from io import StringIO
import logging

logging.basicConfig(level=logging.INFO)

availableEtfTickers = ['NWLG', 'JGRO', 'ESGY', 'QQMG', 'NULG', 'LRGE', 'HAPI']

def listAvailableTickers():
    """
    Returns a list of available ETF tickers specifically selected for the purposes of this package.

    Returns:
    list: A list of strings representing the available ETF tickers.
    """
    return availableEtfTickers

def getEtfHoldings(etfTicker):
    """
    Get the holdings of an ETF and their financial data from https://www.etfdb.com/etf/{etfTicker}/#holdings.

    Parameters:
    etfTicker (str): The ticker of the ETF.

    Returns:
    tuple: A tuple containing:
        - holdingsDf (pd.DataFrame): DataFrame of ETF holdings.
        - financialDataDict (dict): Dictionary with stock tickers as keys and their financial data as values (DataFrames).
    
    Raises:
    ValueError: If the provided ticker is not available in the package.
    Exception: If the ETF holdings page fails to load or the holdings table is not found.
    """
    if etfTicker not in availableEtfTickers:
        raise ValueError(f'Ticker {etfTicker} is not available in the package.')
    
    url = f"https://www.etfdb.com/etf/{etfTicker}/#holdings"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f'Failed to load page {url}')
    
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'etf-holdings'})
    if not table:
        raise Exception('No holdings table found on the page')

    holdingsDf = pd.read_html(StringIO(str(table)))[0]
    holdingsDf = holdingsDf[~holdingsDf['Symbol Symbol'].str.contains("Export All Holdings to CSV", na=False)]

    financialDataDict = {}
    for symbol in holdingsDf['Symbol Symbol']:
        try:
            stock = yf.Ticker(symbol)
            financialData = stock.history(period="1y")
            financialDataDict[symbol] = financialData
        except Exception as e:
            logging.error(f"Error retrieving data for {symbol}: {e}")
            financialDataDict[symbol] = pd.DataFrame()

    return holdingsDf, financialDataDict
