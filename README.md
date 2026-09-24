# 第二课 · HTTP 与 API 原理（补上你「调过但不太懂」的部分）

你之前做过两件和 API 有关的事：
1. 用 `requests.get()` 爬网页（Tiobe 榜单）
2. 用 OpenAI SDK 调 DeepSeek（AI 伴侣）

这两件事背后是**同一个东西**：HTTP 请求。
这一课把它们打通，让你从「会用」变成「懂」。

---

## 1. 一次 HTTP 请求 = 寄信

```
你 (客户端)                   服务器
   │                              │
   │  ① 寄一封信（请求 Request）   │
   │ ────────────────────────────▶│
   │                              │ ② 处理
   │  ③ 收到回信（响应 Response）  │
   │ ◀────────────────────────────│
```

一封信（请求）包含 4 个部分：

| 部分 | 例子 | 作用 |
|---|---|---|
| **URL** | `http://127.0.0.1:8001/echo` | 寄给谁（地址） |
| **方法** | `GET` / `POST` | 要干什么 |
| **请求头** | `Authorization: Bearer xxx` | 信封上的签名（身份） |
| **请求体** | `{"model": "deepseek-v4-pro", ...}` | 信里的内容（POST 才有） |

## 2. 方法：GET vs POST（面试必问）

| | GET | POST |
|---|---|---|
| 用途 | **取数据** | **提交/创建数据** |
| 参数在哪 | URL 后面 `?key=value` | 请求体 body（JSON） |
| 例子 | 查天气、看榜单 | 发消息给 AI、注册账号 |
| 安全性 | 参数会留在历史记录 | 参数在 body，更隐蔽 |

> 你爬 Tiobe 用的 `requests.get(url)` 就是 GET。
> 你调 DeepSeek 用的 SDK，底层其实是一次 **POST**：
> ```
> POST https://api.deepseek.com/chat/completions
> Content-Type: application/json
> Authorization: Bearer sk-xxxx
>
> {"model": "deepseek-v4-pro",
>  "messages": [{"role": "user", "content": "你好"}]}
> ```
> SDK 只是帮你把这些细节藏起来了。作业要你亲手写一次。

## 3. 状态码（响应头上的数字）

| 状态码 | 含义 | 你遇到的场景 |
|---|---|---|
| 200 | 成功 | ✅ 正常返回 |
| 201 | 创建成功 | POST 后常见 |
| 400 | 请求写错了 | 参数不对 |
| 401 | 没登录/Key 错 | API Key 无效 |
| 404 | 地址不存在 | URL 拼错 |
| 429 | 请求太频繁 | 被限流 |
| 500 | 服务器炸了 | 不是你的错 |

> 面试常问：**你的程序调用 API 返回 429 怎么办？**
> 答：说明被限流 → 加等待重试（退避）→ 仍失败则降级提示用户。
> （这是后面「工程化」课的重点，先记住答案方向）

## 4. JSON：服务器和你的通用语言

- JSON = 一种文本格式，Python 的 `dict`/`list` 可以直接对应
- 服务器返回的永远是**字符串**，要 `response.json()` 转成 Python 对象
- 你发请求时，`json=` 参数会自动帮你做「Python 对象 → JSON 字符串」

```python
# 发：Python dict → JSON 字符串 → 服务器
response = requests.post(url, json={"name": "张三"})

# 收：JSON 字符串 → Python dict
data = response.json()
print(data["name"])
```

## 5. 跑起来（本课全部在自己电脑上，不需要外网）

本课用一个「本地 echo 服务器」练习，你把请求发给它，它原样返回，
这样你能看清自己到底发了什么。服务器就是第六章学过的 FastAPI。

```bash
# 终端 1：启动练习服务器（一直开着）
cd D:\agent-learning\lesson-02-http-api
python server.py

# 终端 2：运行演示（GET / POST / 状态码 全部解剖）
python 01_http_basics_demo.py
```

## 6. 用 requests 的 4 个核心口诀

```python
response = requests.get(url)                     # 1. 发请求
print(response.status_code)                      # 2. 看状态码（200？）
print(response.headers)                          # 3. 看响应头（可选）
data = response.json()                           # 4. 拿数据（转成 Python）
```

---

## 📝 本课作业（写完发我检查）

1. 运行 `server.py` + `01_http_basics_demo.py`，看懂每行在做什么
2. 完成 `homework_01.py`：用 requests **裸调** DeepSeek（不用 SDK），实现一个对话函数
3. 用一句话回答：为什么 AI 伴侣项目里的 `client.chat.completions.create(...)` 底层其实是一次 POST？

> 提示：DeepSeek 的接口地址、请求头、请求体格式都在上面的 README 里。

---
> 🎞 配套课件：第二课-HTTP与API.pptx（13 页，带讲稿备注，可逐页自学）

