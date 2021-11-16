#!/usr/bin/env python

"""
Python 3 webserver challenge.

This challenge is based on how web browsers handle origins. The solution 
requires you to force a `null` origin when sending a POST request. The 
webpage contents will provide the hints.

Solution:

var f = document.createElement('iframe');
f.src = '/';
f.sandbox = 'allow-scripts';
var r = document.getElementById('extra');

// Then go into the iframe and click the "Run Query" button

"""

import argparse
import http.server


_FLAG = 'flag{handy_trick_to_hide_your_c2}'
_STATIC_MAP = {
    '/': 'index.html',
    'index.html': 'index.html'
}


def send_bad_request(request_handler):
    request_handler.send_response(400)
    request_handler.send_header('Content-Type', 'text/plain; charset=utf-8')
    request_handler.end_headers()
    
    request_handler.wfile.write(bytes('Bad request sent.', 'utf-8'))
    return


def send_internal_error(request_handler):
    request_handler.send_response(500)
    request_handler.send_header('Content-Type', 'text/plain; charset=utf-8')
    request_handler.end_headers()

    request_handler.wfile.write(bytes('Encountered an internal error for this request.', 'utf-8'))
    return


def serve_static(request_handler, status: int, filepath: str, content_type: str = 'text/html; charset=utf-8'):
    try:
        fd = open(filepath, 'rb')
    except:
        send_internal_error(request_handler)
        return

    request_handler.send_response(status)
    request_handler.send_header('Content-Type', content_type)
    request_handler.end_headers()
    request_handler.wfile.write(fd.read())
    return


class ChallengeHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        normpath = self.path.split('?')[0]
        if normpath in _STATIC_MAP:
            serve_static(self, 200, _STATIC_MAP[normpath])
        else:
            serve_static(self, 404, '404.html')


    def do_POST(self):
        normpath = self.path.split('?')[0]
        if normpath == '/query':
            if 'Origin' in self.headers:
                if self.headers['Origin'].casefold() != 'null'.casefold():
                    self.send_response(403)
                    self.send_header('Content-Type', 'text/plain; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(bytes('HEY. I see this request is coming from {}. It has sent FAR too many requests.\n'.format(self.headers['Origin']), 'utf-8'))
                else:
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/plain; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(bytes('HEY.... Wait where did this request come from? Oh well. Here\'s the flag: {}\n'.format(_FLAG), 'utf-8'))
                return
            else:
                self.send_response(400)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(bytes('Received bad request, missing `Origin` header.\n', 'utf-8'))
                return
        else:
            send_bad_request(self)


    def do_OPTIONS(self):
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0', help='The address to bind this server to')
    parser.add_argument('--port', default=18810, type=int, help='The port to bind this server to')
    parsed_args = parser.parse_args()

    httpserver = http.server.HTTPServer((parsed_args.host, parsed_args.port), ChallengeHTTPRequestHandler)
    print('[+] Running server, listening at http://{}:{}'.format(parsed_args.host, parsed_args.port))

    try:
        httpserver.serve_forever()
    except KeyboardInterrupt:
        pass

    print('[-] Closing server.')
    httpserver.server_close()
    print('[-] Server closed.')

