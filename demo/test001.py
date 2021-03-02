# -*- coding: utf-8 -*-
import pystache,yaml,pprint,jmespath,json,requests
from string import Template
from common.base_api import BaseAPI
# b = BaseAPI()
r = requests.get(r'http://localhost:9999/xintian_sq01')
print(r.text)
# print(r.json())
a = "{'a':1,'b':2}"
j = jmespath.search('a',r.text)
print(j)