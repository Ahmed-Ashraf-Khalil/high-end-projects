import pandas as pd
from database import stock_data
import plotly.express as px
import matplotlib.pyplot as plt

class stock_more_info():
    def __init__(self):
        pass
    
    def technical_analysis(self, ticker, n=14, m=2):
        self.df = stock_data().read_table(ticker)
        # takes dataframe on input
        # n = smoothing length
        # m = number of standard deviations away from MA

        #typical price
        TP = (self.df['High'] + self.df['Low'] + self.df['Close']) / 3
        # but we will use Adj close instead for now, depends

        data = TP
        #data = df['Adj Close']

        # takes one column from dataframe
        B_MA = pd.Series((data.rolling(n, min_periods=n).mean()), name='B_MA')
        sigma = data.rolling(n, min_periods=n).std() 

        BU = pd.Series((B_MA + m * sigma), name='BU')
        BL = pd.Series((B_MA - m * sigma), name='BL')

        df = self.df.join(B_MA)
        df = df.join(BU)
        df = df.join(BL)
        
        df['SMA20'] = df['Close'].rolling(20).mean() #20 days moving average

        df['SMA50'] = df['Close'].rolling(50).mean() #500 days moving average

        df['SMA200'] = df['Close'].rolling(200).mean() #200 days moving average

        df["daily_returns"] = df['Close'].pct_change() #daily returns 
        
        self.df = df.copy()
        
        return df
    
    def plot_info(self):
        
        print("moving averages 20/50/200")
        fig = px.line(data_frame=self.df, x=self.df.index, y=['Close','SMA20', 'SMA50', 'SMA200'])
        fig.show();

        print("\nthe last 200 days")
        self.df['Close'].iloc[-200:].plot()
        self.df['SMA20'].iloc[-200:].plot()
        self.df['SMA50'].iloc[-200:].plot()
        self.df['SMA200'].iloc[-200:].plot()

        plt.xticks(rotation=45)
        plt.legend()
        plt.show();

        print("\nbollinger bands")
        fig = px.line(data_frame=self.df, x=self.df.index, y=['Close','BU',"BL","B_MA"])
        fig.show();

        print("\nthe last 200 days")
        self.df['Close'].iloc[-200:].plot()
        self.df['BU'].iloc[-200:].plot()
        self.df['B_MA'].iloc[-200:].plot()
        self.df['BL'].iloc[-200:].plot()
        plt.xticks(rotation=45)

        plt.legend()
        plt.show();

        print("\nreturns ::")
        fig = px.line(data_frame=self.df,x=self.df.index,y=abs(self.df["daily_returns"]))
        fig.show();