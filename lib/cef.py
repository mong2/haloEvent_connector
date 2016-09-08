#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from options import Options
import lib.loadyaml as loadyaml


class Cef(object):
    def __init__(self, options = None):
        self.options = options or Options()
        self.c = loadyaml.load_cef()

    def cef_constants(self, event):
        severity = 9 if event["critical"] else 3
        return "CEF:%s|%s|%s|%s|%s|%s|%s|" % (self.c["cefVersion"],
                                              self.c["cefVendor"],
                                              self.c["cefProduct"],
                                              self.c["cefProductVersion"],
                                              self.c["eventIdMap"][event["type"]],
                                              event["name"],
                                              severity)

    def build_cef_outliers(self, mapping, event):
        mapping['deviceDirection'] = 1 if 'actor_username' in event else 0

    def build_cef_mapping(self, event):
        mapping = {}
        self.build_cef_outliers(mapping, event)
        for k, v in self.c['cefFieldMapping'].items():
            if k in event:
                mapping[v] = event[k]
                del event[k]
        if event:
            mapping["cs1label"] = "extras"
            mapping["cs1"] = event
        return mapping

    def format_cef(self, batched):
        aggregated_cef = []
        for event in batched:
            cef_str = ""
            constants_map = self.cef_constants(event)
            schema = self.build_cef_mapping(event)
            for k, v in schema.items():
                cef_str += "%s=%s " % (k, v)
            aggregated_cef.append("%s%s" % (constants_map, cef_str))
        return aggregated_cef
