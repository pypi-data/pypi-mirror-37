import requests
import json
import base64
import os
import math
import sys
import operator
import ybc_config


__PREFIX = ybc_config.config['prefix']
__FOOD_URL = __PREFIX + ybc_config.uri + '/food'


__TOP_NUM = 3
__NOT_FOOD = '非菜'

def check(filename=''):
    """
    功能：识别一个图片是否为美食图片。

    参数 filename 是当前目录下期望被识别的图片名字，

    返回：是否为美食。
    """
    if not filename:
        return False

    res = food_name(filename, 1)
    if res == __NOT_FOOD:
        return False
    return True


def food(filename='', topNum=__TOP_NUM):
    """
    功能：美食识别。

    参数 filename 是当前目录下期望被识别的图片名字，

    可选参数 topNum 是识别结果的数量，默认为 3 ，

    返回：图片的美食信息。
    """
    if not filename:
        return -1

    url = __FOOD_URL
    filepath = os.path.abspath(filename)
    files = {
        'file': open(filepath, 'rb')
    }
    data = {
        'topNum': topNum
    }
    for i in range(3):
        r = requests.post(url, files=files, data=data)
        if r.status_code == 200:
            res = r.json()
            if res['result']:
                if topNum == 1:
                    return res['result'][0]
                else:
                    return res['result']

    raise ConnectionError('识别美食图片失败', r._content)


def food_name(filename='', topNum=__TOP_NUM):
    """
    功能：美食名字识别。

    参数 filename 是当前目录下期望被识别的图片名字，

    可选参数 topNum 是识别结果的数量，默认为 3 ，

    返回：美食的名字。
    """
    res = food(filename, topNum)
    if topNum == 1:
        return res['name']
    else:
        sorted_res = sorted(res, key=operator.itemgetter('probability'), reverse=True)
        return sorted_res[0]['name']


def main():
    # print(food('test.jpg', 2))
    # print(food_name('test.jpg'))
    # print(check('test.jpg'))
    pass

if __name__ == '__main__':
    main()
