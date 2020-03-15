from rel_path import *
from http.server import HTTPServer, SimpleHTTPRequestHandler

os.chdir(rootDir)
print('Running HTTP server on 0.0.0.0:8080')
httpd = HTTPServer(('', 8080), SimpleHTTPRequestHandler)
httpd.serve_forever()