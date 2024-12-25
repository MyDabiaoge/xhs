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
    cookie = "a1=193f88d5792dw94q8ooz58pthxycmikfrcjssxkrz50000160260;webId=ba57f42593b9e55840a289fa0b755374;gid.sign=PSF1M3U6EBC/Jv6eGddPbmsWzLI=;gid=yYWfJfi820jSyYWfJfdidiKK0YfuyikEvfISMAM348TEJC28K23TxI888WJK84q8S4WfY2Sy;acw_tc=0a0d0ff917350428306458255e18ead771a3d446b4d581d29e507d9dc09aa6;customer-sso-sid=68c51745195228105544037247ac08d752e8c7cd;x-user-id-creator.xiaohongshu.com=5a997ef7db2e6040d372f94c;customerClientId=997110823847607;access-token-creator.xiaohongshu.com=customer.creator.AT-68c517451952281055440373sflpfoqltphp8on2;galaxy_creator_session_id=JT1hXBKsUFmbueeNTB3nnhLUfLzkVJQxaaIe;galaxy.creator.beaker.session.id=1735042846781022877260"
    xhs_client = XhsClient(cookie, sign=sign)
    title = "我是标题"
    desc = "下面我说两点 \n 1. 第一点 \n 2. 第二点"
    images = [
        r"C:\Users\85195\Pictures\IMG_7666.PNG",
    ]
    note = xhs_client.create_image_note(title, desc, images, is_private=True, post_time="2024-12-24 20:12:59")
    print(json.dumps(note, ensure_ascii=False, indent=2))
