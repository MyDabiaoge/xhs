import datetime
import json
from time import sleep

from playwright.sync_api import sync_playwright

from xhs import DataFetchError, XhsClient


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
    cookie = "a1=1942b06f88dyuly5edy9w38az5air6jpaaooeoak050000265811; webId=49241bd165422b41b978e84f4c039fc8; gid=yYiSWYS2DWv0yYiSWYS2Kl83jKDqCdqVVJA8Y4d1CCW0d028KVS9v4888yYq4Jj8id4W0808; customerClientId=934657907755078; x-user-id-creator.xiaohongshu.com=5a997ef7db2e6040d372f94c; customer-sso-sid=68c5174525989699864733510c106e4bd8d45be3; access-token-creator.xiaohongshu.com=customer.creator.AT-68c51745259896998630512149wmu8d2lnymdtao; galaxy_creator_session_id=PQbPPd3bRZA5Hz5iAEEhKmiJjiZfte5NdAlw; galaxy.creator.beaker.session.id=1735193415027085561850; webBuild=4.50.1; xsecappid=xhs-pc-web; acw_tc=0a4ad62517353789475222469e871d15a17d01d144df7b10182b3e0b3b59b6; web_session=040069791562b6a5a91a0a805a354bb7faf158; unread={%22ub%22:%22676bd0a6000000001402742a%22%2C%22ue%22:%22676d406b000000001300a6b4%22%2C%22uc%22:29}; websectiga=a9bdcaed0af874f3a1431e94fbea410e8f738542fbb02df1e8e30c29ef3d91ac; sec_poison_id=eb2bf0cb-bd85-47bf-8284-0a4c677465b2"

    xhs_client = XhsClient(sign=sign)
    print(datetime.datetime.now())
    phone = "17687225691"
    res = xhs_client.send_code(phone)
    print("验证码发送成功~")
    code = input("请输入验证码：")
    token = ""
    while True:
        try:
            check_res = xhs_client.check_code(phone, code)
            token = check_res["mobile_token"]
            break
        except DataFetchError as e:
            print(e)
            code = input("请输入验证码：")
    login_res = xhs_client.login_code(phone, token)
    print(json.dumps(login_res, indent=4))
    print("当前 cookie：" + xhs_client.cookie)

    print(xhs_client.get_self_info())
