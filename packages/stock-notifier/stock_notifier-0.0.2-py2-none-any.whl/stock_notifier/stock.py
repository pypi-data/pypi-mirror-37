#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This class abstracts the details corresponding to a stock.

@author: rajsaswa
"""

class Stock:
    
    STOCK_VAL_INCREASE = "increased"
    STOCK_VAL_DECREASE = "decreased"
    
    def __init__(self, symbol, stock_value, stock_diff, stock_diff_percentage, margin):
        self.stock_value = stock_value
        self.symbol = symbol
        self.stock_diff = stock_diff
        self.stock_diff_percentage = stock_diff_percentage
        self.margin = margin
        
    def get_stock_value(self):
        """
        Stock value of the stock.
        """
        return self.stock_value
    
    def get_stock_symbol(self):
        """
        Stock symbol of the stock.
        """
        return self.symbol
    
    def get_stock_value_difference(self):
        """
        Difference between the last recorded stock value and the current value.
        """
        return self.stock_diff
    
    def get_stock_difference_in_percent(self):
        return self.stock_diff_percentage
    
    def get_stock_margin(self):
        """
        Returns Stock.STOCK_VAL_INCREASE if the get_stock_value_difference()
        has increased and Stock.STOCK_VAL_DECREASE if the value has decreased.
        """
        return self.margin
