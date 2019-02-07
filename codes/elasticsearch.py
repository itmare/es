#!/usr/bin/env python

import sys
import urllib3
import json


# example
# python elasticsearch.py <OPTION_INITIAL> <ES_URL:PORT>


# -----------------------------------------------------------------
# 사용자의 command를 해석, 액션 분기와 data, header를 추가로 정의하는 function
# -----------------------------------------------------------------
def es(cmd):
    try:
        header = { 'Content-Type': 'application/json' }
        data = {}
        # api 추가
        if cmd[1] == "i":
            es_rtn('GET', cmd[2], data, header)
        elif cmd[1] == "n":
            es_rtn('GET', cmd[2] + "/_cat/nodes?v", data, header)
        elif cmd[1] == "h":
            es_rtn('GET', cmd[2] + "/_cat/health?v", data, header)
        elif cmd[1] == "d":
            es_rtn('GET', cmd[2] + "/_cat/allocation?v", data, header)
        elif cmd[1] == "s":
            es_rtn('GET', cmd[2] + "/_cat/shards?v", data, header)
        elif cmd[1] == "rd":
            data = { "transient" : { "cluster.routing.allocation.enable" : "none" } }
            es_rtn('PUT', cmd[2] + "/_cluster/settings", data, header)
        elif cmd[1] == "re":
            data = { "transient" : { "cluster.routing.allocation.enable" : "all" } }
            es_rtn('PUT', cmd[2] + "/_cluster/settings", data, header)
        else:
            print "incorrect commands"
    except IndexError:
        print "no args"


# -----------------------------------------------------------------
# es(cmd)에서 분기된 액션을 restAPI로 request를 던지는 function
# -----------------------------------------------------------------
def es_rtn(method, cmd, data=None, header=None):
    http = urllib3.PoolManager()

    try:
        rtn = http.request(method,cmd,body=json.dumps(data),headers=header)
    except urllib3.exceptions.HTTPError as errh:
        print ("Http Error:",errh)

    print rtn.data


# -----------------------------------------------------------------
# main function
#   모듈로 쓰일때와 메인으로 쓰일때 둘다 동작하도록 정의
#   sys.argv를 통해 사용자가 입력한 parameter를 list로 받음
# -----------------------------------------------------------------
if __name__ == '__main__':
    es(sys.argv)