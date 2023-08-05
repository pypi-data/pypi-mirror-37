# /usr/bin/env python
# -*- coding:utf-8 -*-



class Result(Exception):

    def __init__(self, data):
        self.result = data
