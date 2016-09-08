import datetime
import sys
import os
import json
import signal
from lib.options import Options
from lib.settings import Settings
from lib.jsonkv import JsonKv
from lib.leef import Leef
from lib.cef import Cef
from lib.rsyslog import Rsyslog
import lib.validate as validate

class Utility(object):
    def __init__(self, options = None):
        self.settings = Settings()
        self.options = options or Options()
        self.rsyslog = Rsyslog()
        self.jsonkv = JsonKv()
        self.leef = Leef(options)
        self.cef = Cef(options)

    def rename(self, a, b):
        os.rename(a, b)

    def interruptHandler(self, signum, frame):
        print "Beginning shutdown..."

    def init_worker(self):
        signal.signal(signal.SIGINT, self.interruptHandler)

    def write_output(self, filename, formatted_events):
        with open(filename, 'a') as f:
            for formatted_event in formatted_events:
                f.write(str(formatted_event))
        f.close()

    def output_events(self, batched):
        if self.options["ceffile"] is not None:
            self.write_output(self.options["ceffile"], self.cef.format_cef(batched))
        if self.options["jsonfile"] is not None:
            self.write_output(self.options["jsonfile"], self.jsonkv.format_json(batched))
        elif self.options["kvfile"] is not None:
            self.write_output(self.options["kvfile"], self.jsonkv.format_kv(batched))
        elif self.options['leeffile'] is not None:
            self.write_output(self.options["leeffile"], self.leef.format_leef(batched))
        elif self.options["cef"]:
            for formatted_event in self.cef.format_cef(batched):
                print formatted_event
        elif self.options["kv"]:
            for formatted_event in self.jsonkv.format_kv(batched):
                print formatted_event
        elif self.options["cefsyslog"]:
            self.rsyslog.process_openlog(self.options["facility"])
            self.rsyslog.process_syslog(self.cef.format_cef(batched))
            self.rsyslog.closelog()
        elif self.options["leefsyslog"]:
            self.rsyslog.process_openlog(self.options["facility"])
            self.rsyslog.process_syslog(self.leef.format_leef(batched))
            self.rsyslog.closelog()
        elif self.options["kvsyslog"]:
            self.rsyslog.process_openlog(self.options["facility"])
            self.rsyslog.process_syslog(self.jsonkv.format_kv(batched))
            self.rsyslog.closelog()
        else:
            pass

    def parse_auth(self):
        auth_keys = []
        with open(self.options['auth'], 'r') as f:
            auth_file = map(str.rstrip, f)
        for line in auth_file:
            key, secret = line.split("|")
            auth_keys.append({"key_id": key, "secret_key": secret})
        return auth_keys

    def parse_pagination_limit(self):
        if self.options['batchsize'] is None:
            return self.settings.pagination_limit()
        validate.batchsize(self.options['batchsize'])
        return int(self.options['batchsize'])

    def parse_threads(self):
        if self.options['threads'] is None:
            return self.settings.threads()
        validate.thread(self.options["threads"])
        return self.options['threads']

    def check_starting(self):
        if self.options["starting"] and self.options["configdir"] is None:
            validate.starting(self.options["starting"])
            return None
        elif self.options["starting"] is None and self.options["configdir"]:
            return self.parse_configdir()
        else:
            raise ValueError("Please choose either --starting or --configdir")

    def parse_configdir(self):
        key_date = []
        files = os.listdir(self.options["configdir"])
        if files:
            for f in files:
                key, end_date = f.split("_")
                validate.starting(end_date)
                key_date.append({"key_id": key, "end_date": end_date})
        else:
            raise ValueError("Please use --starting to specify a starting date")
        return key_date

    def updated_hash(self):
        self.options["api_keys"] = self.parse_auth()
        self.options["batchsize"] = self.parse_pagination_limit()
        self.options["threads"] = self.parse_threads()
        self.options["configfiles"] = self.check_starting()
        return self.options
