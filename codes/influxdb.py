#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib3
import json
from datetime import datetime
from influxdb import InfluxDBClient

influxUrl = "ec2-3-16-8-131.us-east-2.compute.amazonaws.com" # influxdb가 설치된 url주소
esUrl = "ec2-3-16-8-131.us-east-2.compute.amazonaws.com" # es가 설치된 url주소

def get_ifdb(db, host=influxUrl, port=8086, user='root', passwd='root'):
	client = InfluxDBClient(host, port, user, passwd, db)
	try:
		client.create_database(db)
	except:
		pass
	return client

def my_test(ifdb):
        local_dt = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        statVal = es_mon()
	point = [{
		"measurement": 'docs',
                "tags": {
                        "type": "ec2",
                },
		"time": local_dt,
		"fields": {
                    "pri_doc": statVal[0],
                    "tot_doc": statVal[1],
                    "pri_idx_tot": statVal[2],
                    "pri_idx_mil": statVal[3],
                    "tot_idx_tot": statVal[4],
                    "tot_idx_mil": statVal[5]
		}
	}]

	ifdb.write_points(point)

def es_mon():
    http = urllib3.PoolManager()
    header = { 'Content-Type': 'application/json' }
    monCmd = esUrl + ":9200/_stats"

    try:
        rtn = http.request("GET",monCmd,body=json.dumps(None),headers=header)
    except urllib3.exceptions.HTTPError as errh:
        print ("Http Error:",errh)

    monData = json.loads(rtn.data)
    rtnVal = []
    rtnVal.append(monData['_all']['primaries']['docs']['count'])
    rtnVal.append(monData['_all']['total']['docs']['count'])
    rtnVal.append(monData['_all']['primaries']['indexing']['index_total'])
    rtnVal.append(monData['_all']['primaries']['indexing']['index_time_in_millis'])
    rtnVal.append(monData['_all']['total']['indexing']['index_total'])
    rtnVal.append(monData['_all']['total']['indexing']['index_time_in_millis'])

    return rtnVal

if __name__ == '__main__':
    ifdb = get_ifdb(db='mmdb')  # 생성한 influxdb로 변경
    my_test(ifdb)
