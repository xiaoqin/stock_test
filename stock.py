#!/usr/bin/env python
# -*-coding: utf-8 -*-

from bs4 import BeautifulSoup
import myurl


def main():
    url = 'http://stock.qq.com/data/#qgqp'
    doc = myurl.download_url(url)
    print(doc)

if __name__ == '__main__':
    main()
