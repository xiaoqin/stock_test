#!/usr/bin/env python
# -*-coding: utf-8 -*-

import ssl
from urllib import request
from bs4 import BeautifulSoup


def download_url(url):
    data = ''
    req = request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Mcintosh; Intel Mac OS X)')
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    with request.urlopen(req, context=gcontext) as f:
        data = f.read()
    return data


def main():
    pass

if __name__ == '__main__':
    main()
