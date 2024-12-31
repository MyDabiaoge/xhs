import json
from flask import Flask, request
import asyncio # 引入异步函数库
from playwright.async_api import async_playwright

app = Flask(__name__)

A1 = ""

stealth_js_path = r"D:\Kyle\PycharmProjects\stealth.min.js"

@app.route("/sign", methods=["POST"])
async def hello_world():
    req_json = request.get_json()
    uri = req_json["uri"]
    data = req_json["data"]
    a1 = req_json["a1"]
    web_session = req_json["web_session"]
    signature = await sign(uri, data, a1, web_session)
    return signature

async def sign(uri, data, a1, web_session):
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context()
        await context.add_init_script(path=stealth_js_path)
        page = await context.new_page()
        await page.goto("https://www.xiaohongshu.com")
        await page.wait_for_load_state('networkidle')
        # 设置cookie
        await context.add_cookies([
                    {'name': 'a1', 'value': a1, 'domain': ".xiaohongshu.com", 'path': "/"}]
                )
        # 重新加载页面
        await page.reload()
        await page.wait_for_load_state('networkidle')
        # 执行签名
        encrypt_params = await page.evaluate("([url, data]) => window._webmsxyw(url, data)", [uri, data])
        signature = {
            "x-s": encrypt_params["X-s"],
            "x-t": str(encrypt_params["X-t"])
        }
        # 关闭浏览器
        await browser.close()
        return signature

@app.route("/a1", methods=["GET"])
def get_a1():
    return {'a1': A1}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005)