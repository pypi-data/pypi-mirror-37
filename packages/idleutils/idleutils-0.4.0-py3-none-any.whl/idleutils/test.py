#!/usr/bin/env python
# -*- coding: utf-8 -*-

from idleutils import get_html

if __name__ == '__main__':
    html = get_html('http://www.bidding.csg.cn/zbgg/index.jhtml')
    print(html)
