from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import os
from requests import get, put
import urllib.parse
import json
def run(handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
class HttpGetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        def fname2html(fname, is_uploaded):
            background_color = "background-color: rgba(0, 200, 0, 0.25);" if is_uploaded else ""
            return f"""
                <li style="{background_color}" onclick="fetch('/upload', {{'method': 'POST', 'body': '{fname}'}})">
                    {fname}
                </li>
                """
        backup_dir = "Backup"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        uploaded_files = set(os.listdir(backup_dir))
        print("Uploaded files:", uploaded_files)
        print("Files in pdfs directory:", os.listdir("pdfs"))
        self.send_response(200)
        self.send_header("Content-type", 'text/html')
        self.end_headers()
        self.wfile.write("""
            <html>
                <head>
                    <title>File Upload</title>
                </head>
                <body>
                    <h1>Uploaded Files</h1>
                    <ul>
                      {files}
                    </ul>  
                </body>
            </html>
        """.format(files="\n".join(
            fname2html(fname, fname in uploaded_files) for fname in os.listdir("pdfs")
        )).encode())
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        fname = self.rfile.read(content_len).decode("utf-8")
        local_path = f"pdfs/{fname}"
        ya_path = f"Backup/{urllib.parse.quote(fname)}"
        resp = get(f"https://cloud-api.yandex.net/v1/disk/resources/upload?path={ya_path}",
                   headers={"Authorization": "OAuth y0_AgAAAAA32gRgAADLWwAAAAEdS9YfAABAb51YteBMca8MiBJ2ILVA5SUX3w"})
        if resp.status_code == 409:
            print(f"File {fname} already exists on Yandex Disk.")
            self.send_response(200)
            self.end_headers()
            return
        if resp.status_code != 200:
            print("Error getting upload URL:", resp.text)
            self.send_response(500)
            self.end_headers()
            return
        upload_url = json.loads(resp.text)["href"]
        print("Upload URL:", upload_url)
        with open(local_path, 'rb') as file:
            resp = put(upload_url, files={'file': (fname, file)})
        print("Upload response status code:", resp.status_code)
        if resp.status_code == 201:
            print(f"File {fname} uploaded successfully.")
        else:
            print(f"Failed to upload {fname}. Status code: {resp.status_code}")
        self.send_response(200)
        self.end_headers()
run(handler_class=HttpGetHandler)