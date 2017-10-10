#/usr/bin/env python
#coding=utf8
# YoudaoTranslation.py

import sys
import hashlib
import random
from workflow import Workflow3
from workflow import web

# 请到有道智云网站http://ai.youdao.com/gw.s申请API Key
APP_KEY = '***'
SECRET_KEY = '***'

def translate(appKey, secretKey, q):
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

    data = translate(APP_KEY, SECRET_KEY, q)

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
            title = u''
            valueList = webDict.get('value')
            for value in valueList:
                if len(title) > 0:
                    title = title + u', '
                title = title + value
            subtitle = u'网络释义: ' + webDict.get('key')
            wf.add_item(title=title, subtitle=subtitle, arg=title, copytext=True, valid=True)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
