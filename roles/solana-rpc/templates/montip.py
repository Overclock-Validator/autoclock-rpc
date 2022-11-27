import urllib.request
import threading
import json
import time

MAINNET = "https://api.mainnet-beta.solana.com"
LOCAL = "http://localhost:8899"
PAYLOAD = {"jsonrpc":"2.0","id":1, "method":"getSlot", "params":[{"commitment":"processed"}]}

def get_slot(req, jsondata, result, idx):
    response = urllib.request.urlopen(req, jsondata)
    res = response.read()
    slotnum = json.loads(res)["result"]
    result[idx] = slotnum


if __name__ == "__main__":
    jsondata = json.dumps(PAYLOAD)
    jsondataasbytes = jsondata.encode('utf-8')
    content_len = len(jsondataasbytes)
    while True:
        tlist = []
        reqlist = []
        resultlist = [0,0]
        for c,u in enumerate([LOCAL, MAINNET]):
            req = urllib.request.Request(u)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            req.add_header('Content-Length', content_len)
            req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')
            reqlist.append((req, jsondataasbytes, resultlist, c))
        for r in reqlist:
            tlist.append(threading.Thread(target = get_slot, args = r))
        for t in tlist:
            t.start()
        for t in tlist:
            t.join()
        print("reference : %s"%(resultlist[1]))
        print("my node   : %s"%(resultlist[0]))
        print("slots behind reference : %s"%(resultlist[1] - resultlist[0]))
        print("=====\n")
        time.sleep(10)
