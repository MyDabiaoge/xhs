import datetime
import json

import requests

import xhs.help
from xhs import XhsClient, SearchSortType, SearchNoteType


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
    cookie = "a1=1942c36cefelx5gyf2va1k1e0d5jq5a9o31csgpa250000399247;webId=ba57f42593b9e55840a289fa0b755374;gid.sign=PSF1M3U6EBC/Jv6eGddPbmsWzLI=;gid=yYWfJfi820jSyYWfJfdidiKK0YfuyikEvfISMAM348TEJC28K23TxI888WJK84q8S4WfY2Sy;acw_tc=0a0bb32017359079957411593e10812b45ea7dcc85b9b6e1af16e0e13bef4a;web_session=040069791562b6a5a91ab79242354b47d04ffe"
    proxy_ip = '118.117.189.137:3828'
    proxies = {
        # 'http': 'http://{}'.format(proxy_ip),
        # 'https': 'http://{}'.format(proxy_ip)
    }
    xhs_client = XhsClient(cookie, sign=sign, proxies=proxies)
    # # get note info
    note_info = xhs_client.get_note_by_id("6559843e000000001f02d333", "ABvXuks91Jwa1OUCSf2x3w2lhQe1GJr15WQ5a_63uPx00=")
    print(datetime.datetime.now())
    print(json.dumps(note_info, indent=2, ensure_ascii=False))
    print(xhs.help.get_imgs_url_from_note(note_info))

    #get note by keyword
    # keyword = "这家店"
    # data = xhs_client.get_note_by_keyword(keyword,sort = SearchSortType.MOST_POPULAR,note_type = SearchNoteType.IMAGE)
    # print(json.dumps(data, ensure_ascii=False, indent=2))

    #get topic
    topic_keyword = "Python"
    topics = xhs_client.get_suggest_topic(topic_keyword)
    print(json.dumps(topics, ensure_ascii=False, indent=2))