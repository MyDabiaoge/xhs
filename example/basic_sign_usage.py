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
    cookie = "a1=19413002a0acfy0ct7q9reydwq98m90pj9plsw2bk50000342548; webId=49241bd165422b41b978e84f4c039fc8; gid=yYiSWYS2DWv0yYiSWYS2Kl83jKDqCdqVVJA8Y4d1CCW0d028KVS9v4888yYq4Jj8id4W0808; customerClientId=934657907755078; x-user-id-creator.xiaohongshu.com=5a997ef7db2e6040d372f94c; customer-sso-sid=68c5174525989699864733510c106e4bd8d45be3; access-token-creator.xiaohongshu.com=customer.creator.AT-68c51745259896998630512149wmu8d2lnymdtao; galaxy_creator_session_id=PQbPPd3bRZA5Hz5iAEEhKmiJjiZfte5NdAlw; galaxy.creator.beaker.session.id=1735193415027085561850; webBuild=4.50.1; xsecappid=xhs-pc-web; acw_tc=0a4ad62517353789475222469e871d15a17d01d144df7b10182b3e0b3b59b6; web_session=040069791562b6a5a91a0a805a354bb7faf158; unread={%22ub%22:%22676bd0a6000000001402742a%22%2C%22ue%22:%22676d406b000000001300a6b4%22%2C%22uc%22:29}; websectiga=a9bdcaed0af874f3a1431e94fbea410e8f738542fbb02df1e8e30c29ef3d91ac; sec_poison_id=eb2bf0cb-bd85-47bf-8284-0a4c677465b2"
    proxy_ip = '118.117.189.137:3828'
    proxies = {
        # 'http': 'http://{}'.format(proxy_ip),
        # 'https': 'http://{}'.format(proxy_ip)
    }
    xhs_client = XhsClient(cookie, sign=sign, proxies=proxies)
    # # get note info
    # note_info = xhs_client.get_note_by_id("6559843e000000001f02d333", "ABvXuks91Jwa1OUCSf2x3w2lhQe1GJr15WQ5a_63uPx00=")
    # print(datetime.datetime.now())
    # print(json.dumps(note_info, indent=2, ensure_ascii=False))
    # print(xhs.help.get_imgs_url_from_note(note_info))

    #get note by keyword
    # keyword = "这家店"
    # data = xhs_client.get_note_by_keyword(keyword,sort = SearchSortType.MOST_POPULAR,note_type = SearchNoteType.IMAGE)
    # print(json.dumps(data, ensure_ascii=False, indent=2))

    #get topic
    topic_keyword = "Python"
    topics = xhs_client.get_suggest_topic(topic_keyword)
    print(json.dumps(topics, ensure_ascii=False, indent=2))