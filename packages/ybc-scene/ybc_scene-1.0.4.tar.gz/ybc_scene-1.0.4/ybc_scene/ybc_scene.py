import requests
import json
import base64
import os
import math
import ybc_config

__PREFIX = ybc_config.config['prefix']
__SCENE_URL = __PREFIX + ybc_config.uri + '/sceneRecognition'
__OBJECT_URL = __PREFIX + ybc_config.uri + '/objectRecognition'


def scene_recog(filename=''):
    """
    场景识别。
    :param filename: 待识别图片文件。
    :return: 识别结果及置信度字典组成的列表。
    """
    url = __SCENE_URL
    return _imageRecognition(filename, url)


def object_recog(filename=''):
    """
    物体识别。
    :param filename: 待识别图片文件。
    :return: 识别结果及置信度字典组成的列表。
    """
    url = __OBJECT_URL
    return _imageRecognition(filename, url)


def _imageRecognition(filename='', url=''):
    if not filename:
        return -1

    filepath = os.path.abspath(filename)
    files = {
        'file': open(filepath, 'rb')
    }

    for i in range(3):
        r = requests.post(url, files=files)
        if r.status_code == 200:
            res = r.json()
            if res['errno'] == 0 and res['tags']:
                res_list = []
                sum = 0
                for val in res['tags']:
                    res_list.append({'label_id': val['value'],
                                     'label_confd': val['confidence']})
                    sum += val['confidence']
                for val in res_list:
                    val['label_confd'] = str(math.floor(val['label_confd']/sum * 100)) + '%'

                return res_list

    raise ConnectionError('识别物体或场景信息失败', r._content)


def main():
    res = object_recog('test.jpg')
    print(res)
    res = scene_recog('test.jpg')
    print(res)


if __name__ == '__main__':
    main()
