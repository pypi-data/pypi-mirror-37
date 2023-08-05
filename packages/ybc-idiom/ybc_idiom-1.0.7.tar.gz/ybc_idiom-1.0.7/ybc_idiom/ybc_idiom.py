import json
import requests
import os
import re
import ybc_config

__PREFIX = ybc_config.config['prefix']
__IDIOM_URL = __PREFIX + ybc_config.uri + '/idiom'

data_path = os.path.abspath(__file__)
data_path = os.path.split(data_path)[0]+'/idioms.txt'


def meaning(keyword=''):
    if keyword == '':
        return -1
    url = __IDIOM_URL

    data = {
        'keyword': keyword
    }

    for i in range(3):
        r = requests.post(url, data=data)
        if r.status_code == 200:
            res = r.json()['result']
            if res:
                return {
                    '名称': keyword,
                    '读音': '无' if res['pinyin'] == None else res['pinyin'],
                    '解释': '无' if res['chengyujs'] == None else res['chengyujs'],
                    '出自': '无' if res['from_'] == None else res['from'],
                    '近义词': '无' if res['tongyi'] == None else ','.join(res['tongyi']),
                    '反义词': '无' if res['fanyi'] == None else ','.join(res['fanyi']),
                    '举例': '无' if res['example'] == None else res['example'].replace(' ','')
                }
            else:
                raise ConnectionError('查询成语解释失败', r._content)


def search(keyword=''):
    '''模糊搜索成语'''

    if keyword == '':
        return -1

    f = open(data_path, encoding='UTF-8')
    content = f.read()
    f.close()
    s = re.findall('.*' + keyword + '.*', content)

    # 返回生僻成语较多，是否返回结果列表中的随机10个成语？
    if s:
        return s[0:10]
    else:
        return -1

def main():
    print(meaning('叶公好龙'))
    print(search('一'))


if __name__ == '__main__':
    main()
