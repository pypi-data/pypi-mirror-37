# -*- coding: utf-8 -*-

import datetime
import json

def isDate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def printp(data):
	print json.dumps(data, indent=2, sort_keys=True)