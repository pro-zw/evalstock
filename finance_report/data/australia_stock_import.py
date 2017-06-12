# -*- coding: utf-8 -*-

import pandas as pd
from finance_report.models import Stock


def import_stock_list():

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


def import_stock_market_data():
    import time
    from datetime import datetime
    import pandas_datareader.data as web
    from pandas_datareader.yahoo.quotes import _yahoo_codes

    _yahoo_codes.update({'MarketCap': 'j1'})
    _yahoo_codes.update({'LastTradeDate': 'd1'})

    stock_queryset = Stock.objects.filter(stock_code__endswith='.asx')

    for stock in stock_queryset:
        yahoo_code = stock.stock_code[0:3].upper() + '.AX'
        stock_quote = web.get_quote_yahoo(yahoo_code)

        if not stock_quote.empty:
            try:
                last_trade_date_str = stock_quote.loc[yahoo_code, 'LastTradeDate']
                if last_trade_date_str != 'N/A':
                    stock.market_data_date = datetime.strptime(
                        last_trade_date_str,
                        '%m/%d/%Y'
                    )

                market_cap_str = stock_quote.loc[yahoo_code, 'MarketCap']
                market_cap_unit = market_cap_str[-1:]
                if market_cap_unit == 'M':
                    stock.market_value = float(market_cap_str[:-1]) * 1e6
                elif market_cap_unit == 'B':
                    stock.market_value = float(market_cap_str[:-1]) * 1e9
                else:
                    raise Exception(
                        'Unknown yahoo stock market value unit - {}'.format(market_cap_str))

                stock.save()
            except Exception as exception:
                print(exception)
                continue

        # Do not do too quickly, or the Yahoo finance may block us
        time.sleep(0.01)
