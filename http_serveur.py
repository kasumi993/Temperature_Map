#coding:utf-8
import http.server

port=80
address=("",port)


handler=http.server.CGIHTTPRequestHandler
handler.cgi_directories=["/"]
httpd=http.server.HTTPServer(address,handler)


print(f"serveur python démarré sur le PORT {port}")

httpd.serve_forever()