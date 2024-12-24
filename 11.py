from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from requests import get, put
import urllib.parse
import json

# Запрос токена Яндекс Диска
yandex_token = input("Введите ваш токен Яндекс Диска: ")

def run(handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()

class HttpGetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/style.css':
            self.send_response(200)
            self.send_header("Content-type", 'text/css')
            self.end_headers()
            with open('style.css', 'rb') as f:
                self.wfile.write(f.read())
            return

        def fname2html(fname, is_uploaded):
            background_color = "background-color: rgba(0, 200, 0, 0.25);" if is_uploaded else ""
            return f"""
                <li style="{background_color}" onclick="fetch('/upload', {{'method': 'POST', 'body': '{fname}'}})">
                    {fname}
                </li>
                """

        ya_disk_files = set()
        try:
            resp = get("https://cloud-api.yandex.net/v1/disk/resources?path=Backup",
                       headers={"Authorization": f"OAuth {yandex_token}"})
            if resp.status_code == 200:
                files_data = json.loads(resp.text)
                if '_embedded' in files_data and 'items' in files_data['_embedded']:
                    ya_disk_files = {urllib.parse.unquote(item['name']) for item in files_data['_embedded']['items']}
        except Exception as e:
            print("Ошибка при получении списка файлов с Яндекс.Диска:", e)

        print("Файлы на Яндекс.Диске:", ya_disk_files)
        print("Файлы в папке pdfs:", os.listdir("pdfs"))

        self.send_response(200)
        self.send_header("Content-type", 'text/html')
        self.end_headers()
        self.wfile.write(f"""
            <html>
                <head>
                    <title>Downloads files</title>
                    <link rel="stylesheet" type="text/css" href="/style.css">
                </head>
                <body>
                    <h1>Downloads files</h1>
                    <ul>
                      {''.join(
            fname2html(fname, fname in ya_disk_files) for fname in os.listdir("pdfs")
        )}
                    </ul>
                </body>
            </html>
        """.encode())

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        fname = self.rfile.read(content_len).decode("utf-8")
        local_path = f"pdfs/{fname}"
        ya_path = f"Backup/{urllib.parse.quote(fname)}"

        resp = get(f"https://cloud-api.yandex.net/v1/disk/resources/upload?path={ya_path}",
                   headers={"Authorization": f"OAuth {yandex_token}"})

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