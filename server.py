from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os

PORT = int(os.environ.get("PORT", 8000))

# mapping firmware → XML
OTA_MAP = {
    "00502001": "http://raw.githubusercontent.com/sar404/otaupdate/main/update.xml",
}

DEFAULT_XML = "http://raw.githubusercontent.com/sar404/otaupdate/main/update.xml"

class OTAHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode()

            print("\n=== OTA REQUEST ===")
            print(body)

            # parse POST data
            data = urllib.parse.parse_qs(body)

            firmware = data.get("firmware", ["unknown"])[0]
            device = data.get("device", ["unknown"])[0]

            print("Firmware:", firmware)
            print("Device:", device)

            # pilih XML
            xml_url = OTA_MAP.get(firmware, DEFAULT_XML)

            print("Selected XML:", xml_url)

            # response WAJIB format ini
            response = f"url={xml_url}"

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()

            self.wfile.write(response.encode())

        except Exception as e:
            print("ERROR:", str(e))
            self.send_response(500)
            self.end_headers()

HTTPServer(("0.0.0.0", PORT), OTAHandler).serve_forever()
