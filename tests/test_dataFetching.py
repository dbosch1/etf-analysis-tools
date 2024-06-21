import unittest
from etf_analysis.dataFetching import listAvailableTickers, getEtfHoldings

class TestDataFetching(unittest.TestCase):

    def test_listAvailableTickers(self):
        """
        Test the listAvailableTickers function to ensure it returns the correct list of tickers.
        """
        expected_tickers = ['NWLG', 'JGRO', 'ESGY', 'QQMG', 'NULG', 'LRGE', 'HAPI']
        result = listAvailableTickers()
        self.assertEqual(result, expected_tickers, "The list of available tickers does not match the expected output.")
    
    def test_getEtfHoldings_invalidTicker(self):
        """
        Test getEtfHoldings function to ensure it raises a ValueError for an invalid ticker.
        """
        invalid_ticker = "INVALID"
        with self.assertRaises(ValueError):
            getEtfHoldings(invalid_ticker)
    
    def test_getEtfHoldings_validTicker(self):
        """
        Test getEtfHoldings function to ensure it returns data for a valid ticker.
        """
        valid_ticker = "NWLG"
        holdings_df, financial_data_dict = getEtfHoldings(valid_ticker)
        
        self.assertIsInstance(holdings_df, pd.DataFrame, "Holdings should be a DataFrame")
        self.assertIsInstance(financial_data_dict, dict, "Financial data should be a dictionary")
        
        # Verify the DataFrame is not empty
        self.assertFalse(holdings_df.empty, "Holdings DataFrame should not be empty")
        
        # Verify the dictionary contains data for each symbol in the holdings DataFrame
        for symbol in holdings_df['Symbol Symbol']:
            self.assertIn(symbol, financial_data_dict, f"Financial data dictionary should contain data for {symbol}")
            self.assertIsInstance(financial_data_dict[symbol], pd.DataFrame, f"Financial data for {symbol} should be a DataFrame")

if __name__ == '__main__':
    unittest.main()
