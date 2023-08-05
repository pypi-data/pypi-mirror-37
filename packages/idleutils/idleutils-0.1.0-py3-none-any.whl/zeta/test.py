#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from urlfetcher import URLFetcher
from .. zeta import get_html

if __name__ == '__main__':
    html = get_html('http://www.bidding.csg.cn/zbgg/index.jhtml')
    print(html)
    #dic = {
        #'url': 'http://www.bidding.csg.cn/zbgg/index.jhtml', 'name': 'name', 'ajax': {
            #'curl': '',
            #'method': 'get',
        #},
        #'selecter': {
            #'type': 'selecter',
            #'struct': 'selecterValue'
        #},
        #'detailpage': {
            #'detailpage': 'firstPageDetailPage',
            #'param': 'firstRecordUrl',
        #}
    #}

    # URLFetcher().simulate_url_prams(dic)
    # html = URLFetcher().fetch_curl(
    #     "curl 'https://ss0.bdstatic.com/k4oZeXSm1A5BphGlnYG/newmusic/lovesong.png' -H 'Referer: https://www.baidu.com/' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36' --compressed")
    #html = URLFetcher().fetch_url('http://www.bidding.csg.cn/zbgg/index.jhtml')
    #print(html)
    #engine, lst, msg = URLFetcher().get_page_list(html)

    # engine, lst, msg = URLFetcher().simulate_url_prams(dic)
    # for item in lst:
    #     print item['title']
    # print msg
    # webgather_table("xx")
