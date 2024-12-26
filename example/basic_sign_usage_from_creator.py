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
    cookie = "abRequestId=f51ece8d-2d31-5c60-99aa-5947824470d1; a1=19401971259wb4c9xl1t33d882byoobq8c7egjuyv50000318902; webId=5e214287f2b4e99595b6ea0785b3f1fa; gid=yj88S2jjW2Adyj88S2jYihulSf2MdfJ2Vy1vxhl2361WfA28q0VVT6888JqKyy28i8Dffyd0; customerClientId=467080234129237; web_session=04006979070577ea84d58c755d354bc713b469; webBuild=4.48.0; acw_tc=0a0bb22a17351095230581775e685fd9de2ec120b67e0503f07e242d2a5764; unread={%22ub%22:%22674498ee000000000703956a%22%2C%22ue%22:%2267624677000000000900c391%22%2C%22uc%22:27}; xsecappid=ugc; customer-sso-sid=68c51745223875537428797164c02ae0d66276cc; x-user-id-creator.xiaohongshu.com=5aaa3fb811be102b099ad483; access-token-creator.xiaohongshu.com=customer.creator.AT-68c517452238755374287972eqil8bkxgumsncpb; galaxy_creator_session_id=9efCDTmEmhd6zc3LJd6s0WAUoyr9UqeFU2ii; galaxy.creator.beaker.session.id=1735109546625010850679; websectiga=2845367ec3848418062e761c09db7caf0e8b79d132ccdd1a4f8e64a11d0cac0d; sec_poison_id=30552b11-044b-4e0d-b5c4-353d1a7654eb"
    xhs_client = XhsClient(cookie, sign=sign)
    title = "第一次发,试试"
    desc = "看看效果 \n 1. 好好好 \n 2. 666"
    images = [
        r"C:\Users\85195\Pictures\IMG_7666.PNG",
    ]
    note = xhs_client.create_image_note(title, desc, images, is_private=True, post_time="2024-12-24 20:12:59")
    print(json.dumps(note, ensure_ascii=False, indent=2))

    cookie = "abRequestId=7c2cb08a-a8b0-515e-8076-71004ef25bb1; a1=19401971259wb4c9xl1t33d882byoobq8c7egjuyv50000318902; webId=49241bd165422b41b978e84f4c039fc8; gid=yYiSWYS2DWv0yYiSWYS2Kl83jKDqCdqVVJA8Y4d1CCW0d028KVS9v4888yYq4Jj8id4W0808; customerClientId=934657907755078; webBuild=4.48.0; customer-sso-sid=68c5174524078439415796153da0b274b0cca542; x-user-id-creator.xiaohongshu.com=5a997ef7db2e6040d372f94c; access-token-creator.xiaohongshu.com=customer.creator.AT-68c517452407843942009720p1wq4pu6lsbezwqa; galaxy_creator_session_id=KodKPrbARVxwXHtcLhTgGDQ6qLfzn5yLwbVU; galaxy.creator.beaker.session.id=1735148915196039695223; acw_tc=0ad6fbe517351512881038294ee97e6e9454ab39d5a4ae7ffd2d8944e0c87d; xsecappid=xhs-pc-web; websectiga=16f444b9ff5e3d7e258b5f7674489196303a0b160e16647c6c2b4dcb609f4134; sec_poison_id=5ebbd613-8111-4f58-a7a6-7cc4dcad61c6; web_session=040069791562b6a5a91ac91959354bfaecdee6; unread={%22ub%22:%22676be4f00000000014021f1f%22%2C%22ue%22:%2267653b800000000013018f46%22%2C%22uc%22:25}"
    xhs_client = XhsClient(cookie, sign=sign)
    title = "第一次发,试试"
    desc = "看看效果 \n 1. 好好好 \n 2. 666"
    images = [
        r"C:\Users\85195\Pictures\IMG_7666.PNG",
    ]
    note = xhs_client.create_image_note(title, desc, images, is_private=True, post_time="2024-12-24 20:12:59")
    print(json.dumps(note, ensure_ascii=False, indent=2))