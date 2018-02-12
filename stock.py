#!/usr/bin/env python
# -*-coding: utf-8 -*-

import tencent
import sina


def main():
    tencent.download_all_stock_code()
    # sina.download_hs300_code()

if __name__ == '__main__':
    main()
