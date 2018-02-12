#!/usr/bin/env python
# -*-coding: utf-8 -*-

from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
import myurl


def get_hs300_stock_code():
    __get_hs3000_stock_code(download=False)


def download_hs300_stock_code():
    __get_hs3000_stock_code(download=True)


def __get_hs3000_stock_code(download=False):
    codes = []
    base_url = 'http://money.finance.sina.com.cn/d/api/openapi_proxy.php/?__s=%s&callback=%s'
    callback_arg = 'FDC_DC.theTableData'

    cur_page = 1
    each_page_count = 80
    total = cur_page * each_page_count
    while cur_page * each_page_count <= total:
        s_arg = '[["jjhq",%d,%d,"",0,"hs300"]]' % (cur_page, each_page_count)
        url = base_url % (s_arg, callback_arg)
        doc = myurl.download_url(url)
        soup = BeautifulSoup(doc, 'html.parser')
        text = soup.get_text()
        text = text.split('\n')[1]
        idx = text.find(callback_arg)
        if idx == -1:
            break
        js_str = text[idx+len(callback_arg)+1:-1]
        data = json.loads(js_str)[0]
        items = data['items']
        for stock in items:
            symbol = stock[0]
            codes.append(symbol[2:])

        total = int(data['count'])
        cur_page += 1

    if download:
        with open('./hs300.txt', 'w') as f:
            f.write(json.dumps(codes))

    return codes


def download_stock_data(code, max_year=2):
    return __get_stock_data(code, max_year, download=True)


def get_stock_data(code, max_year=2):
    return __get_stock_data(code, max_year, download=False)


def __get_stock_data(code, max_year=2, download=False):
    df_all = pd.DataFrame()
    base_url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/%s.phtml'
    base_url = base_url % code
    doc = myurl.download_url(base_url)
    soup = BeautifulSoup(doc, 'html.parser')
    hist_date = soup.find('div', attrs={'id': 'con02-4'})
    hist_year = hist_date.find('select', attrs={'name': 'year'})
    years = hist_year.find_all('option')
    if max_year > 0:
        select_years = years[0:max_year]
    else:
        select_years = years
    for y in select_years:
        time.sleep(int(random.random() * 7) + 1)
        df_year = pd.DataFrame()
        year = y.get_text()
        for jidu in (4, 3, 2, 1):
            url = base_url + ('?year=%s&jidu=%d' % (year, jidu))
            doc = myurl.download_url(url)
            soup = BeautifulSoup(doc, 'html.parser')
            table = soup.find('table', attrs={'id': 'FundHoldSharesTable'})
            trs = table.find_all('tr')
            if len(trs) < 2:
                continue

            index = []
            columns = ['open', 'high', 'close', 'low', 'volume']
            detail = []
            for item in trs[2:]:
                tds = item.find_all('td')
                date = tds[0].get_text().strip()
                index.append(date)
                start_idx = 1
                one_line = []
                for i in range(start_idx, start_idx+len(columns)):
                    one_line.append(tds[i].get_text())
                detail.append(one_line)
            df_jidu = pd.DataFrame(detail, columns=columns, index=index)
            df_year = df_year.append(df_jidu)
        df_all = df_all.append(df_year)
    if download:
        df_all.to_csv('./%s' % code)
    return df_all


def main():
    # hs300 = download_hs300_stock_code()
    data = download_stock_data('600000')
    print(data)

if __name__ == '__main__':
    main()
