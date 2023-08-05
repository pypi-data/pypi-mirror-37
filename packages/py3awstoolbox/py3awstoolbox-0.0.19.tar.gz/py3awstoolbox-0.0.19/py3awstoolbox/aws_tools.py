import os
import sys
import time
import boto3
from botocore.client import Config
import py3toolbox     as tb

class S3():
  def __init__(self, bucket_name):
    self.s3_config    = Config(connect_timeout=5, retries={'max_attempts': 100})
    self.s3           = boto3.resource('s3')
    self.s3client     = boto3.client('s3', config=self.s3_config)
    self.bucket_name  = bucket_name
    self.bucket       = self.s3.Bucket(self.bucket_name)
    
  def get_subfolders(self, prefix='') :
    kwargs = {'Bucket': self.bucket_name , 'Delimiter' : '/' } 
    if isinstance(prefix, str): kwargs['Prefix'] = prefix 
   
    while True:
      resp = self.s3client.list_objects_v2(**kwargs)
      try:
        if len(resp['CommonPrefixes'])>0 :
          for f in resp['CommonPrefixes']:
            yield ( f['Prefix'])
      except KeyError:
        try:
          kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
          break     
        continue
      try:
        kwargs['ContinuationToken'] = resp['NextContinuationToken']
      except KeyError:
        break   
   
  def get_objects(self, prefix='', suffix='', recursive=True):
    if recursive :
      kwargs = {'Bucket': self.bucket_name}
    else:
      kwargs = {'Bucket': self.bucket_name, 'Delimiter' : '/' }
      
    if isinstance(prefix, str): kwargs['Prefix'] = prefix
    
    while True:
      resp = self.s3client.list_objects_v2(**kwargs)
      try:
        contents = resp['Contents']
      except KeyError:
        try:
          kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
          break      
        continue

      for obj in contents:
        key = obj['Key']
        if key.endswith(suffix): yield obj

      try:
        kwargs['ContinuationToken'] = resp['NextContinuationToken']
      except KeyError:
        break

  def get_keys(self, prefix='', suffix='', recursive=True):
    for obj in self.get_objects( prefix=prefix, suffix=suffix, recursive=recursive):
      yield obj['Key']

  def download_file(self, s3file, local_file):
    objs = self.get_objects(prefix=s3file)
    self.bucket.download_file(s3file, local_file)
      
  def upload_file(self, s3file,local_file) :
    self.s3.meta.client.upload_file(local_file, self.bucket_name , s3file)
  
class Logs():
  def __init__(self):
    self.aws_log_client = boto3.client('logs')
    self.start_time = int(time.time())*1000
    
    pass
  
  def get_logs(self,log_group, start_time=None, end_time=None ):
    kwargs = {
        'logGroupName': log_group,
        'limit': 10000,
    }
    
    if start_time is not None:
      kwargs['startTime'] = start_time
    if end_time is not None:
      kwargs['endTime'] =  end_time

    while True:
      resp = self.aws_log_client.filter_log_events(**kwargs)
      yield from resp['events']
      try:
        kwargs['nextToken'] = resp['nextToken']
      except KeyError:
        break

  def get_requestid(self, log_text):
    requestid = None
    # [RequestId:               55010d25-95c8-11e8-9b14-8519fb68a71b]
    # [2018-08-01T20:20:18.292Z	4ecc273d-95c8-11e8-9f8a-35299c41545c]
    m = tb.re_search(re_pattern='^(RequestId\:|\d+\-\d+\-\d+T\d+\:\d+\:\d+\.\d+Z)\s+(\w{8}\-\w{4}\-\w{4}\-\w{4}\-\w{12})\s+', text=log_text)
    if m is not None:
      requestid = m(1)[1]
    return (requestid)


  def filter_logs(self, log_group, key_word=None, last_mins=None, start_time=None, next_mins=None, end_time=None,):
    logs_requestid_found = []
    logs_unfilterd = []
    logs_filtered  = {}
    requestid = None
    
    # check keyword
    if key_word is not None and len(key_word.strip()) <1 :
      key_word = None
    
    # set start time
    if last_mins is not None:
      self.start_time = int(time.time())*1000 - last_mins * 60 * 1000 
    else:
      self.start_time = start_time
    
    # set end time  
    if next_mins is not None:
      self.end_time   = self.start_time + next_mins * 60 * 1000 
    else:
      self.end_time   = end_time

    # go through logs
    log_events = self.get_logs(log_group=log_group,start_time= self.start_time, end_time = self.end_time)
    for log_event in log_events: 
      message = log_event['message']
      if len(message.strip()) <1 : continue
      logs_unfilterd.append(message)
      
      # filter by keyword
      if key_word is None or key_word in message :
        requestid = self.get_requestid(log_text = message)
        if requestid is None: continue
        logs_requestid_found.append(requestid)

        
    logs_requestid_found = list(set(logs_requestid_found))
    # filter by request id
    for requestid in logs_requestid_found:
      for log in logs_unfilterd:
        if requestid in log:
          if requestid not in logs_filtered: 
            logs_filtered [requestid] = []
          logs_filtered [requestid].append(log)
    return logs_filtered
    
if __name__ == "__main__":
  #aws_log = Logs()
  #logs_found = aws_log.filter_logs(log_group='/aws/lambda/tafe-search-sit-tafe', key_word= None , last_mins=15)
  #logs_found = aws_log.filter_logs(log_group='/aws/lambda/tafe-search-sit-tafe', key_word= 'screen and media' , last_mins=30)
  #total =  (len(list(logs_found.keys())))
  #success = 0
  #for requestid in logs_found.keys() :
  #  if "[200] - Success." in  ''.join(logs_found[requestid]):
  #    success +=1
  #print (success, total)
  
  mys3 = S3('testpublic111') 
  mys3.upload_file('test.txt','/temp/1.json')
  
  
  pass  
