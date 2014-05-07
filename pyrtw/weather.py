#!/usr/bin/env python
# coding=utf-8

"""
Sync. call to the weather service with the requests module 
"""

import requests
import json

import constants

KEY = constants.KEY
URL = constants.URL

def get_weather(town='haifa', key=KEY):
	url = URL.format(town, key)
	return json.loads(requests.get(url).text)
	


if __name__ == "__main__":
	r = get_weather()
	print r