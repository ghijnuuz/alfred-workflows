#/usr/bin/env python
#coding=utf8

import sys
import os
import hashlib
import random
from workflow import Workflow3
from workflow import web

def translate(q):
    appKey = os.getenv('app_key', '').strip()
    secretKey = os.getenv('secret_key', '').strip()
    fromLang = 'auto'
    toLang = 'auto'
    salt = random.randint(1, 65536)

    signStr = appKey + q.encode('utf8') + str(salt) + secretKey
    m = hashlib.md5()
    m.update(signStr)
    sign = m.hexdigest()

    param = {'q':q, 'from':fromLang, 'to':toLang, 'appKey':appKey, 'salt':salt, 'sign':sign}
    return web.get('http://openapi.youdao.com/api', param).json()

def main(wf):
    args = wf.args
    q = args[0]

    data = translate(q)

    translationData = data.get('translation')
    if translationData is not None:
        result = translationData[0]
        wf.add_item(title=result, subtitle=u'翻译结果', arg=result, copytext=True, valid=True)
    basicData = data.get('basic')
    if basicData is not None:
        explains = basicData.get('explains')
        for explain in explains:
            wf.add_item(title=explain, subtitle=u'简明释义', arg=explain, copytext=True, valid=True)
    webData = data.get('web')
    if webData is not None:
        for webDict in webData:
            valueList = webDict.get('value')
            for value in valueList:
                title = value
                subtitle = u'网络释义: ' + webDict.get('key')
                wf.add_item(title=title, subtitle=subtitle, arg=title, copytext=True, valid=True)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
