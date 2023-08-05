#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import posixpath
import socket
import socketserver
import sys
import urllib.parse
from functools import partial
from http.server import SimpleHTTPRequestHandler, HTTPServer
import qrcode


class ThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True


class RequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        if directory is None:
            directory = os.getcwd()
        self.directory = directory
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        CURSOR_UP_ONE = '\x1b[1A'
        ERASE_LINE = '\x1b[2K'

        sys.stdout.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format % args))
        sys.stdout.write(ERASE_LINE)
        sys.stdout.write(CURSOR_UP_ONE)

    def read(self, n=None):
        return ''

    def translate_path(self, path):
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        trailing_slash = path.rstrip().endswith('/')
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        path = posixpath.normpath(path)
        words = path.split('/')
        words = filter(None, words)
        path = self.directory
        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bind', '-b', default='', metavar='ADDRESS',
                        help='Specify alternate bind address '
                             '[default: all interfaces]')
    parser.add_argument('port', action='store',
                        default=8000, type=int,
                        nargs='?',
                        help='Specify alternate port [default: 8000]')
    parser.add_argument('--directory', '-d', default=os.getcwd(),
                        help='Specify alternative directory '
                             '[default:current directory]')

    parser.add_argument('--qr', action='store_true', help='show qrcode in terminal')

    args = parser.parse_args()
    handler_class = RequestHandler
    server_address = (args.bind, args.port)
    handler_class.protocol_version = "HTTP/1.0"
    handler_class = partial(handler_class,
                            directory=args.directory)
    host = socket.gethostbyname(socket.gethostname())
    if args.qr:
        qr = qrcode.QRCode()
        qr.add_data("http://{}:{}".format(host, args.port))
        qr.print_ascii(tty=True)

    with ThreadingHTTPServer(server_address, handler_class) as httpd:
        sa = httpd.socket.getsockname()
        serve_message = "Serving HTTP on {host} port {port} with directory:{directory} (http://{host}:{port}/) ..."
        print(serve_message.format(host=host, port=sa[1], directory=args.directory))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)


if __name__ == "__main__":
    main()
