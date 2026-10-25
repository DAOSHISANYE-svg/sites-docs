#!/usr/bin/env python
"""karing-github-api.py · 经 Karing CONNECT 隧道调 GitHub REST API（本机 github 段直连全 000）
原理: Karing :3066 对 CONNECT 隧道放行任意 host（实测 api.github.com TLS 隧道 200）;
      原始 socket → CONNECT → ssl 包装 → REST。token 自动从 %USERPROFILE%/.git-credentials 取。
用法:
  python karing-github-api.py GET /user
  python karing-github-api.py POST /user/repos '{"name":"x","private":false}'
  python karing-github-api.py GET /repos/DAOSHISANYE-svg/sites-docs/commits/main
输出: HTTP 状态行 + JSON body（美化）。退出码: 0=2xx/3xx, 1=4xx/5xx, 2=隧道/网络失败
详见 decisions/ADR-007。
"""
import json, os, re, socket, ssl, sys

TUNNEL = ("127.0.0.1", 3066)

def load_token():
    for cand in (os.path.expanduser("~/.git-credentials"), os.path.join(os.sep, "c", "Users", "junji", ".git-credentials")):
        try:
            for line in open(cand, encoding="utf-8", errors="replace"):
                m = re.match(r"https?://[^:]+:(\S+)@github\.com", line.strip())
                if m:
                    return m.group(1)
        except OSError:
            continue
    sys.exit("未找到 github token（需 ~/.git-credentials 一行 https://user:<token>@github.com）")

def call(host, method, path, token, body=None, attempt=1):
    try:
        s = socket.create_connection(TUNNEL, timeout=30)
    except OSError:
        if attempt >= 2:
            sys.exit("隧道失败: CONNECT 无响应（Karing 服务是否在跑? tasklist | grep karing）")
        import time
        time.sleep(2)
        return call(host, method, path, token, body, attempt + 1)
    s.sendall(f"CONNECT {host}:443 HTTP/1.1\r\nHost: {host}\r\n\r\n".encode())
    buf = b""
    while b"\r\n\r\n" not in buf:
        c = s.recv(4096)
        if not c:
            s.close()
            sys.exit("隧道失败: CONNECT 无响应（Karing 服务是否在跑? tasklist | grep karing）")
        buf += c
    if b" 200" not in buf.split(b"\r\n")[0]:
        s.close()
        sys.exit(f"隧道失败: {buf.decode('latin1','ignore')[:120]}")
    ts = ssl.create_default_context().wrap_socket(s, server_hostname=host)
    raw = json.dumps(body).encode() if body else b""
    hdrs = (f"{method} {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: karing-github-api/1.0\r\n"
            f"Accept: application/vnd.github+json\r\nAuthorization: token {token}\r\n")
    if raw:
        hdrs += f"Content-Type: application/json\r\nContent-Length: {len(raw)}\r\n"
    ts.sendall(hdrs.encode() + b"\r\n" + raw)
    data = b""
    while True:
        c = ts.recv(65536)
        if not c:
            break
        data += c
    ts.close()
    parts = data.split(b"\r\n\r\n", 1)
    line = parts[0].decode("latin1", "ignore").split("\r\n")[0]
    body2 = parts[1].decode("utf-8", "ignore") if len(parts) > 1 else ""
    print(line)
    try:
        print(json.dumps(json.loads(body2), ensure_ascii=False, indent=1)[:8000])
        code = int(line.split(" ")[1])
        sys.exit(0 if code < 400 else 1)
    except (json.JSONDecodeError, ValueError):
        print(body2[:2000])
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    host = sys.argv[1] if sys.argv[1].count(".") else "api.github.com"
    method, path = (sys.argv[1], sys.argv[2]) if sys.argv[1] in ("GET", "POST", "PUT", "DELETE", "PATCH") else ("GET", sys.argv[1])
    body = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
    call(host, method, path, load_token(), body)
