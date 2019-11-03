# -*- coding: UTF-8 -*-

import json

import datetime
import requests

url = "http://ictconf.net/api/event/?format=json"

params = dict()
text = "/Yes utkucan bıyıklı".replace("/Yes", "").split(" ")
print(text[1]+ " " + text[2])

