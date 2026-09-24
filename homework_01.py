"""
============================================================
第二课 · 作业 1：用 requests 裸调 DeepSeek（不用 SDK）
============================================================
目标：亲手写一次 POST + JSON，彻底搞懂 SDK 背后发生了什么。

需要的东西（README 里都有）：
- 接口地址: https://api.deepseek.com/chat/completions
- 请求头:   Authorization: Bearer <你的key>   +   Content-Type: application/json
- 请求体:   {"model": "deepseek-v4-pro",
             "messages": [{"role": "user", "content": "..."}]}

环境变量 DEEPSEEK_API_KEY 你应该已经配置过了（AI 伴侣项目用过）
"""

import os
import requests

DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"


def chat(user_message: str) -> str:
    """
    你的任务：用 requests.post 调 DeepSeek，返回 AI 的回复文本。
    步骤：
      1. 构造 headers（从环境变量读 key：os.environ.get("DEEPSEEK_API_KEY")）
      2. 构造 json body（model 用 "deepseek-v4-pro"，messages 里放 user 消息）
      3. 发 POST 请求
      4. 检查状态码，打印出来（不是 200 就 print 错误信息）
      5. 从 response.json() 里取出回复文本
         → 路径是 data["choices"][0]["message"]["content"]
      6. return 这段文本
    """
    # ── 第 1 步：信封封面（headers）──
    headers = {
        "Authorization": "Bearer " + os.environ.get("DEEPSEEK_API_KEY"),  # 注意 Bearer 后面有空格
        "Content-Type": "application/json",
    }

    # ── 第 2 步：信纸（body）──
    body = {
        "model": "deepseek-v4-pro",
        "messages": [{"role": "user", "content": user_message}],
    }

    # ── 第 3 步：寄出去（POST）──
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=body)

    # ★ 新加的：先看状态码
    if response.status_code != 200:
        # 不是 200 → 别急着拆信，把错误原因告诉用户
        return f"请求失败（状态码 {response.status_code}）: {response.text}"

    # ── 第 4 步：检查回信 + 取出 AI 的回答 ──
    print(f"状态码: {response.status_code}")
    data = response.json()
    return data["choices"][0]["message"]["content"]


# 测试（不要改）
if __name__ == "__main__":
    reply = chat("黄灿灿是谁")
    print(f"\n[机器人] AI 回复: {reply}")

    # 加分题：改成多轮对话（把历史消息也传进去）
    # reply = chat("我刚刚问了什么？")  # 如果你没传历史，AI 是不记得的
