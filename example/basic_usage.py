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
                proxy = {"server": "http://171.110.83.124:3828"}
                # 如果一直失败可尝试设置成 False 让其打开浏览器，适当添加 sleep 可查看浏览器状态
                browser = chromium.launch(headless=True,proxy=proxy)

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
    # cookie = "abRequestId=7c2cb08a-a8b0-515e-8076-71004ef25bb1; a1=18fc78c5696b3xe3jj2q0lxx7ae6jctyyo8a40i4e50000183429; webId=49241bd165422b41b978e84f4c039fc8; gid=yYiSWYS2DWv0yYiSWYS2Kl83jKDqCdqVVJA8Y4d1CCW0d028KVS9v4888yYq4Jj8id4W0808; customer-sso-sid=68c5174489075830345800417a8732aeb15dee09; x-user-id-creator.xiaohongshu.com=5a997ef7db2e6040d372f94c; customerClientId=934657907755078; access-token-creator.xiaohongshu.com=customer.creator.AT-68c5174489075830344206547zrqjela3z8mr3zq; galaxy_creator_session_id=2i3XPZjSMedYeCxTum2Kh0xYH2p2zF1eRgE9; galaxy.creator.beaker.session.id=1734333947958091469973; webBuild=4.48.0; acw_tc=0a4acac317348842996138516ed956356bae10ccdfc66e8229d119b7be137c; websectiga=3fff3a6f9f07284b62c0f2ebf91a3b10193175c06e4f71492b60e056edcdebb2; sec_poison_id=e52241b4-3fc2-4720-992d-91c1d0ba6727; xsecappid=xhs-pc-web; unread={%22ub%22:%2263f8be830000000011012520%22%2C%22ue%22:%2264c3afcb0000000010031c34%22%2C%22uc%22:19}; web_session=040069791562b6a5a91a45745d354be477a4ed"
    cookie = "abRequestId=f51ece8d-2d31-5c60-99aa-5947824470d1; a1=193f24acc16ek9p8irh4z5m5g3nyw8phc8dygebt950000535067; webId=5e214287f2b4e99595b6ea0785b3f1fa; gid=yj88S2jjW2Adyj88S2jYihulSf2MdfJ2Vy1vxhl2361WfA28q0VVT6888JqKyy28i8Dffyd0; customerClientId=467080234129237; x-user-id-creator.xiaohongshu.com=5a997ef7db2e6040d372f94c; xsecappid=xhs-pc-web; webBuild=4.48.0; websectiga=984412fef754c018e472127b8effd174be8a5d51061c991aadd200c69a2801d6; sec_poison_id=c3d1526a-8ca3-4516-8e14-150558b98b49; acw_tc=0a4addf717348847666672685ed64e3b8ce01dc2b52f8df92aa0715697e632; unread={%22ub%22:%22674294370000000002028330%22%2C%22ue%22:%22674bd73a0000000008005b0c%22%2C%22uc%22:25}; web_session=04006979070577ea84d58c755d354bc713b469"
    proxy_ip = '171.110.83.124:3828'
    proxies = {
        'http': 'http://{}'.format(proxy_ip),
        'https': 'http://{}'.format(proxy_ip)
    }
    xhs_client = XhsClient(cookie, sign=sign, proxies=proxies)
    print(datetime.datetime.now())

    for _ in range(10):
        # 即便上面做了重试，还是有可能会遇到签名失败的情况，重试即可
        try:
            note = xhs_client.get_note_by_id("675f71a80000000002036c0d", "AByMVaWDZzWD1PveggbGD7YqZV94BCDukX-jhjbxqOgWo")
            print(json.dumps(note, indent=4, ensure_ascii=False))
            print(help.get_imgs_url_from_note(note))
            break
        except DataFetchError as e:
            print(e)
            print("失败重试一下下")
