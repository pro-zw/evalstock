# -*- coding: utf-8 -*-

import pandas as pd
from finance_report.models import Stock


def main():

    stock_url = "http://www.asx.com.au/asx/research/ASXListedCompanies.csv"
    stock_df = pd.read_csv(stock_url, index_col=['ASX code'], skiprows=2)

    for row in stock_df.iterrows():
        code = Stock.internal_code(row[0], 'Australia')

        stock, created = Stock.objects.update_or_create(
            stock_code=code,
            defaults={
                'stock_name': row[1]['Company name'],
                'industry': row[1]['GICS industry group']
            })
        stock.save()
