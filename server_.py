

import socket
from threading import Thread
import json


HOST = "127.0.0.1"
PORT = 65432
class Server :

    def __init__(self):
        self.clients = {}
        self.data = {}
        self.mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mysocket.bind((HOST, PORT))
        self.mysocket.listen()

    # this function is handel each client it receive data from client and broadcast it to other client connected to the server
    # using broadcast function
    # and we use dictionary to send multi type of data at the same time
    # and because we cant send dictionary we sent it like json data
    def handel(self, client, username):
        # why while loop because this function work in a thread we need to keep this thread working
        # to keep receiving and broadcasting
        # if we don't but while it will only work once
        while True :
            msg = client.recv(1024).decode()
            self.data['msg'] = msg
            self.data['user'] = username
            self.data['users'] = []
            for users in self.clients:
                self.data['users'] += [users]
            newdata = json.dumps(self.data)

            self.broadcast(newdata)
            if not msg :
                break


    def runServer(self):
        """
            inside this function we listen to each client to connect to server and put it inside a thread
            each clietn will work on single thread

        """
        while True:
            client , adress = self.mysocket.accept()
            userName = client.recv(1024).decode()

            self.clients[userName] = client
            print("clients: ",self.clients)
            self.broadcast(f"{userName} connected to the server\n")

            thread = Thread(target= self.handel, args= (client, userName))
            thread.start()



    # this function is broadcasting sented msg to each client
    def broadcast(self, msg):
        for user in self.clients:
            try:
                self.clients[user].sendall(msg.encode())
            except BrokenPipeError :
                pass



if __name__ == '__main__':
    server = Server()
    server.runServer()