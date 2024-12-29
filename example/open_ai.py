from openai import OpenAI

client = OpenAI(api_key="sk-f92524b97bd64f84928599e9ac6bbc30", base_url="https://api.deepseek.com")
content = '''
标题:湖州｜这家蛋糕店我真的超爱的🎂
-正文:
织里茵特拉根小镇里的一家宝藏蛋糕店哦
📍六日姐姐～
蛋糕颜值超高的 自己给图片的话还原度也很棒👍
用料夹心什么的都很不错哒～
小姐姐态度也很好的
好吃好看主要价格还不贵 安利
这是一篇点赞量很高的的小红书博主的文稿，我希望你能详细拆解。其中必须
包括:标题、个性化和真实性、布局、长度、结构、表情包以及语言风格等。然后根据拆解的部分进行权重分配。最后请你模仿该博主的写作风格，帮我写一篇关于“店名：金记三都烧鸭粉店，地址：柳州市马场路”的文稿，要求字数相近，带话题标签。只需要输出最后的文稿就行了。
'''
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是 DeepSeek，负责小红书博主文稿拆解与模仿。"},
        {"role": "user", "content": content},
    ],
    stream=False
)

print(response.choices[0].message.content)