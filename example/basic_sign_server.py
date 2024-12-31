import time
import json

from flask import Flask, request
from gevent import monkey
from playwright.sync_api import sync_playwright

monkey.patch_all()

app = Flask(__name__)

A1 = ""


def get_context_page(instance, stealth_js_path):
    chromium = instance.chromium
    browser = chromium.launch(headless=True)
    context = browser.new_context()
    context.add_init_script(path=stealth_js_path)
    page = context.new_page()
    return context, page


# 如下更改为 stealth.min.js 文件路径地址
stealth_js_path = r"D:\Kyle\PycharmProjects\stealth.min.js"
print("正在启动 playwright")
playwright = sync_playwright().start()
browser_context, context_page = get_context_page(playwright, stealth_js_path)
context_page.goto("https://www.xiaohongshu.com")
print("正在跳转至小红书首页")
time.sleep(5)
context_page.reload()
time.sleep(1)
cookies = browser_context.cookies()
for cookie in cookies:
    if cookie["name"] == "a1":
        A1 = cookie["value"]
        print("当前浏览器 cookie 中 a1 值为：" + cookie["value"] + "，请将需要使用的 a1 设置成一样方可签名成功")
print("跳转小红书首页成功，等待调用")


def sign(uri, data, a1, web_session):
    try:
        # context_page.reload()
        # # 确保页面加载完成
        # context_page.wait_for_load_state('networkidle')
        #
        # # 检查页面是否处于预期状态
        # if not context_page.is_visible('body'):
        #     raise Exception("页面未加载完成或未处于预期状态")
        encrypt_params = context_page.evaluate("([url, data]) => window._webmsxyw(url, data)", [uri, data])
        return {
            "x-s": encrypt_params["X-s"],
            "x-t": str(encrypt_params["X-t"])
        }
    except  Exception as e:
        raise Exception(e)



@app.route("/sign", methods=["POST"])
def hello_world():
    req_json = request.json
    # print(json.dumps(req_json, indent=2, ensure_ascii=False))
    uri = req_json["uri"]
    data = req_json["data"]
    a1 = req_json["a1"]
    web_session = req_json["web_session"]
    return sign(uri, data, a1, web_session)


@app.route("/a1", methods=["GET"])
def get_a1():
    return {'a1': A1}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005)
