import socket

import queue
# import thread module
from _thread import *
import threading

#queue = queue.Queue()
server_run = True

class RemoteQueueServer:
    def __init__(self,queue, port: int):
        self._queue = queue
        self._port = port


    def run(self):
        self._run = True
        self._thread = threading.Thread(target=self._run_remote_queue_server)

        self._thread.start()

    def stop(self):
        self._run = False

        self._thread.join(timeout=1.5)

    def _run_remote_queue_server(self):
        def handle_client(queue, socket):
            BUFFER_SIZE: int = 1024
            try:
                c, addr = socket.accept()
                with c:
                    data = c.recv(BUFFER_SIZE)
                    queue.put(data.decode("utf-8"))
            except:
                return


        HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
        socket.setdefaulttimeout(1)
        #PORT = port  # Port to listen on (non-privileged ports are > 1023)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, self._port))
            s.listen()
            print("socket is listening")
            while self._run:
                handle_client(self._queue,s)







