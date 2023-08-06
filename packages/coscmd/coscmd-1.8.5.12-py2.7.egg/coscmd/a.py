import requests
header = dict()
header["Host"] = "pinduoduo-gz-1252081001.cos.ap-guangzhou.myqcloud.com"
header["Authorization"] = "q-sign-algorithm=sha1&q-ak=AKIDVosgGZqNzbO1QyfXYKyPbYF1Zswl5t3v&q-sign-time=1539590265;1539600325&q-key-time=1539590265;1539600325&q-header-list=host&q-url-param-list=&q-signature=972340ca7b5aa0104561e704546a0c8049d3d0b5"
requests.get('http://pinduoduo-gz-1252081001.cos.ap-guangzhou.myqcloud.com/?prefix=', headers=header)