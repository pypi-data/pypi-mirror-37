import requests
import json
import base64
import os
import ybc_config


__PREFIX = ybc_config.config['prefix']
__CAR_URL = __PREFIX + ybc_config.uri + '/carRecognition'


__TOP_NUM = 3


def car_recognition(filename='', topNum=__TOP_NUM):
    """
    功能：识别一个车辆图片的车型。

    参数 filename 是当前目录下期望被识别的图片名字，

    可选参数 topNum 是识别结果的数量，默认为 3 ，

    返回：识别出的车型信息。
    """

    if not filename:
        return -1

    url = __CAR_URL
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
                return res['result'][0]['name']

    raise ConnectionError('识别车辆图片失败', r._content)


def main():
    print(car_recognition('test.jpg'))


if __name__ == '__main__':
    main()
