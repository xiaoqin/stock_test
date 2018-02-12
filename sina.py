#!/usr/bin/env python
# -*-coding: utf-8 -*-

from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import random
import json
import myurl
import config

default_start = '2017-12-10'
default_end = time.strftime("%Y-%m-%d", time.localtime())
data_dir = config.data_dir
stock_url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/%s.phtml'

def get_year_and_jidu(date):
    (year, month, day) = date.split('-')
    jidu = (int(month) + 2) // 3
    return (int(year), jidu)


def get_hs300_stock_code(download=False):
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
            print('download error:', url)
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
        with open(os.path.join(data_dir, 'hs300.txt'), 'w') as f:
            f.write(json.dumps(codes))

    return codes


def get_stock_data(code, start=default_start, end=default_end, download=False):
    (start_year, start_jidu) = get_year_and_jidu(start)
    (end_year, end_jidu) = get_year_and_jidu(end)
    start_time = time.strptime(start, '%Y-%m-%d')
    end_time = time.strptime(end, '%Y-%m-%d')

    df_all = pd.DataFrame()
    for year in range(end_year, start_year-1, -1):
        time.sleep(int(random.random() * 7) + 1)
        df_year = pd.DataFrame()
        for jidu in (4, 3, 2, 1):
            if year == end_year and jidu > end_jidu:
                continue
            if year == start_year and jidu < start_jidu:
                continue
            url = (stock_url % code) + ('?year=%d&jidu=%d' % (year, jidu))
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
                localtime = time.strptime(date, '%Y-%m-%d')
                if localtime > end_time or localtime < start_time:
                    continue
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
        df_all.to_csv(os.path.join(data_dir, code))

    return df_all


def main():
    hs300 = get_hs300_stock_code()
    if hs300:
        data = get_stock_data(hs300[0])
        print(data)

if __name__ == '__main__':
    main()
