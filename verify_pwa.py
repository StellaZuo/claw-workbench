# -*- coding: utf-8 -*-
import http.server, socketserver, threading, urllib.request, json, os

os.chdir(r'C:\Users\叶磊\WorkBuddy\Claw\workbench')
PORT = 8124
httpd = socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()

paths = ['index.html', 'manifest.json', 'sw.js', 'data.js',
         'icons/icon-192.png', 'icons/icon-512.png']
print("=== 资源可达性 (HTTP 状态码) ===")
for p in paths:
    try:
        r = urllib.request.urlopen(f'http://localhost:{PORT}/{p}', timeout=5)
        print(f"  {p} -> {r.status}")
    except Exception as e:
        print(f"  {p} -> ERR {e}")

print("=== manifest.json 合法性 ===")
try:
    m = json.load(open('manifest.json', encoding='utf-8'))
    print("  OK | name=", m.get('name'), "| display=", m.get('display'))
except Exception as e:
    print("  ERR", e)

print("=== data.js 合法性 ===")
t = open('data.js', encoding='utf-8').read()
assert t.startswith('window.WB_DATA'), "data.js 必须以 window.WB_DATA 开头"
print("  OK | 大小", len(t), "字节")

httpd.shutdown()
print("done")
