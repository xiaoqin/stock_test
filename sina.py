#!/usr/bin/env python
# -*-coding: utf-8 -*-

from bs4 import BeautifulSoup
import json
import myurl

def get_hs300_stock_code():
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

    return codes


def main():
    hs300 = get_hs300_stock_code()
    with open('./hs300.txt', 'w') as f:
        f.write(json.dumps(hs300))
    print(hs300)

if __name__ == '__main__':
    main()
