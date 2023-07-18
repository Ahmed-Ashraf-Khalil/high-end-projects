#compress warnings
import logging
import warnings
import requests

warnings.filterwarnings("ignore")
logger = logging.getLogger('cmdstanpy')
logger.addHandler(logging.NullHandler())
logger.propagate = False
logger.setLevel(logging.CRITICAL)

from finnlp.data_sources.news.finnhub_date_range import Finnhub_Date_Range #news gathering

from bardapi import Bard #bard llm
from bardapi.constants import SESSION_HEADERS

import yfinance as yf #information about tickers
import pandas as pd #storing data in dataframe
from tqdm.notebook import tqdm 
from datetime import date



def news_and_FA(ticker,PSID,PSIDTS,PSIDCC,finhub_token,start_date,end_date):
    """
        do the fundamental analysis part also as collecting news about stock
    input:: 
    ticker sympol 
    bard token : Available at https://bard.google.com inspect-> application-> cookies-> first folder-> copy value of __Secure-1PSID
    finhub token : Available at https://finnhub.io/dashboard
    start date of the news and the end date in this format 'year-month-day'

    retrun :: 
    dataframe of the news , the fundamental analysis of bard AI """
    

    #tokens
    news_downloader = Finnhub_Date_Range({"token":finhub_token})

    session = requests.Session()
    session.headers = SESSION_HEADERS
    session.cookies.set("__Secure-1PSID", PSID)
    session.cookies.set("__Secure-1PSIDTS", PSIDTS)
    session.cookies.set("__Secure-1PSIDCC", PSIDCC)
    bard = Bard(token=PSID, session=session)


    #company name and ticker info
    company_name = (yf.Ticker(ticker)).info['longName']

    #date format and ranges
    date_list = pd.date_range(start_date,end_date)
    date_list = [date.strftime("%Y-%m-%d") for date in date_list]

    #geting the news and changing it to dataframe
    news_downloader.download_date_range_stock(start_date = start_date,end_date = end_date, stock = ticker)
    news = news_downloader.dataframe
    news["date"] = news.datetime.dt.date
    news["date"] = news["date"].astype("str")
    news = news.sort_values("datetime")

    headline_list = []
    answers = {}

    for date in tqdm(date_list):
        # news data
        today_news = news[news.date == date]
        headlines = today_news.headline.tolist()
        headlines = "\n".join(headlines)
        headline_list.append(headlines)

        prompt = f"There are news about the {company_name} Company, whose stock code is '{ticker}'. The news are separated in '\n'. The news are {headlines}. \
            Please give a brief summary of these news and analyse the possible trend of the stock price of the {company_name} Company.\
            Please give trends results based on different possible assumptions"

        answers[date]=bard.get_answer(prompt)['content']

        answers["headlines"]=headline_list

    return news,answers