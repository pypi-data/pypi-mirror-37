import requests
import json
import base64
import os
import ybc_config


__PREFIX = ybc_config.config['prefix']
__NAMECARD_URL = __PREFIX + ybc_config.uri + '/nameCardOcr'

__RETURN_IMAGE = 0


def namecard_info(filename=''):
    """
    功能：名片识别。

    参数 filename 是当前目录下期望被识别的图片名字，

    返回：识别出的名片信息。
    """

    if not filename:
        return -1

    url = __NAMECARD_URL
    filepath = os.path.abspath(filename)
    files = {
        'file': open(filepath, 'rb')
    }

    data = {
        'returnImage': __RETURN_IMAGE
    }

    for i in range(3):
        r = requests.post(url, files=files, data=data)
        if r.status_code == 200:
            res = r.json()
            if 'result_list' in res:
                res_dict = {}
                for val in res['result_list'][0]['data']:
                    res_dict[val['item']] = val['value']
                return res_dict

    raise ConnectionError('识别身份证图片失败', r._content)


def main():
    res = namecard_info('test.jpg')
    print(res)



if __name__ == '__main__':
    main()
