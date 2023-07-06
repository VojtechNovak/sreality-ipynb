from http.server import BaseHTTPRequestHandler, HTTPServer
import psycopg2


class RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self._set_response()
            self.wfile.write('<html><body>'.encode('utf-8'))
            self.wfile.write('<h1>Sreality Ads</h1>'.encode('utf-8'))

            conn = psycopg2.connect(host='localhost',
                                    port = '5432',
                                    user = 'postgres',
                                    password = '159357lol',
                                    dbname = 'postgres')
            cur = conn.cursor()
            cur.execute('SELECT id, velikost, lokace FROM sreality LIMIT 500')
            ads = cur.fetchall()

            self.wfile.write('<table>'.encode('utf-8'))
            self.wfile.write('<tr>'.encode('utf-8'))
            self.wfile.write('<th>ID</th>'.encode('utf-8'))
            self.wfile.write('<th>Velikost</th>'.encode('utf-8'))
            self.wfile.write('<th>Lokace</th>'.encode('utf-8'))
            self.wfile.write('</tr>'.encode('utf-8'))

            for ad in ads:
                id, velikost, lokace = ad
                self.wfile.write('<tr>'.encode('utf-8'))
                self.wfile.write(f'<td>{id}</td>'.encode('utf-8'))
                self.wfile.write(f'<td>{velikost}</td>'.encode('utf-8'))
                self.wfile.write(f'<td>{lokace}</td>'.encode('utf-8'))
                self.wfile.write('</tr>'.encode('utf-8'))

            self.wfile.write('</table>'.encode('utf-8'))

            cur.close()
            conn.close()

            self.wfile.write('</body></html>'.encode('utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><body><h1>Page not found</h1></body></html>'.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
