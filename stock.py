#!/usr/bin/env python
# -*-coding: utf-8 -*-

import tencent
import sina
import time


def main():
    # tencent.get_all_stock_code()
    hs300 = sina.get_hs300_stock_code()
    for code in hs300:
        sina.get_stock_data(code)
        time.sleep(30)

if __name__ == '__main__':
    main()
