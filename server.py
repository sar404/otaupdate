from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os

PORT = int(os.environ.get("PORT", 8000))

class OTAHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode()

        print("REQ:", body)

        # balas ke endpoint XML lokal
        xml_url = f"http://{self.headers['Host']}/update.xml"

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(f"url={xml_url}".encode())

    def do_GET(self):
        if self.path == "/update.xml":
            self.send_response(200)
            self.send_header("Content-Type", "text/xml")
            self.end_headers()

            xml = """<?xml version="1.0" encoding="utf-8"?>
<update>
    <version>1.0.2</version>
    <url>http://YOUR-IP/update.zip</url>
    <md5>xxxxxxxx</md5>
    <size>850000000</size>
</update>
"""
            self.wfile.write(xml.encode())

HTTPServer(("0.0.0.0", PORT), OTAHandler).serve_forever()
