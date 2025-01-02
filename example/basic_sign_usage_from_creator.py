import datetime
import json
from pydoc_data.topics import topics

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
    # cookie = "abRequestId=f51ece8d-2d31-5c60-99aa-5947824470d1; a1=19401971259wb4c9xl1t33d882byoobq8c7egjuyv50000318902; webId=5e214287f2b4e99595b6ea0785b3f1fa; gid=yj88S2jjW2Adyj88S2jYihulSf2MdfJ2Vy1vxhl2361WfA28q0VVT6888JqKyy28i8Dffyd0; customerClientId=467080234129237; web_session=04006979070577ea84d58c755d354bc713b469; webBuild=4.48.0; acw_tc=0a0bb22a17351095230581775e685fd9de2ec120b67e0503f07e242d2a5764; unread={%22ub%22:%22674498ee000000000703956a%22%2C%22ue%22:%2267624677000000000900c391%22%2C%22uc%22:27}; xsecappid=ugc; customer-sso-sid=68c51745223875537428797164c02ae0d66276cc; x-user-id-creator.xiaohongshu.com=5aaa3fb811be102b099ad483; access-token-creator.xiaohongshu.com=customer.creator.AT-68c517452238755374287972eqil8bkxgumsncpb; galaxy_creator_session_id=9efCDTmEmhd6zc3LJd6s0WAUoyr9UqeFU2ii; galaxy.creator.beaker.session.id=1735109546625010850679; websectiga=2845367ec3848418062e761c09db7caf0e8b79d132ccdd1a4f8e64a11d0cac0d; sec_poison_id=30552b11-044b-4e0d-b5c4-353d1a7654eb"
    # xhs_client = XhsClient(cookie, sign=sign)
    # title = "第一次发,试试"
    # desc = "看看效果 \n 1. 好好好 \n 2. 666"
    # images = [
    #     r"C:\Users\85195\Pictures\IMG_7666.PNG",
    # ]
    # note = xhs_client.create_image_note(title, desc, images, is_private=True, post_time="2024-12-24 20:12:59")
    # print(json.dumps(note, ensure_ascii=False, indent=2))

    cookie = "a1=194135c1450y6vt776r1mpkt26b0cke9g3peq4drj50000113707; webId=8565665a4f270d4e4533502376f271ff; gid=yj4yq2SyfjkJyj4yq2Sy4q4f28vKh9WWKFy6UFVUT9JKDd288STdjA888yyqW8W8WdJqij0J; abRequestId=8565665a4f270d4e4533502376f271ff; webBuild=4.51.1; web_session=04006979070577ea84d5258746354b8a8f782a; customer-sso-sid=68c517454529940037871464e58f3de2a90eb674; x-user-id-creator.xiaohongshu.com=5aaa3fb811be102b099ad483; customerClientId=251402100558487; access-token-creator.xiaohongshu.com=customer.creator.AT-68c517454529940037871465xpmtnops0mfjpv19; galaxy_creator_session_id=1QNeptYrgdNPwxMdVshktmp2G7Vi4v6gSOcA; galaxy.creator.beaker.session.id=1735643004845086970825; xsecappid=ugc; acw_tc=0ad5861d17358287595447696e7019897fdaa66f7ddfefc652bd6c9de9d10a; websectiga=9730ffafd96f2d09dc024760e253af6ab1feb0002827740b95a255ddf6847fc8; sec_poison_id=acd6f410-bf73-4c24-a6d7-ed6b1a5116ad"
    xhs_client = XhsClient(cookie, sign=sign)
    title = "OMG！！！这家烧鸭粉店绝了！！！"
    desc = '''谁懂啊？？？这家金记三都烧鸭粉真的是个宝藏店铺，柳州人的天堂，不仅有酸鲜甜的口感，还有各种配料！！！！

下午六点开门，我准时冲进去，一进门就被那香气给迷住了。烧鸭酱的浓郁，白辣椒的刺激，蒜米的香，葱和香菜的清新，再加上辣油的点睛之笔，每一口都是味蕾的狂欢。最惊喜的是，还送鸭头，简直是意外的惊喜！

这家店在马鹿山农贸市场入口旁，位置虽然不起眼，但味道绝对让你惊艳。每一口都让人回味无穷，真的是酸鲜甜的完美结合。吃完一碗，还想再来一碗，根本停不下来！
#柳州美食[话题]# #烧鸭粉[话题]# #柳州探店[话题]# #美食日常[话题]# #宝藏店铺[话题]#'''
    images = [
        r"C:\Users\85195\Downloads\IMG_0095.JPG",
        r"C:\Users\85195\Downloads\IMG_0100.JPG",
        r"C:\Users\85195\Downloads\IMG_0101.JPG",
    ]
    topics = []
    topic_keyword_list = ["柳州美食", "烧鸭粉", "柳州探店", "美食日常", "宝藏店铺"]
    for topic_keyword in topic_keyword_list:
        item_topics = xhs_client.get_suggest_topic(topic_keyword)
        if len(item_topics) > 0:
            topic = {
                "id": item_topics[0]["id"],
                "name": item_topics[0]["name"],
                "type": "topic",
                "link": item_topics[0]["link"],
            }
            topics.append(topic)

    print(topics)
    note = xhs_client.create_image_note(title, desc, images, topics=topics, is_private=True,
                                        post_time="2024-12-24 20:12:59")
    print(json.dumps(note, ensure_ascii=False, indent=2))
