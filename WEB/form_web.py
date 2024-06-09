# -*- coding: utf-8 -*-

import http.server
import json
import os
import threading
from urllib.parse import urlparse, parse_qs
import sys

class ConfigServer(http.server.BaseHTTPRequestHandler):
    
    def load_html_template(self):
        with open('WEB/form_template.html', 'r', encoding='utf-8') as file:
            return file.read()

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')  # Especificar la codificación UTF-8
            self.end_headers()
            config = self.load_config()
            saved_message = ''
            form_template = self.load_html_template()
            self.wfile.write(form_template.format(saved_message=saved_message, **config).encode())
        elif self.path == '/shutdown':
            self.send_response(200)
            self.end_headers()
            self.shutdown_server()
            self.wfile.write('Server shutting down...'.encode())
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_params = parse_qs(post_data)
            config = self.load_config()
            config.update({key: value[0] for key, value in post_params.items()})
            self.save_config(config)
            self.send_response(303)
            self.send_header('Location', '/shutdown')
            self.end_headers()
            self.send_saved_message()
            sys.exit(0)  # Salir del script después de guardar la configuración y apagar el servidor
        else:
            self.send_error(404)

    def load_config(self):
        config_path = 'Config/config.json'
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as config_file:  # Especificar la codificación UTF-8
                return json.load(config_file)
        return {
            "bot_token": "",
            "group_id": "",
            "bucleCalls": "",
            "url": "",
            "total_days": "",
            "sleeper": "",
            "restaurant_0": ""
        }

    def save_config(self, config):
        with open('Config/config.json', 'w', encoding='utf-8') as config_file:  # Especificar la codificación UTF-8
            json.dump(config, config_file, indent=4)

    def shutdown_server(self):
        self.server.shutdown()

    def send_saved_message(self):
        saved_message_script = ''
        self.wfile.write(saved_message_script.encode())

def run_server():
    server_address = ('', 777)
    httpd = http.server.HTTPServer(server_address, ConfigServer)
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
