#!/usr/bin/env python
# -*-coding: utf-8 -*-

from bs4 import BeautifulSoup
import json

import myurl

def get_all_stock_code():
    codes = {}
    base_url = 'http://stock.finance.qq.com/sstock/view/show.php?t=qgqp&c=search_by_type&p=%d&type=%d'
    stock_types = {'sh': 1, 'sz': 2, 'zxb': 3, 'cyb': 4}
    for k in stock_types.keys():
        codes[k] = []
        v = stock_types[k]
        cur_page = 1
        total_page = 1
        while cur_page <= total_page:
            url = base_url % (cur_page, v)
            doc = myurl.download_url(url)
            soup = BeautifulSoup(doc, 'html.parser')
            js_str = soup.get_text()
            index = js_str.find('{')
            if index == -1:
                break
            ret = json.loads(js_str[index:])
            data = ret['data']
            total_page = int(data['totalPage'])
            cur_page = int(data['curPage']) + 1
            result = data['result']
            for stock in result:
                codes[k].append(stock['ZQDM'])

    with open('./all_code.txt', 'w') as f:
        f.write(json.dumps(codes))

    return codes


def main():
    codes = get_all_stock_code()
    print(codes)

if __name__ == '__main__':
    main()
