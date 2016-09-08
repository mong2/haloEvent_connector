#!/usr/bin/python
# -*- coding: utf-8 -*-
from lib import *
utility = Utility()
args = utility.updated_hash()


def main():
    for i in args["api_keys"]:
        event = Event(i['key_id'], i['secret_key'])
        event.retrieve_events()


if __name__ == "__main__":
    main()
