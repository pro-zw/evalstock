# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt

from django.db.models import Q

import magic_formula.models as magic_formula_models

# 设置图形输出默认参数
font_name = './eval_utility/STHeiti_Medium_1.ttf'
font_prop = font_manager.FontProperties(fname=font_name)
mpl.rcParams['font.family'] = font_prop.get_name()
mpl.rcParams['axes.unicode_minus'] = False


def export_results():

    # 读取股票最新市场数据
    stock_quote_df = pd.read_csv('./eval_utility/china_stock_overview.csv',
                                 index_col=['股票名称'], parse_dates=True)

    eligible_stocks = (
        magic_formula_models.LatestIndex.objects
                            .filter(
                                stock__market_value__gte=2e10,
                                stock__financial_report_date='2017-03-31',
                                roce_ttm__lte=2.0,  # 太大的值不可信
                                ebit_without_joint_ttm__gt=0.0,
                                ebit_with_joint_ttm__gt=0.0,
                                # net_profit_reality__gt=0.6,
                                # net_profit_reality__lt=2
                                )
                            .filter(Q(stock__stock_code__endswith='.sh')
                                    | Q(stock__stock_code__endswith='.sz'))
                            .prefetch_related('stock'))

    eligible_stock_df = (pd.DataFrame(list(eligible_stocks.values(
        'stock__stock_code', 'stock__stock_name',
        'stock__market_value', 'stock__industry',
        'roce', 'roce_ttm', 'earnings_yield', 'net_profit_reality')))
        .set_index('stock__stock_name'))

    # 简单指标过滤
    eligible_stock_df['市净率'] = stock_quote_df['市净率']
    eligible_stock_df = eligible_stock_df[eligible_stock_df['市净率'] <= 3.5]

    eligible_stock_df['市盈率TTM'] = stock_quote_df['市盈率TTM']
    eligible_stock_df = eligible_stock_df[eligible_stock_df['市盈率TTM'] <= 20]
    eligible_stock_df = eligible_stock_df[eligible_stock_df['市盈率TTM'] >= 5]

    # 排序资本回报率
    eligible_stock_df.sort_values(by=['roce_ttm'], axis=0, ascending=False, inplace=True)
    eligible_stock_df['roce_rate'] = range(1, len(eligible_stock_df) + 1)

    # 排序收益率
    eligible_stock_df.sort_values(by=['earnings_yield'], axis=0, ascending=False, inplace=True)
    eligible_stock_df['earnings_yield_rate'] = range(1, len(eligible_stock_df) + 1)

    # 计算综合排名
    eligible_stock_df['overall_rate'] = eligible_stock_df['roce_rate'] + eligible_stock_df['earnings_yield_rate']
    eligible_stock_df.sort_values(by=['overall_rate'], axis=0, ascending=True, inplace=True)

    eligible_stock_df.to_csv('./eval_utility/china_magic_formula_results.csv', encoding='utf-8')
    eligible_stock_df = eligible_stock_df.reset_index().set_index('stock__stock_code')

    f, ax = plt.subplots()
    ax.scatter(eligible_stock_df['roce'], eligible_stock_df['earnings_yield'])
    ax.set_title('神奇公式分布图')
    ax.set_xlabel('投入资本回报率')
    ax.set_ylabel('收益率')
    for i, stock_name in enumerate(eligible_stock_df['stock__stock_name']):
        ax.annotate(stock_name, (eligible_stock_df['roce'].iloc[i], eligible_stock_df['earnings_yield'].iloc[i]))
    plt.show()


def plot_roce_ttm(stock_code: str):
    from magic_formula.models import HistoricalKpi

    historical_kpi = HistoricalKpi.objects.filter(stock__stock_code=stock_code)
    roce_ttm_df = (pd.DataFrame(list(historical_kpi.values(
        'stock__stock_name', 'report_date', 'roce_ttm')))
        .set_index('report_date'))

    plt.figure()
    roce_ttm_df['roce_ttm'].plot(label=roce_ttm_df['stock__stock_name'][-1])
    plt.legend()
    plt.show()
