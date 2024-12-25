import datetime
import json
from time import sleep

from playwright.sync_api import sync_playwright

from xhs import DataFetchError, XhsClient, help


def sign(uri, data=None, a1="", web_session=""):
    for _ in range(10):
        try:
            with sync_playwright() as playwright:
                stealth_js_path = r"D:\Kyle\PycharmProjects\stealth.min.js"
                chromium = playwright.chromium

                # 如果一直失败可尝试设置成 False 让其打开浏览器，适当添加 sleep 可查看浏览器状态
                browser = chromium.launch(headless=True)

                browser_context = browser.new_context()
                browser_context.add_init_script(path=stealth_js_path)
                context_page = browser_context.new_page()
                context_page.goto("https://www.xiaohongshu.com")
                browser_context.add_cookies([
                    {'name': 'a1', 'value': a1, 'domain': ".xiaohongshu.com", 'path': "/"}]
                )
                context_page.reload()
                # 这个地方设置完浏览器 cookie 之后，如果这儿不 sleep 一下签名获取就失败了，如果经常失败请设置长一点试试
                sleep(1)
                encrypt_params = context_page.evaluate("([url, data]) => window._webmsxyw(url, data)", [uri, data])
                return {
                    "x-s": encrypt_params["X-s"],
                    "x-t": str(encrypt_params["X-t"])
                }
        except Exception:
            # 这儿有时会出现 window._webmsxyw is not a function 或未知跳转错误，因此加一个失败重试趴
            pass
    raise Exception("重试了这么多次还是无法签名成功，寄寄寄")


if __name__ == '__main__':
    # cookie = "abRequestId=7c2cb08a-a8b0-515e-8076-71004ef25bb1; a1=18fc78c5696b3xe3jj2q0lxx7ae6jctyyo8a40i4e50000183429; webId=49241bd165422b41b978e84f4c039fc8; gid=yYiSWYS2DWv0yYiSWYS2Kl83jKDqCdqVVJA8Y4d1CCW0d028KVS9v4888yYq4Jj8id4W0808; customerClientId=934657907755078; webBuild=4.48.0; web_session=030037a164a6b31ced5cd70a10204ad64a1096; unread={%22ub%22:%22674a0e960000000006015e63%22%2C%22ue%22:%22674d0ae5000000000203b5cf%22%2C%22uc%22:25}; xsecappid=ugc; customer-sso-sid=68c51745195433404981116769e9f67e2aa260c4; x-user-id-creator.xiaohongshu.com=5a997ef7db2e6040d372f94c; access-token-creator.xiaohongshu.com=customer.creator.AT-68c517451954334050240257qzgyzdidxe627dsv; galaxy_creator_session_id=lmEWNESEZH1TCR9IzjGuew9UG7Wn3pOyStPG; galaxy.creator.beaker.session.id=1735043324606023086634; websectiga=8886be45f388a1ee7bf611a69f3e174cae48f1ea02c0f8ec3256031b8be9c7ee; sec_poison_id=76d122d0-3133-471c-b963-7253dea36b7c"
    cookie = "abRequestId=f51ece8d-2d31-5c60-99aa-5947824470d1; a1=1900c598fcd5sed25j1ly5iml7d3ajjkqvhqmzovo50000236115; webId=5e214287f2b4e99595b6ea0785b3f1fa; gid=yj88S2jjW2Adyj88S2jYihulSf2MdfJ2Vy1vxhl2361WfA28q0VVT6888JqKyy28i8Dffyd0; customerClientId=467080234129237; web_session=04006979070577ea84d58c755d354bc713b469; webBuild=4.48.0; acw_tc=0a0bb22a17351095230581775e685fd9de2ec120b67e0503f07e242d2a5764; unread={%22ub%22:%22674498ee000000000703956a%22%2C%22ue%22:%2267624677000000000900c391%22%2C%22uc%22:27}; xsecappid=ugc; customer-sso-sid=68c51745223875537428797164c02ae0d66276cc; x-user-id-creator.xiaohongshu.com=5aaa3fb811be102b099ad483; access-token-creator.xiaohongshu.com=customer.creator.AT-68c517452238755374287972eqil8bkxgumsncpb; galaxy_creator_session_id=9efCDTmEmhd6zc3LJd6s0WAUoyr9UqeFU2ii; galaxy.creator.beaker.session.id=1735109546625010850679; websectiga=2845367ec3848418062e761c09db7caf0e8b79d132ccdd1a4f8e64a11d0cac0d; sec_poison_id=30552b11-044b-4e0d-b5c4-353d1a7654eb"

    xhs_client = XhsClient(cookie, sign=sign)
    print(datetime.datetime.now())

    for _ in range(10):
        # 即便上面做了重试，还是有可能会遇到签名失败的情况，重试即可
        try:
            title = "我是标题"
            desc = "下面我说两点 \n 1. 第一点 \n 2. 第二点"
            images = [
                r"C:\Users\85195\Pictures\IMG_7666.PNG",
            ]
            note = xhs_client.create_image_note(title, desc, images, is_private=True, post_time="2024-12-24 20:12:59")
            print(json.dumps(note, ensure_ascii=False, indent=2))
            break
        except DataFetchError as e:
            print(e)
            print("失败重试一下下")
