# The first step is to download pdf report from Morning Star
# The link is like:
# http://www2.aspecthuntley.com.au/pdf/sil/advancedprofile/today/NAB_advancedprofile.pdf

import urllib.request
import os
import time

from finance_report.models import Stock


def download_advanced_profile():
    """Batch download stock pdf profiles

    Note the text cannot be extracted directly from the downloaded pdfs,
    it must be processed by OCR, and I use the software named PDFelement Pro version
    :return:
    """
    for stock in Stock.objects.filter(stock_code__endswith='.asx'):
        try:
            report_name = '{}_advancedprofile.pdf'.format(stock.stock_code[:3].upper())
            report_link = \
                'http://www2.aspecthuntley.com.au/pdf/sil/advancedprofile/today/{}'\
                .format(report_name)

            urllib.request.urlretrieve(
                report_link,
                os.path.join('./finance_report/data/australia_morning_star_reports_pdf/', report_name))

            time.sleep(0.01)
        except Exception as exception:
            print(exception)
            continue
