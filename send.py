import requests
import base64
import pickle
import json

def handler(event, context): 
    if event['path'].find("send")!=-1:
        data = base64.b64decode(event['body'])
        data = pickle.loads(data)
        event['data'] = data
        if data['method'] == "GET":
            print(data)
            res = requests.get(data['url'],headers=data['headers'])
            return res.content
        elif data['method'] == "POST":
            res = requests.post(data['url'],headers=data['headers'],data=json.dumps(data['data']))
            try:
                return res.json()
            except:
                return res.text
        # return '{"msg":"方法不正确"}'
        return event
    else:
        flag = False
        try:
            res = requests.post("https://api.moguding.net:9000/practice/plan/v3/getPlanByStu",timeout=3)
            flag = True
        except:
            pass
        res = requests.get("https://4.ipw.cn",timeout=3)
        return res.text + str(flag)