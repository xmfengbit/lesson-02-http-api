"""
============================================================
第二课 · HTTP 与 API 演示：一次请求的完整解剖
============================================================
前置：先开一个终端运行  python server.py
然后本脚本在另一个终端运行：python 01_http_basics_demo.py
"""

import requests

# 本地练习服务器地址（你电脑上的 FastAPI）
BASE_URL = "http://127.0.0.1:8001"

print("=" * 55)
print("演示 0：确认服务器活着")
print("=" * 55)

response = requests.get(f"{BASE_URL}/")
print(f"状态码: {response.status_code}")
print(f"服务器说: {response.json()}")

print("\n" + "=" * 55)
print("演示 1：GET 请求（取数据，参数在 URL 后面）")
print("=" * 55)

# ① 发请求
response = requests.get(f"{BASE_URL}/echo", params={"city": "深圳", "q": "天气"})

# ② 看状态码
print(f"状态码: {response.status_code}")          # 应该是 200

# ③ 看响应头（挑几个重要的）
print(f"Content-Type: {response.headers.get('Content-Type')}")
print(f"服务器: {response.headers.get('Server')}")

# ④ 拿数据
data = response.json()
print(f"\n服务器返回: {data}")
print(f"服务器收到的参数: {data['params']}")

print("\n" + "=" * 55)
print("演示 2：POST 请求（提交数据）——这就是调 AI 的方式")
print("=" * 55)

# json= 参数会自动帮你做「Python dict → JSON 字符串」
response = requests.post(
    f"{BASE_URL}/echo",
    json={"model": "deepseek-v4-pro", "messages": [{"role": "user", "content": "你好"}]},
)

print(f"状态码: {response.status_code}")
data = response.json()
print(f"服务器收到的 JSON: {data['received_json']}")

print("\n" + "=" * 55)
print("演示 3：请求头 = 身份证明（API Key 放在这里）")
print("=" * 55)

# 真正的 AI API 调用都会带 Authorization 头
headers = {
    "Authorization": "Bearer sk-1234567890",
    "Content-Type": "application/json",
}
response = requests.post(f"{BASE_URL}/echo", headers=headers, json={"prompt": "test"})
print(f"服务器收到请求头: {response.request.headers}")

print("\n" + "=" * 55)
print("演示 4：错误状态码（404 = 地址不存在）")
print("=" * 55)

response = requests.get(f"{BASE_URL}/status/404")
print(f"状态码: {response.status_code}  ← 这就是 404，地址/资源不存在")

print("\n[OK] 看明白这 4 个演示后，去做 homework_01.py（真刀真枪调 DeepSeek）")


