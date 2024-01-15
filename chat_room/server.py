import socket, select

host = "192.168.1.217"
port = 12345

def read_message(client_socket):
    try:
        return client_socket.recv(1024)
    except:
        return False



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    try:
        server_sock.bind((host, port))    
        server_sock.listen()
        print(f"Listening on {host}:{port}")
        sockets_list = [server_sock]
        clients = {}
        while True:
            read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
            for notified_sock in read_sockets:
                if notified_sock == server_sock:
                    client_sock, addr = server_sock.accept()
                    usr = read_message(client_sock)
                    if usr is False: 
                        continue
                    clients[client_sock] = usr
                    sockets_list.append(client_sock)
                    print(f"Accepted new connection from {client_sock}:{addr}, username = " + usr.decode("utf-8"))
                else:
                    message = read_message(notified_sock)
                    if message is False or message.decode("utf-8") == "done":
                        print("Closed connection from " + clients[notified_sock].decode("utf-8"))
                        sockets_list.remove(notified_sock)
                        del clients[notified_sock]
                    else:
                        usr = clients[notified_sock]
                        print(f"Recieved message from {usr}: " + message.decode("utf-8"))
                        #Now broadcast
                        for client_sock in clients:
                            #if client_sock != notified_sock:
                            client_sock.sendall(usr + b": " + message)
            for notified_sock in exception_sockets:
                sockets_list.remove(notified_sock)
                del clients[notified_sock]
    except KeyboardInterrupt:
        print("Keyboard interrupt")
