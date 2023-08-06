#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This class abstracts the logic for getting stock data from NASDAQ.

@author: rajsaswa
"""
import logging, urllib2
from .. import stock
from BeautifulSoup import BeautifulSoup
from . import stock_config

class NasdaqStockConfig(stock_config.StockConfig):
    STOCK_URL = "https://www.nasdaq.com/"
    STOCK_QUOTE = "symbol"
    BACK_SLASH = "/"
    
    @staticmethod
    def get_html_content(url):
        """
        Gets the html content given a URL.
        """
        response = urllib2.urlopen(url)
        html_content = response.read()
        logging.debug("Html content: %s", html_content)
        return BeautifulSoup(html_content)

    @staticmethod
    def get_stock_url(stock_symbol):
        """
        Gets the NASDAQ url for the stock given a stock symbol.
        """
        return NasdaqStockConfig.STOCK_URL + NasdaqStockConfig.BACK_SLASH + \
            NasdaqStockConfig.STOCK_QUOTE + NasdaqStockConfig.BACK_SLASH + \
            stock_symbol
    
    @staticmethod
    def get_stock_data(stock_symbol):
        """
        Gets the Stock data given a stock symbol.
        """
        bs_content = NasdaqStockConfig. \
            get_html_content(NasdaqStockConfig.get_stock_url(stock_symbol))
        stock_val_container = bs_content.find("div", 
                                                 {"id": "qwidget_lastsale"})
        
        logging.debug("Obtained stock value for stock: %s", stock_val_container.text)
        
        stock_diff_container = bs_content.find("div", 
                                               {"id": "qwidget_netchange"})
        logging.debug("Obtained stock difference for stock: %s", stock_diff_container.text)
        
        stock_diff_percentage = bs_content.find("div", 
                                                {"id": "qwidget_percent"})
        logging.debug("Obtained stock difference in percentage for stock: %s", stock_diff_percentage.text)
        
        margin = None
        arrow_container = str(bs_content.find("div", {"id": "qwidget-arrow"}))
        if "arrow-red" in arrow_container:
            margin = stock.Stock.STOCK_VAL_DECREASE
        else:
            margin = stock.Stock.STOCK_VAL_INCREASE
            
        logging.debug("Obtained stock margin: %s", margin)
        return stock.Stock(stock_symbol, stock_val_container.text, stock_diff_container.text, 
                     stock_diff_percentage.text, margin)
