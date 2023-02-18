import requests

def sendPlusPlus(token: str, title: str, content: str):
    url = f'http://www.pushplus.plus/send?token={token}&title={title}&content={content}'
    requests.get(url=url)
    
def sendServerChan(sckey: str, title: str, content: str):
    url = f'https://sc.ftqq.com/{sckey}.send?text={title}&desp={content}'
    requests.get(url=url)