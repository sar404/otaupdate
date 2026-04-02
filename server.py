from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os

PORT = int(os.environ.get("PORT", 8000))

OTA_MAP = {
    "1.0.0": "https://raw.githubusercontent.com/user/repo/main/update_v1.xml",
    "1.0.1": "https://raw.githubusercontent.com/user/repo/main/update_v2.xml",
}

DEFAULT_XML = "https://raw.githubusercontent.com/user/repo/main/update.xml"

class OTAHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode()

        print("\n=== OTA REQUEST ===")
        print(body)

        data = urllib.parse.parse_qs(body)

        firmware = data.get("firmware", ["unknown"])[0]
        device = data.get("device", ["unknown"])[0]

        print("Firmware:", firmware)
        print("Device:", device)

        xml_url = OTA_MAP.get(firmware, DEFAULT_XML)

        print("Response:", xml_url)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        self.wfile.write(f"url={xml_url}".encode())

HTTPServer(("0.0.0.0", PORT), OTAHandler).serve_forever()
