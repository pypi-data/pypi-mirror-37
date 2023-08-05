# -*- coding: utf-8 -*-

from .urlfetcher import *

def get_html(URL):
    return URLFetcher().fetch_url(URL)

