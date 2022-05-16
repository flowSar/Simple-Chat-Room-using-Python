import socket
from tkinter import *
import socket as st
from threading import Thread


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

import json

class Client (Tk):

    def __init__(self):
        super().__init__()

        self.geometry("550x590")


        top_frame = Frame(self)
        top_frame.grid(row = 0 , column = 0, pady = (10,10))
        self.userName = StringVar()
        self.username_entry = Entry(top_frame, textvariable = self.userName)
        self.username_entry.grid(row = 0, column = 0, padx = (10, 10))

        self.btn_connect = Button(top_frame, text = "connect", command = self.connect)
        self.btn_connect.grid(row = 0, column = 1)


        host_label = Label(top_frame, text = "Host")
        host_label.grid(row = 1, column = 0, padx = (5, 5), pady = (5, 5))

        self.host_label_value = Label(top_frame, text = "")
        self.host_label_value.grid(row = 1, column = 1)

        self.host = StringVar()

        self.host_entry = Entry(top_frame, textvariable = self.host )
        self.host_entry.grid(row = 1, column = 1, padx = (5, 5), pady = (5, 5))
        self.host_entry.insert(END, "127.0.0.1")




        self.textScreen = Text(top_frame, width = 48, height = 26,background = "white", foreground = "blue")
        self.textScreen.grid(row = 2, column = 0, padx = (5,5), pady = (5,5), columnspan = 2)

        connected_user_frame = Frame(self, )
        connected_user_frame.grid(row = 0, column = 1, sticky = (N), pady = (10,0))
        connected_client_title = Label(connected_user_frame, text = "connected Users")
        connected_client_title.grid(row = 0, column = 0, sticky = (N), pady = (10,0))

        self.connected_user_names = Label(connected_user_frame, text = "")
        self.connected_user_names.grid(row = 1, column = 0)

        self.connected_client = []




        frame = Frame(self)
        frame.grid(row = 1 , column = 0)
        self.text_input = Text(frame, width = 39, height = 3, background = "#FEFBE7", foreground = "#251D3A")
        self.text_input.grid(row = 1, column = 0, padx = (5,5), pady = (5,5))

        send_btn = Button(frame, text = "Send", command = self.sendMsg)
        send_btn.grid(row = 1, column = 1)


        self.mysocket = None


        self.mainloop()

    # this function is for add all connected client to the screen
    def listenToConnctedClient(self, data):
        nm = ""
        for names in data['users']:
            nm += names +"\n"
        self.connected_user_names['text'] = nm

    def listenningToChange(self, sock):
        while True:
            data = sock.recv(1024).decode().strip()
            try :
                data = json.loads(data)
                self.chatRoom(data)
                self.listenToConnctedClient(data)

            except json.decoder.JSONDecodeError:

                self.textScreen.insert(END, data+"\n")
                self.textScreen.tag_add('gre', 'end-2c linestart', 'end-2c')
                self.textScreen.tag_configure('gre', background="yellow", foreground="green", justify = "center")

            if not data :
                break


    def chatRoom(self, data):
        try:
            if data['user'] == self.userName.get() :
                self.textScreen.insert(END, data['msg'], "orange_fg")
                # self.textScreen.tag_add('orange_fg', 'end-2c linestart', 'end-2c')
                self.textScreen.tag_configure('orange_fg', background="orange", foreground="white", justify = "right")
            else:
                self.textScreen.insert(END, data['user']+" : "+data['msg'],'green_fg')
                self.textScreen.tag_configure('green_fg', background="green", foreground="white")
        except KeyError:
            pass

    def sendMsg(self):
        self.mysocket.sendall(self.text_input.get('1.0', END).encode())
        self.text_input.delete('1.0', END)


    def connect(self):
        self.mysocket = st.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mysocket.connect((self.host.get(), PORT))
        userName = self.userName.get()
        self.mysocket.sendall(userName.encode())
        data = self.mysocket.recv(1024).decode()
        self.textScreen.insert(END, data, 'co')
        self.textScreen.tag_configure('co', background="yellow", foreground="green", justify = "center")
        self.text_input.delete('1.0', END)
        self.btn_connect.destroy()
        self.username_entry.destroy()
        self.host_label_value['text'] = self.host.get()
        self.host_entry.destroy()
        thread = Thread(target=self.listenningToChange, args= (self.mysocket,))
        thread.start()




if __name__ == '__main__':
    Client()
    # Login()
