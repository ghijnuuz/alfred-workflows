# /usr/bin/env python
# coding=utf8

import sys
import os
import hashlib
import random
from workflow import Workflow3
from workflow import web

ERROR_CODE = {
    '101': '缺少必填的参数，出现这个情况还可能是et的值和实际加密方式不对应',
    '102': '不支持的语言类型',
    '103': '翻译文本过长',
    '104': '不支持的API类型',
    '105': '不支持的签名类型',
    '106': '不支持的响应类型',
    '107': '不支持的传输加密类型',
    '108': 'appKey无效，注册账号， 登录后台创建应用和实例并完成绑定， 可获得应用ID和密钥等信息，其中应用ID就是appKey（ 注意不是应用密钥）',
    '109': 'batchLog格式不正确',
    '110': '无相关服务的有效实例',
    '111': '开发者账号无效，可能是账号为欠费状态',
    '201': '解密失败，可能为DES,BASE64,URLDecode的错误',
    '202': '签名检验失败',
    '203': '访问IP地址不在可访问IP列表',
    '301': '辞典查询失败',
    '302': '翻译查询失败',
    '303': '服务端的其它异常',
    '401': '账户已经欠费停'
}


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

    param = {'q': q, 'from': fromLang, 'to': toLang, 'appKey': appKey, 'salt': salt, 'sign': sign}
    return web.get('http://openapi.youdao.com/api', param).json()


def check_success(data):
    if isinstance(data, dict) and data.get('errorCode') == '0':
        return True
    else:
        return False


def get_error(data):
    code = None
    if isinstance(data, dict):
        code = data.get('errorCode')

    title = 'ERROR'
    subtitle = '翻译失败啦'
    if isinstance(code, str):
        if ERROR_CODE.has_key(code):
            title = 'ERROR CODE: %s' % code
            subtitle = ERROR_CODE.get(code)
        else:
            title = 'ERROR CODE: %s' % code
            subtitle = '未知错误'

    wf.add_item(title=title, subtitle=subtitle)


def get_translation(data):
    translationData = data.get('translation')
    if translationData is not None:
        for translation in translationData:
            wf.add_item(title=translation, subtitle=u'翻译结果', arg=translation, valid=True)


def get_basic(data):
    basicData = data.get('basic')
    if basicData is not None:
        explains = basicData.get('explains')
        for explain in explains:
            wf.add_item(title=explain, subtitle=u'简明释义', arg=explain, valid=True)


def get_web(data):
    webData = data.get('web')
    if webData is not None:
        for webDict in webData:
            valueList = webDict.get('value')
            for value in valueList:
                title = value
                subtitle = u'网络释义: ' + webDict.get('key')
                wf.add_item(title=title, subtitle=subtitle, arg=title, valid=True)


def main(wf):
    args = wf.args
    if len(args) == 0:
        return

    q = args[0]

    data = translate(q)

    if check_success(data):
        get_translation(data)
        get_basic(data)
        get_web(data)
    else:
        get_error(data)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
