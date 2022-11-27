import urllib.request
import threading
import json
import time

LOCAL = "http://localhost:8899"
PAYLOAD = {"jsonrpc":"2.0","id":1,"method":"getHighestSnapshotSlot"} 

def get_snap_slot(req, jsondata):
    response = urllib.request.urlopen(req, jsondata)
    res = response.read()
    slotnum = json.loads(res)["result"]["incremental"]
    return slotnum

if __name__ == "__main__":
    jsondata = json.dumps(PAYLOAD)
    jsondataasbytes = jsondata.encode('utf-8')
    content_len = len(jsondataasbytes)
    latest_snap = None
    while True:
        req = urllib.request.Request(LOCAL)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        req.add_header('Content-Length', content_len)
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')
        if latest_snap is None:
            latest_snap = get_snap_slot(req,jsondataasbytes)
            print("current incr snapshot slot: %s\nsleeping..."%(latest_snap))
            stime = int(time.time())
            time.sleep(1)
        latest_incr = get_snap_slot(req,jsondataasbytes)
        if latest_incr == latest_snap:
            time.sleep(1)
        else:
            etime = int(time.time()) - stime
            break
print("latest incr snapshot slot: %s\nslept: %s seconds"%(latest_incr,etime))
