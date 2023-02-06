import ddddocr
import requests
import re

ocr = ddddocr.DdddOcr()

# for i in range(100):
#     res = requests.get("https://api.moguding.net:9000/session/user/v1/captcha.jpg?uuid=7ede1a5d-92b8-4a15-8459-7c0364c200ee")
#     img_bytes = res.content
#     yzm = ocr.classification(img_bytes)
#     yzm = re.sub(r'[\u4e00-\u9fa5]|-', '', yzm)
#     with open(f'yzm/{yzm}.png', 'wb') as f:
#         f.write(res.content)

#     print(yzm)

from app.common.gxyUtils import sign

sign('104609356','123456')