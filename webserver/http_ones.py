import http.server
import socketserver

PORT = 1235
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer((''), Handler) as httpd:
    httpd.serve_forever()
