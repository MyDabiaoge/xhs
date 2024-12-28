import datetime
import json

import requests

import xhs.help
from xhs import XhsClient


def sign(uri, data=None, a1="", web_session=""):
    # 填写自己的 flask 签名服务端口地址
    res = requests.post("http://localhost:5005/sign",
                        json={"uri": uri, "data": data, "a1": a1, "web_session": web_session})
    signs = res.json()
    return {
        "x-s": signs["x-s"],
        "x-t": signs["x-t"]
    }


if __name__ == '__main__':
    # cookie = "abRequestId=f51ece8d-2d31-5c60-99aa-5947824470d1; a1=193f88d5792dw94q8ooz58pthxycmikfrcjssxkrz50000160260; webId=5e214287f2b4e99595b6ea0785b3f1fa; gid=yj88S2jjW2Adyj88S2jYihulSf2MdfJ2Vy1vxhl2361WfA28q0VVT6888JqKyy28i8Dffyd0; customerClientId=467080234129237; x-user-id-creator.xiaohongshu.com=5a997ef7db2e6040d372f94c; xsecappid=xhs-pc-web; webBuild=4.48.0; websectiga=984412fef754c018e472127b8effd174be8a5d51061c991aadd200c69a2801d6; sec_poison_id=c3d1526a-8ca3-4516-8e14-150558b98b49; acw_tc=0a4addf717348847666672685ed64e3b8ce01dc2b52f8df92aa0715697e632; unread={%22ub%22:%22674294370000000002028330%22%2C%22ue%22:%22674bd73a0000000008005b0c%22%2C%22uc%22:25}; web_session=04006979070577ea84d58c755d354bc713b469"
    cookie = "a1=194077c4f55k13xv9taixk77cfm7zf0z9bg7x9c5k50000264847;webId=ba57f42593b9e55840a289fa0b755374;gid.sign=PSF1M3U6EBC/Jv6eGddPbmsWzLI=;gid=yYWfJfi820jSyYWfJfdidiKK0YfuyikEvfISMAM348TEJC28K23TxI888WJK84q8S4WfY2Sy;acw_tc=0a0b147517352985280168421ed6072f13d4d0b94278652a98b6d885948cc4;web_session=040069791562b6a5a91a6bc65b354b22d997b0"
    proxy_ip = '118.117.189.137:3828'
    proxies = {
        # 'http': 'http://{}'.format(proxy_ip),
        # 'https': 'http://{}'.format(proxy_ip)
    }
    xhs_client = XhsClient(cookie, sign=sign, proxies=proxies)
    # get note info
    note_info = xhs_client.get_note_by_id("675f71a80000000002036c0d", "AByMVaWDZzWD1PveggbGD7YqZV94BCDukX-jhjbxqOgWo")
    print(datetime.datetime.now())
    print(json.dumps(note_info, indent=2, ensure_ascii=False))
    print(xhs.help.get_imgs_url_from_note(note_info))

    # proxy_ip = "219.144.183.6:3828"
    #
    # # 白名单方式（需提前设置白名单）
    # proxies = {
    #     "http": "http://%(proxy)s/" % {"proxy": proxy_ip},
    #     "https": "http://%(proxy)s/" % {"proxy": proxy_ip}
    # }
    #
    # # 要访问的目标网页
    # target_url = "https://www.xiaohongshu.com"
    #
    # # 使用代理IP发送请求
    # response = requests.get(target_url, proxies=proxies)
    #
    # # 获取页面内容
    # if response.status_code == 200:
    #     print(response.text)