# Etract
import yfinance as yf
import numpy as np
import pandas as pd

# transform and load
import sqlite3
from datetime import date

class stock_data():
    """
    manipulate stock data
    """
    def __init__(self):
        self.connection = sqlite3.connect("stocks.sqlite",check_same_thread=False)
    
    def delete_table(self,ticker):
        """
        delete the ticker from the database
        """
        cursor = self.connection.cursor()
        cursor.execute(f"DROP TABLE {ticker}")
        print(f"table {ticker} deleted")
        
    def add_table(self,ticker):
        print(f"downloading {ticker} ...")
        df = yf.download(tickers=ticker)
        n_inserted = df.to_sql(name=ticker,con=self.connection,if_exists="replace")
        print(f"number of inserted data is : {n_inserted}")
        print("shape ",df.shape)
        print("\n----------------------")
        
    def read_table(self,ticker):
        sql = f"""
            SELECT *
            FROM '{ticker}'
            """
        
        df = pd.read_sql(sql,con=self.connection,index_col="Date").drop_duplicates()
        
        print(f"{ticker} shape ",df.shape)
        
        return df

