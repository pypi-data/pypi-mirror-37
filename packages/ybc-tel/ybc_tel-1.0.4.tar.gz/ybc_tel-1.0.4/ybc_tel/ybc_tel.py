import json
import requests
import ybc_config

__PREFIX = ybc_config.config['prefix']
__TEL_URL = __PREFIX + ybc_config.uri + '/tel'


def detail(tel=''):
    """
    手机号码归属地信息查询。
    :param tel: 手机号码，
    :return: 手机号码归属地信息。
    """
    if tel == '':
        return -1

    url = __TEL_URL
    data = {
        'phone': tel
    }

    for i in range(3):
        r = requests.post(url, data=data)
        if r.status_code == 200:
            res = r.json()['result']
            if res:
                res_info = {}
                res_info['province'] = res['province']
                res_info['city'] = res['city']
                res_info['company'] = res['company']
                res_info['shouji'] = tel
                return res_info

    raise ConnectionError('获取翻译结果失败', r._content)


def main():
    print(detail('18635579617'))

if __name__ == '__main__':
    main()
