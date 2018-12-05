#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib3
import json

esUrl = "es_url:9200"

def es(cmd):
    try:
        header = { 'Content-Type': 'application/json' }
        data = {}
        if cmd[1] == "i":
            rtn = es_rtn('GET', esUrl, data, header)
        elif cmd[1] == "h":
            rtn = es_rtn('GET', esUrl + "/_cat/health?v", data, header)
        elif cmd[1] == "d":
            rtn = es_rtn('GET', esUrl + "/_cat/allocation?v", data, header)
        elif cmd[1] == "re":
            data = { "transient" : { "cluster.routing.allocation.enable" : "all" } }
            rtn = es_rtn('PUT', esUrl + "/_cluster/settings", data, header)
        elif cmd[1] == "rd":
            data = { "transient" : { "cluster.routing.allocation.enable" : "none" } }
            rtn = es_rtn('PUT', esUrl + "/_cluster/settings", data, header)
        else:
            print "incorrect commands"
            rtn = "incorrect commands"
    except IndexError:
        print "no args"
        rtn = "no args"

    return rtn

def es_rtn(method, cmd, data=None, header=None):
    http = urllib3.PoolManager()

    try:
        rtn = http.request(method,cmd,body=json.dumps(data),headers=header)
    except urllib3.exceptions.HTTPError as errh:
        print ("Http Error:",errh)

    print rtn.data
    return rtn.data

if __name__ == '__main__':
    es(sys.argv)
