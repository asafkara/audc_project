import time
from http.server import HTTPServer
from server import MyServer

HOSTNAME = 'localhost'
PORT = 8080


if __name__ == "__main__":
    httpserv = HTTPServer((HOSTNAME, PORT), MyServer)
    print("Server has been started http://%s:%s" % (HOSTNAME, PORT))
    try:
        httpserv.serve_forever()
    except KeyboardInterrupt:
        pass
    httpserv.server_close()
    print(time.asctime(), 'Server DOWN - %s:%s' % (HOSTNAME, PORT))
