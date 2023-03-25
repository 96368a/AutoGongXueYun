import sys,os
sys.stdout = open(os.devnull, 'w')

import ddddocr
import requests
import re
ocr = ddddocr.DdddOcr()

sys.stdout = sys.__stdout__
def getCode(uuid):
    res = requests.get(f'https://api.moguding.net:9000/session/user/v1/captcha.jpg?uuid={uuid}')
    img_bytes = res.content
    code = ocr.classification(img_bytes)
    code = re.sub(r'[\u4e00-\u9fa5]|-', '', code)
    return code