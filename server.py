"""
============================================================
第二课 · 练习用 echo 服务器（FastAPI）
============================================================
作用：把客户端发来的请求原样返回，让你看清自己发了什么。

运行方法（开一个终端）：
    python server.py

然后另开一个终端跑：
    python 01_http_basics_demo.py

这就是一次真实的「服务器 ↔ 客户端」通信，只不过服务器在你电脑上。
"""

from fastapi import FastAPI, HTTPException

app = FastAPI(title="第二课练习服务器")


@app.get("/")
def root():
    """根路径：确认服务器活着"""
    return {"message": "练习服务器运行中，去跑 01_http_basics_demo.py"}


@app.get("/echo")
def echo_get(city: str = None, q: str = None):
    """
    GET 演示：参数在 URL 后面
    访问 /echo?city=深圳&q=天气
    → 服务器把你的参数原样返回
    """
    return {"method": "GET", "params": {"city": city, "q": q}}


@app.post("/echo")
def echo_post(body: dict):
    """
    POST 演示：数据放在请求体 body（JSON）
    → 服务器把你发的 JSON 原样返回
    调 AI 就是这种形式！
    """
    return {"method": "POST", "received_json": body}


@app.get("/status/{code}")
def status(code: int):
    """状态码演示：/status/404 就返回 404，/status/500 就返回 500"""
    raise HTTPException(status_code=code, detail=f"这是状态码 {code} 的演示")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)

