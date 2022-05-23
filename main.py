# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import config
import tpage
import os


hostName = "localhost"
serverPort = 8082

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("charset", "utf-8")
        self.end_headers()
        if(self.path == "/info"):
            self.wfile.write(bytes('<html><head><title>INFO</title></head>', "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>This is tpage webserver.</p>", "utf-8"))
            self.wfile.write(bytes("<p>tpage version: 0.1</p>", "utf-8"))
            self.wfile.write(bytes(f"<p>connected css: {config.connect_css}</p>", "utf-8"))
            self.wfile.write(bytes(f"<p>main page location: {config.main_page}</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
        else:
            if(self.path[1:].endswith(".tpage")):
                file = open('./pages/'+self.path[1:],mode='r',encoding="utf-8")
                page = tpage.parse(file.read())
                file.close()
                self.wfile.write(bytes(f'<html><head><meta charset="utf-8"><title>{self.path[1:]}</title>', "utf-8"))
                if(config.connect_css != False):
                    self.wfile.write(bytes(f'<link rel="stylesheet" href="{config.connect_css}">', "utf-8"))
                self.wfile.write(bytes('</head>', "utf-8"))
                self.wfile.write(bytes("<body>", "utf-8"))
                self.wfile.write(bytes(tpage.getHTMLcode(page), "utf-8"))
                self.wfile.write(bytes("</body></html>", "utf-8"))
            elif(config.connect_css in self.path[1:]):
                file = open(config.connect_css,mode='r',encoding="utf-8")
                page = file.read()
                file.close()
                self.wfile.write(bytes(page, "utf-8"))
                return
            elif(self.path == "" or self.path == "/"):
                file = open(config.main_page,mode='r',encoding="utf-8")
                page = tpage.parse(file.read())
                file.close()
                self.wfile.write(bytes(f'<html><head><meta charset="utf-8"><title>{self.path[1:]}</title>', "utf-8"))
                if(config.connect_css != False):
                    self.wfile.write(bytes(f'<link rel="stylesheet" href="{config.connect_css}">', "utf-8"))
                self.wfile.write(bytes('</head>', "utf-8"))
                self.wfile.write(bytes("<body>", "utf-8"))
                self.wfile.write(bytes(tpage.getHTMLcode(page), "utf-8"))
                self.wfile.write(bytes("</body></html>", "utf-8"))

            
        

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")