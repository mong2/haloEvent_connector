#!/usr/bin/python
# -*- coding: utf-8 -*-
import dateutil.parser
import datetime
import pytz
import platform
from lib.settings import Settings

settings = Settings()


def validate_time(date):
    try:
        dateutil.parser.parse(date)
    except:
        raise ValueError(date + "is not in iso8601 time format")

def validate_time_range(date):
    date_parsed = dateutil.parser.parse(date)
    if date_parsed.tzinfo is None:
        date_parsed = pytz.utc.localize(date_parsed)
    time_range = (datetime.datetime.utcnow().replace(tzinfo=pytz.utc) - datetime.timedelta(days=settings.historical_limit()))
    if date_parsed < time_range:
        raise ValueError(date + " is out of range")

def batchsize(page):
    try:
        int(page)
    except:
        raise ValueError(page + " is not an integer")
    if int(page) > settings.pagination_limit():
        raise ValueError("you have exceeded the batchsize limitation")

def thread(thread):
    try:
        int(thread)
    except:
        raise ValueError(thread + "is not an integer")
    if int(thread) > settings.threads():
        raise ValueError("you have exceeded the thread limitation")

def starting(date):
   validate_time(date)
   validate_time_range(date)

def operating_system():
    if platform.system() is 'Windows':
        return "windows"
    return "linux"
