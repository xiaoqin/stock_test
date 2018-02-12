#!/usr/bin/env python
# -*- coding=utf-8 -*-

from urllib import request
import ssl


def download_url(url, debug=True):
    '''获取url地址页面内容'''
    if debug:
        print('downloading', url)

    data = ''
    req = request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36')
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    with request.urlopen(req, context=gcontext) as f:
        data = f.read()
    return data


def main():
    url = 'http://stock.qq.com/data/#qgqp'
    doc = download_url(url)
    print(doc)

if __name__ == '__main__':
    main()
