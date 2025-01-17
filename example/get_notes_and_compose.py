import datetime
import json

import requests

import xhs.help
from xhs import XhsClient, SearchSortType, SearchNoteType
from openai import OpenAI


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
    cookie = "a1=1942bf22a705rk2g8czmlsiiic0lyr1ehcnf6kn2w50000125783; webId=49241bd165422b41b978e84f4c039fc8; gid=yYiSWYS2DWv0yYiSWYS2Kl83jKDqCdqVVJA8Y4d1CCW0d028KVS9v4888yYq4Jj8id4W0808; customerClientId=934657907755078; x-user-id-creator.xiaohongshu.com=5a997ef7db2e6040d372f94c; customer-sso-sid=68c5174525989699864733510c106e4bd8d45be3; access-token-creator.xiaohongshu.com=customer.creator.AT-68c51745259896998630512149wmu8d2lnymdtao; galaxy_creator_session_id=PQbPPd3bRZA5Hz5iAEEhKmiJjiZfte5NdAlw; galaxy.creator.beaker.session.id=1735193415027085561850; webBuild=4.50.1; xsecappid=xhs-pc-web; acw_tc=0a4ad62517353789475222469e871d15a17d01d144df7b10182b3e0b3b59b6; web_session=040069791562b6a5a91a0a805a354bb7faf158; unread={%22ub%22:%22676bd0a6000000001402742a%22%2C%22ue%22:%22676d406b000000001300a6b4%22%2C%22uc%22:29}; websectiga=a9bdcaed0af874f3a1431e94fbea410e8f738542fbb02df1e8e30c29ef3d91ac; sec_poison_id=eb2bf0cb-bd85-47bf-8284-0a4c677465b2"
    proxy_ip = '118.117.189.137:3828'
    proxies = {
        # 'http': 'http://{}'.format(proxy_ip),
        # 'https': 'http://{}'.format(proxy_ip)
    }
    xhs_client = XhsClient(cookie, sign=sign, proxies=proxies)
    file_content = ''
    chat_content = '''
标题：{}
-正文：
{}
这是一篇点赞量很高的的小红书博主的文稿，我希望你能详细拆解。其中必须
包括:标题、个性化和真实性、布局、长度、结构、表情包以及语言风格等。
然后根据拆解的部分进行权重分配。
最后请你按照分析的结果模仿该博主的写作风格，根据“{}”这些信息写一篇探店文稿，重点描述味道和体验不要提及价格。
要求口语化且字数不能大于原文，文末带话题标签格式为" #这是话题文字[话题]# "。只需要输出最后的文稿就行了。
'''
    # get note by keyword
    keyword = "这家店"
    data = xhs_client.get_note_by_keyword(keyword, sort=SearchSortType.MOST_POPULAR, note_type=SearchNoteType.IMAGE)
    # print(json.dumps(data, ensure_ascii=False, indent=2))
    for item in data['items']:
        if not item['model_type'] == 'note':
            continue
        source_note_url = "https://www.xiaohongshu.com/explore/{}?xsec_token={}&xsec_source=pc_feed".format(item['id'], item['xsec_token'])
        print("note_id:{},xsec_token:{}".format(item['id'], item['xsec_token']))
        print(source_note_url)
        note_info = xhs_client.get_note_by_id(item['id'], item['xsec_token'])
        item_content = chat_content.format(note_info['title'], note_info['desc'],
                                           "店名：金记三都烧鸭粉，地址：柳州市马鹿山农贸市场入口旁，口味：酸鲜甜，配料：烧鸭酱、白辣椒、蒜米、葱、香菜、辣油，送鸭头,下午六点开门")
        client = OpenAI(api_key="sk-f92524b97bd64f84928599e9ac6bbc30", base_url="https://api.deepseek.com")

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位小红书爆款文案写作大师。"},
                {"role": "user", "content": item_content},
            ],
            stream=False
        )
        file_content += source_note_url + "\n"
        file_content += response.choices[0].message.content + "\n\n"
        print(response.choices[0].message.content)
    f = open(r"D:\Kyle\demo_file.txt", "w", encoding='utf-8')
    f.write(file_content)
    f.close()


    # get note info
    # note_info = xhs_client.get_note_by_id("6559843e000000001f02d333", "ABvXuks91Jwa1OUCSf2x3w2lhQe1GJr15WQ5a_63uPx00=")
    # print(datetime.datetime.now())
    # print(json.dumps(note_info, indent=2, ensure_ascii=False))
    # print(xhs.help.get_imgs_url_from_note(note_info))
