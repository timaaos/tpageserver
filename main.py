# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import config
from tpage import tpage
import os


hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if(self.path.find(config.connect_css) > -1):
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.send_header("charset", "utf-8")
            self.end_headers()
            file = open(config.connect_css_location,mode='r',encoding="utf-8")
            page = file.read()
            file.close()
            self.wfile.write(bytes(page, "utf-8"))
            return
        if(self.path == "/info"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("charset", "utf-8")
            self.end_headers()
            self.wfile.write(bytes('<html><head><title>INFO</title></head>', "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>This is tpage webserver.</p>", "utf-8"))
            self.wfile.write(bytes(f"<p>tpage version: {tpage.version}</p>", "utf-8"))
            self.wfile.write(bytes(f"<p>connected css: {config.connect_css}</p>", "utf-8"))
            self.wfile.write(bytes(f"<p>main page location: {config.main_page}</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
        elif(self.path == "/docs"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("charset", "utf-8")
            self.end_headers()
            self.wfile.write(bytes('<html><head><title>DOCS</title></head>', "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes(f"<p>The docs for tpage {tpage.version}</p>", "utf-8"))
            self.wfile.write(bytes("<h2>Keys:</h2>", "utf-8"))
            self.wfile.write(bytes("<p>You need to have type of element in the key.</p>", "utf-8"))
            self.wfile.write(bytes("<h2>Types:</h2>", "utf-8"))
            self.wfile.write(bytes("<p>TITLE - the big text/title</p>", "utf-8"))
            self.wfile.write(bytes("<p>TEXT - just text</p>", "utf-8"))
            self.wfile.write(bytes("<p>RANDCHOOSE - random choose, the value needs to be like First,Second,Third</p>", "utf-8"))
            self.wfile.write(bytes("<p>RANDRANGE - random range, the value needs to be like 1,10</p>", "utf-8"))
            self.wfile.write(bytes("<p>IMAGE - image, the value needs to be url</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
        else:
            if(self.path[1:].endswith(".tpage")):
                if(not os.path.isfile('./pages/'+self.path[1:])):
                    self.send_response(404)
                    self.send_header("Content-type", "text/html")
                    self.send_header("charset", "utf-8")
                    self.end_headers()
                    openpage(self,config.not_found)
                    return
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("charset", "utf-8")
                self.end_headers()
                openpage(self,'./pages/'+self.path[1:])
            elif(self.path == "" or self.path == "/"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("charset", "utf-8")
                self.end_headers()
                openpage(self,config.main_page)
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.send_header("charset", "utf-8")
                self.end_headers()
                openpage(self,config.not_found)
def openpage(serv,name):
    file = open(name,mode='r',encoding="utf-8")
    page = tpage.parse(file.read())
    file.close()
    serv.wfile.write(bytes(f'<html><head><meta charset="utf-8"><title>{serv.path[1:]}</title>', "utf-8"))
    if(config.connect_css != False):
        serv.wfile.write(bytes(f'<link rel="stylesheet" href="{config.connect_css}">', "utf-8"))
    serv.wfile.write(bytes('</head>', "utf-8"))
    serv.wfile.write(bytes("<body>", "utf-8"))
    serv.wfile.write(bytes(tpage.getHTMLcode(page), "utf-8"))
    serv.wfile.write(bytes("</body></html>", "utf-8"))
        

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")