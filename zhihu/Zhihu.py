# /usr/bin/env python
# coding=utf8

import sys
from workflow import Workflow3
from workflow import web


def autocomplete(q):
    param = {'token': q, 'max_matches': 10, 'use_similar': 0}
    return web.get('https://www.zhihu.com/autocomplete', param).json()


def get_url(type, id):
    return 'https://www.zhihu.com/%s/%s' % (type, id)


ITEM_LEN = 7


def get_question(item_list):
    for item in item_list:
        if isinstance(item, list) and len(item) >= ITEM_LEN:
            item_type = item[0]
            if item_type == 'question':
                title = item[1]
                subtitle = u'问题 - %d 个回答' % item[4]
                arg = get_url(item_type, str(item[3]))
                wf.add_item(title=title, subtitle=subtitle, arg=arg, valid=True)


def get_article(item_list):
    for item in item_list:
        if isinstance(item, list) and len(item) >= ITEM_LEN:
            item_type = item[0]
            if item_type == 'article':
                title = item[1]
                subtitle = u'专栏 - %d 个赞' % item[4]
                arg = 'https://zhuanlan.zhihu.com/p/%d' % item[3]
                wf.add_item(title=title, subtitle=subtitle, arg=arg, valid=True)


def get_people(item_list):
    for item in item_list:
        if isinstance(item, list) and len(item) >= ITEM_LEN:
            item_type = item[0]
            if item_type == 'people':
                title = item[1]
                subtitle = u'用户 - %s - %s' % (item[2], item[5])
                arg = get_url(item_type, item[2])
                wf.add_item(title=title, subtitle=subtitle, arg=arg, valid=True)


def get_topic(item_list):
    for item in item_list:
        if isinstance(item, list) and len(item) >= ITEM_LEN:
            item_type = item[0]
            if item_type == 'topic':
                title = item[1]
                subtitle = u'话题 - %d 个精选回答' % item[6]
                arg = get_url(item_type, str(item[2]))
                wf.add_item(title=title, subtitle=subtitle, arg=arg, valid=True)


def main(wf):
    args = wf.args
    q = args[0]

    data = autocomplete(q)

    if isinstance(data, list) and len(data) > 0:
        item_list = data[0]
        get_question(item_list)
        get_article(item_list)
        get_people(item_list)
        get_topic(item_list)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
