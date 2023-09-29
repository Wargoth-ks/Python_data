import pathlib
import urllib.parse
import mimetypes
import json
import threading
import socket

from http.server import HTTPServer, BaseHTTPRequestHandler
from cryptography.fernet import Fernet
from datetime import datetime
from time import sleep

key = Fernet.generate_key()


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.send_html_file("front-init/index.html")
        elif pr_url.path == "/message.html":
            self.send_html_file("front-init/message.html")
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("front-init/error.html", 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())

    def do_POST(self):
        comm_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        encryption = Fernet(key)

        data = self.rfile.read(int(self.headers["Content-Length"]))
        encrypt_data = encryption.encrypt(data)
        comm_socket.sendto(encrypt_data, ("localhost", 8081))
        print(f"Message: {encrypt_data} was sending")

        self.send_response(301)
        self.send_header("Location", "/")
        self.end_headers()


def data_json(data):
    with open("front-init/storage/data.json", "a+", encoding="utf-8") as mes:
        json.dump(data, mes, ensure_ascii=True, indent=4)


def web_server(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ("", 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


def socket_server():
    now = datetime.now()
    encryption = Fernet(key)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("localhost", 8081))
        s.setblocking(True)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            while True:
                data, addr = s.recvfrom(1024)
                if not data:
                    print("No received data")
                    break
                print(f"Received data: {data} from: {addr}")
                decrypted_data = encryption.decrypt(data)
                data_parse = urllib.parse.unquote_plus(decrypted_data.decode())
                print(data_parse)
                data_dict = {
                    f"{now}": {
                        key: value
                        for key, value in [
                            el.split("=") for el in data_parse.split("&")
                        ]
                    }
                }
                print(data_dict)
                data_json(data_dict)

        except KeyboardInterrupt:
            print(f"Destroy server")
        finally:
            s.close()


if __name__ == "__main__":
    web = threading.Thread(target=web_server)
    sock = threading.Thread(target=socket_server)

    sock.start()
    print(f"{sock} is starting ...")
    sleep(3)
    web.start()
    print(f"{web} is starting ...")
    sock.join()
    web.join()

    print("Done!")
