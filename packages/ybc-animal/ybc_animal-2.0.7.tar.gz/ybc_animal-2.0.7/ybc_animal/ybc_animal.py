import requests
import json
import base64
import os
import sys
import os.path
import ybc_config
import ybc_player as player

__PREFIX = ybc_config.config['prefix']
__ANIMAL_URL = __PREFIX + ybc_config.uri + '/animal'

__TOP_NUM = 1
__MAX_TOP_NUM = 6


def _info(filename='', topnum=__TOP_NUM):
    """
    功能：识别图片中的动物信息。

    参数 filename 是当前目录下期望被识别的图片名字，
    可选参数 topnum 是可能的识别结果数量，最大为 6，默认为 1，
    返回：识别出的动物信息。
    """
    if not filename:
        return -1

    if topnum not in range(1, __MAX_TOP_NUM + 1):
        topnum = 1

    url = __ANIMAL_URL
    filepath = os.path.abspath(filename)
    data = {}
    data['topNum'] = topnum
    files = {
        'file': open(filepath, 'rb')
    }

    for i in range(3):
        r = requests.post(url, data=data, files=files)

        if r.status_code == 200:
            res = r.json()
            if (res['result']):
                if topnum == 1:
                    return res['result'][0]['name']
                else:
                    return res['result']

    raise ConnectionError('识别动物图片失败', r._content)

def desc(filename=''):
    if not filename:
        return -1
    res = _info(filename)
    # data文件夹路径
    data_path = os.path.abspath(__file__)
    data_path = os.path.split(data_path)[0]+'/data/'
    # 读取desc.json文件中数据
    f_shi = open(data_path + 'desc.json', encoding='utf-8')
    descjson = json.load(f_shi)
    f_shi.close()

    if res and res != '非动物':
        for item in descjson:
            if item['name'] == res:
                return res+os.linesep+item['description']
        s = res+',暂时没有介绍'
        return s
    else:
        return '这不是一个动物哟~'


def what(filename=''):
    """
    功能：识别图片中的动物种类。

    参数 filename 是当前目录下期望被识别的图片名字，

    返回：识别出的动物种类。
    """
    if not filename:
        return -1
    res = _info(filename)
    if res and res != '非动物':
        res = res.replace('犬','狗')
        res = res.replace('梗','狗')
        res = res.replace('多','狗')
        res = res.replace('基','狗')
        res = res.replace('奇','狗')
        res = res.replace('加','狗')
        res = res.replace('巴','狗')
        res = res.replace('八','狗')
        res = res.replace('美','狗')
        res = res.replace('迪','狗')
        res = res.replace('羔','羊')
        return res[-1:]
    else:
        return '这不是一个动物哟~'


def breed(filename=''):
    """
    功能：识别图片中的动物名称。

    参数 filename 是当前目录下期望被识别的图片名字，

    返回：识别出的动物名称。
    """
    if not filename:
        return -1
    res = _info(filename)
    if res and res != '非动物':
        res = res.replace('犬','狗')
        return res
    else:
        return '这不是一个动物哟~'


def sound(animal=''):
    """
    功能：播放相应动物的叫声。

    参数 animal是动物的种类，

    返回：无。
    """
    dir_res = os.path.abspath(__file__)
    dir_res = os.path.dirname(dir_res)
    if animal not in ('猫', '犬', '虎', '鸟', '狗', '羊'):
        player.play(dir_res+'/data/error.mp3')
    else:
        sound_dict = {
            '猫':'cat.mp3',
            '犬':'dog.mp3',
            '狗':'dog.mp3',
            '鸟':'bird.mp3',
            '羊':'sheep.mp3',
            '虎':'tiger.mp3'
        }
        filepath = dir_res+'/data/'+sound_dict[animal]
        player.play(filepath)


def main():
    print(desc('/Users/chenyue/Desktop/动物大全/ddh.jpeg'))
    pass


if __name__ == '__main__':
    main()
