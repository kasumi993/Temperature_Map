#coding:utf-8
import http.server
import socketserver

port=80
address=("",port)

handler=http.server.SimpleHTTPRequestHandler
httpd=socketserver.TCPServer(address,handler)


print(f"serveur python démarré sur le PORT {port}")

httpd.serve_forever()