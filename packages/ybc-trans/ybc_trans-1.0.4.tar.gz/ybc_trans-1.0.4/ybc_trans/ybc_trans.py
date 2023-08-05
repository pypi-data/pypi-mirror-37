import requests
import ybc_config

__PREFIX = ybc_config.config['prefix']
__TRANSLATE_URL = __PREFIX + ybc_config.uri + '/translate'

__CHINESE = 'zh-CHS'
__ENGLISH = 'EN'


def en2zh(text=''):
    """
    英译中接口。
    :param text: 要翻译的英文。
    :return: 翻译结果。
    """
    return translate(text, __ENGLISH, __CHINESE)


def zh2en(text=''):
    """
    中译英接口。
    :param text: 要翻译的中文。
    :return: 翻译结果。
    """
    return translate(text, __CHINESE, __ENGLISH)


def translate(text='', _from='', _to=''):
    """
    翻译接口。
    :param text: 要翻译的文本。
    :param _from: 源语言。
    :param _to: 目标语言。
    :return: 翻译结果。
    """
    if text == '':
        return -1

    data = {
        'q': text,
        'from': _from,
        'to': _to
    }
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }
    url = __TRANSLATE_URL

    for i in range(3):
        r = requests.post(url, json=data, headers=headers)
        if r.status_code == 200:
            res = r.json()
            if res['errorCode'] == "0" and res['translation']:
                return res['translation'][0]

    raise ConnectionError('获取翻译结果失败', r._content)

def main():
    print(zh2en('苹果'))
    print(en2zh('test'))


if __name__ == '__main__':
    main()
