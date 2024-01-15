import socket, select, errno, sys
import tkinter as tk
from threading import Thread
host = "192.168.1.217"
port = 12345

username = input("Username: ")


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((host, port))

client_socket.setblocking(False)

client_socket.sendall(username.encode("utf-8"))


def send(e):
    global message
    message = message_entry.get()
    if message and message != "":
        client_socket.sendall(message.encode("utf-8"))
        if message == "done":
            client_socket.close()
            sys.exit()
    message_entry.delete(0, tk.END)


def recieve():
    while True:
        try:
            while True:
                msg = client_socket.recv(1024)
                print(msg.decode("utf-8"))
                msg_list.insert(0, msg.decode("utf-8"))
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print(f"Reading error {str(e)}")
                client_socket.close()
                sys.exit()
            continue
        except Exception as e:
            print(f"Reading error {str(e)}")
            client_socket.close()
            sys.exit()

window = tk.Tk()
window.title(username)
window.geometry("500x300")

window.bind("<Return>", send)

msg_list = tk.Listbox()
message_entry = tk.Entry()

message_entry.pack()
msg_list.pack()

message = ""



recieve_thread = Thread(target = recieve)
recieve_thread.start()
window.mainloop()
