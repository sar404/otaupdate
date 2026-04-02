class OTAHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/update.xml":
            self.send_response(200)
            self.send_header("Content-Type", "text/xml")
            self.end_headers()

            xml = """<?xml version="1.0" encoding="utf-8"?>
<update>
    <version>1.0.2</version>
    <url>http://YOUR-SERVER/update.zip</url>
    <md5>xxxxxxxx</md5>
    <size>850000000</size>
</update>
"""
            self.wfile.write(xml.encode())
