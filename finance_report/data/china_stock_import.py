# -*- coding: utf-8 -*-
"""Import the fundamental chinese stock information into the database.

The basic stock information imported includes: stock code, stock name,
and industry

If the latest market data is imported, the additional data available 
here includes: market data date (the latest one) and market value

If the latest stock financial data is imported, the additional data
available here includes: financial report date (the latest one)

"""


import pandas as pd
from finance_report.models import Stock


def main():
    """Import the fundamental stock information
    """

    stock_market_df = pd.read_csv(
        './finance_report/data/china_stock_overview.csv',
        index_col=['股票代码'], parse_dates=True)

    stock_df = (stock_market_df[
        ['股票名称', '交易日期', '总市值', '新浪行业']]
        .dropna(subset=['股票名称'])
        .where((pd.notnull(stock_market_df)), None)
    )

    for (code, name,
         market_data_date,
         market_value, industry) in stock_df.itertuples():

        code = code[2:] + '.' + code[0:2]

        stock, created = Stock.objects.update_or_create(
            stock_code=code,
            defaults={
                'stock_name': name,
                'industry': industry,
                'market_data_date': market_data_date,
                'market_value': market_value
            })
        stock.save()

if __name__ == "__main__":
    main()
