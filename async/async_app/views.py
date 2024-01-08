import json
import time
import random
import requests
from concurrent import futures
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

executor = futures.ThreadPoolExecutor(max_workers=1)
ServerToken = "rjbrbjwf4908h8nfieh"
url = "http://127.0.0.1:8080/api/event/finish-scanning"

def do_scanning(req_body):
    scanned_percent = random.randint(1, 100)
    time.sleep(5)
    req_body['scanned_percent'] = scanned_percent
    req_body['Token'] = ServerToken
    return req_body

def status_callback(task):
    try:
      result = task.result()
      print(result)
    except futures._base.CancelledError:
      return
    requests.put(url, data=json.dumps(result), timeout=3)

@api_view(['Put'])
def scan(request):
    req_body = json.loads(request.body)
    task = executor.submit(do_scanning, req_body)
    task.add_done_callback(status_callback)        
    return Response(status=status.HTTP_200_OK)
