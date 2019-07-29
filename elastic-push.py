from elasticsearch import Elasticsearch
from argparse import ArgumentParser
import json

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename", help="write report to FILE", metavar="FILE")
parser.add_argument("-s", "--server", dest="server", help="server name or IP of elastic search")

args = parser.parse_args()

f = open(args.filename,"r")
item = f.read()

# get the number of jobs that ran
json_data = json.loads(item)
count = len(json_data['jobs'])

# extract the job details we want to send with every job
timestamp = json_data['timestamp']
time = json_data['time']
fio_version = json_data['fio version']

# setup the elasticsearch connection
es = Elasticsearch(
  [args.server],
  use_ssl=True,
  verify_certs=True,
  ca_certs='/elasticsearch/ca',
  client_cert='/elasticsearch/cert',
  client_key='/elasticsearch/key'
  )

# add the job and disk_util details to each job before we send it
for i in range(count):
  push_data = json_data['jobs'][i]
  push_data['timestamp'] = timestamp
  push_data['fio_version'] = fio_version
  push_data['time'] = time
  push_data['disk_util'] = json_data['disk_util'][i]
  #print push_data
  res = es.index(index="fio-output", doc_type='fio-3', body=push_data)


#debug
#print count
#print args.server
#print item
#print timestamp
#print fio_version
