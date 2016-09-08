#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from options import Options
import lib.loadyaml as loadyaml


class Leef(object):
    def __init__(self, options = None):
        self.options = options or Options()
        self.c = loadyaml.load_leef()

    def constants(self, event):
        return "LEEF:%s|%s|%s|%s|%s|" % (self.c['leefFormatVersion'],
                                         self.c['leefVendor'],
                                         self.c['leefProduct'],
                                         self.c['leefProductVersion'],
                                         event['name'])

    def event_category(self, event):
        for key, value in self.c['leefCategoriesByName'].items():
            if event['type'] in value:
                return key

    def build_leef_outliers(self, mapping, event):
        category = self.event_category(event)
        mapping['cat'] = category if category else "unknown"
        mapping['leefDateFormat'] = self.c['leefDateFormat']
        mapping['sev'] = 9 if event['critical'] else 3
        mapping['isLoginEvent'] = True if event['type'] in self.c['leefLoginEventNames'] else False
        mapping['isLogoutEvent'] = True if event['type'] in self.c['leefLogoutEventNames'] else False

    def build_leef_mapping(self, event):
        mapping = {}
        self.build_leef_outliers(mapping, event)
        for k, v in self.c['leefFieldMapping'].items():
            if k in event:
                mapping[v] = event[k]
                del event[k]
        if event:
            for ek, ev in event.items():
                mapping[ek] = ev
        return mapping

    def format_leef(self, batched):
        aggregated_leef = []
        for event in batched:
            leef_str = ""
            constants_map = self.constants(event)
            schema = self.build_leef_mapping(event)
            for k, v in schema.items():
                leef_str += "%s=%s     " % (k, v)
            aggregated_leef.append("%s%s" % (constants_map, leef_str))
        return aggregated_leef
