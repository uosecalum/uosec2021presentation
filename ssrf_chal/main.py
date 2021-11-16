#!/usr/bin/env python

"""
Python 3 webserver challenge.

This challenge is based on abusing SSRF. It will reject attempts to 
specify IP addresses (so folks can't just plug in 169.254.169.254) but 
still allow folks to enter domains that resolve to those endpoints.

Solution: find a DNS endpoint that'll resolve to the IMDS endpoint and grab 
creds to reach into the S3 bucket with the results.

"""

import argparse
import http.server
import re
import urllib.parse

import requests


_STATIC_MAP = {
    '/': 'index.html',
    'index.html': 'index.html'
}
_IP_PATTERN = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')


def allowed_endpoint(endpoint: str):
    print('Regex check')
    if re.search(_IP_PATTERN, endpoint) is not None:
        print('Matched IP')
        return False
    return True


def send_bad_request(request_handler, msg: str='Bad request sent.'):
    request_handler.send_response(400)
    request_handler.send_header('Content-Type', 'text/plain; charset=utf-8')
    request_handler.end_headers()
    
    request_handler.wfile.write(bytes(msg, 'utf-8'))
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
        if normpath == '/grabpage':
            # grab out endpoint to pull from
            querystrparts = self.path.split('?')
            if len(querystrparts) == 0:
                send_bad_request('Missing query-string?')
            elif len(querystrparts) == 1:
                send_bad_request('Missing query-string?')
            elif len(querystrparts) == 2:
                querystr = querystrparts[1]
            else:
                querystr = '?'.join(querystrparts[1:])


            if not querystr.startswith('endpoint='):
                send_bad_request(self, 'endpoint split: {}'.format(querystr))
                return
            endpoint = querystr.split('endpoint=')[-1]

            # parse and validate the endpoint
            try:
                parseresult = urllib.parse.urlparse(endpoint)
            except:
                send_bad_request(self, 'Failed to parse url: {}'.format(endpoint))
                return

            if parseresult.scheme not in ('http', 'https'):
                serve_static(self, 400, '400.html')
                return

            if parseresult.netloc == '':
                send_bad_request(self, 'Empty host in URL not allowed.')
                return

            if not allowed_endpoint(parseresult.netloc):
                serve_static(self, 403, '403.html')
                return

            
            try:
                resp = requests.get(endpoint)
            except:
                send_bad_request(self, 'Unable to retrieve URL: {}'.format(endpoint))
                return

            self.send_response(200)
            self.end_headers()
            self.wfile.write(resp.content)
            self.wfile.write(bytes('<!-- CLUE: Grab creds and poke at S3 bucket 670903390496-secrets -->', 'utf-8'))
            return
        else:
            send_bad_request(self, 'wrong path')
            return


    def do_OPTIONS(self):
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0', help='The address to bind this server to')
    parser.add_argument('--port', default=6193, type=int, help='The port to bind this server to')
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

