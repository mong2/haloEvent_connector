#!/usr/bin/python
# -*- coding: utf-8 -*-
import cloudpassage
import multiprocessing
import copy_reg
import types
import datetime
import dateutil.parser
import os
import sys
import time
from functools import partial
from lib.settings import Settings
from lib.utility import Utility


def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)


class Event(object):
    def __init__(self, key_id, secret_key, args=None):
        self.settings = Settings()
        self.utility = Utility(args)
        self.args = args or self.utility.updated_hash()
        self.event_id_exist = True
        self.key_id = key_id
        self.secret_key = secret_key
        self.data_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'data')
        self.config_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'configs', 'configdir')

    def create_halo_session_object(self):
        session = cloudpassage.HaloSession(self.key_id, self.secret_key)
        return session

    def get(self, per_page, date, page):
        session = self.create_halo_session_object()
        api = cloudpassage.HttpHelper(session)
        url = "/v1/events?per_page=%s&page=%s&since=%s" % (per_page,
                                                           page,
                                                           date)
        return api.get(url)

    def latest_event(self, per_page, date, page):
        session = self.create_halo_session_object()
        api = cloudpassage.HttpHelper(session)
        url = "/v1/events?sort_by=created_at.desc&per_page=%s&page=%s&since=%s" % (per_page,
                                                                                   page,
                                                                                   date)
        return api.get(url)

    def batch(self, date):
        batched = []
        p = multiprocessing.Pool(self.settings.threads(), self.utility.init_worker)
        paginations = list(range(1, self.settings.pagination_limit() + 1))
        per_page = str(self.settings.per_page())

        try:
            partial_get = partial(self.get, per_page, date)
            data = p.map(partial_get, paginations)
            for i in data:
                batched.extend(i["events"])
            return batched
        except KeyboardInterrupt:
            print "Caught KeyboardInterrupt, terminating workers"
            # print >> sys.stderr, "Caught KeyboardInterrupt, terminating workers"
            p.terminate()
            p.join()

    def historical_limit_date(self):
        historical_limit = self.settings.historical_limit()
        temp = (datetime.datetime.now() - datetime.timedelta(days=historical_limit))
        date = temp.strftime('%Y-%m-%d')
        return date

    def sort_by(self, data, param):
        sort_data = sorted(data, key=lambda x: x[param])
        return sort_data

    def get_end_date(self, dates, end_date):
        if end_date != self.historical_limit_date:
            return dates[-1]["created_at"]
        return dateutil.parser.parse(dates[-1]["created_at"]).strftime('%Y-%m-%d')

    def id_exists_check(self, data, event_id):
        return any(k['id'] == event_id for k in data)

    def loop_date(self, batched, end_date):
        sorted_data = self.sort_by(batched, "created_at")
        start_date = sorted_data[0]["created_at"]
        end_date = self.get_end_date(sorted_data, end_date)
        return start_date, end_date

    def initial_date(self):
        config_files = os.listdir(self.config_dir)
        if config_files:
            for i in config_files:
                key_id, date = i.split("_")
                if self.key_id == key_id:
                    return self.normalize_date(date)
        return self.args['starting']

    def customize_date(self, date):
        return date.replace(':', '+')

    def normalize_date(self, date):
        return date.replace('+', ':')

    def file_exists_check(self, end_date):
        end_date = self.customize_date(end_date)
        initial_date = self.customize_date(self.initial_date())

        original = os.path.join(self.config_dir, "%s_%s" % (self.key_id, initial_date))
        new = os.path.join(self.config_dir, "%s_%s" % (self.key_id, end_date))

        files = os.listdir(self.config_dir)
        if files:
            self.utility.rename(original, new)
        else:
            f = open(new, 'w')
            f.close()

    def retrieve_events(self):
        end_date = self.initial_date()
        initial_event_id = self.latest_event("1", "", "1")["events"][0]["id"]
        while self.event_id_exist:
            batched = self.batch(end_date)
            start_date, end_date = self.loop_date(batched, end_date)
            self.utility.output_events(batched)
            print "Wrote: %s to %s" % (start_date, end_date)
            self.file_exists_check(end_date)
            if self.id_exists_check(batched, initial_event_id):
                self.event_id_exist = False
