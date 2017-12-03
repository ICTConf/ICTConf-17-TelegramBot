# -*- coding: UTF-8 -*-

import json

import datetime
import requests

url = "http://127.0.0.1:8000/api/event/?format=json"

params = dict()
text = "/Yes utkucan bıyıklı".replace("/Yes", "").split(" ")
print(text[1]+ " " + text[2])

