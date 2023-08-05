# -*- coding: utf-8 -*-

from .urlfetcher import URLFetcher

def get_html(URL):
    return URLFetcher().fetch_url(URL)

