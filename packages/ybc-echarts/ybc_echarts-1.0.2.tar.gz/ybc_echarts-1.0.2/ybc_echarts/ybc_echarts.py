# coding=utf-8
from pyecharts import Geo as GetGeo

class Geo(GetGeo):
    def __init__(self, title="", subtitle="", **kwargs):
        super().__init__(title, subtitle, **kwargs)

    def add(self, *args, **kwargs):
        self.__add('',*args, **kwargs)