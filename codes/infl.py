#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urllib3
import json
from datetime import datetime
from influxdb import InfluxDBClient

influxUrl = "es01" # url where influxdb installed on
esUrl = "es01" # url wehre es installed on


# -----------------------------------------------------------------
# function to connect to influxdb
# -----------------------------------------------------------------
def get_ifdb(db, host=influxUrl, port=8086, user='root', passwd='root'):
    client = InfluxDBClient(host, port, user, passwd, db)
    try:
        client.create_database(db)
    except:
        pass
    return client


# -----------------------------------------------------------------
# function to load data by time-series on influxdb
# -----------------------------------------------------------------
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
            "pri_doc": statVal[0], # primary document
            "tot_doc": statVal[1], # total document
            "pri_idx_tot": statVal[2], # primary index total
            "pri_idx_mil": statVal[3], # primary index milliseconds
            "tot_idx_tot": statVal[4], # total index total
            "tot_idx_mil": statVal[5] # total index milliseconds
        }
    }]

    ifdb.write_points(point)


# -----------------------------------------------------------------
# function to extract data from a cluster for monitoring
#   call the function 'my_test'
# -----------------------------------------------------------------
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


# -----------------------------------------------------------------
# main function
#   for running by module and main
#   for connecting to influxdb then, write data on db based on the connection info
# -----------------------------------------------------------------
if __name__ == '__main__':
    ifdb = get_ifdb(db='mdb')  # change to the db name being created
    my_test(ifdb)
