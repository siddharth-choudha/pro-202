import socket
from threading import Thread


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000


server.bind((ip_address, port))
server.listen()

print("Server has started")
clients = []
list_of_clients = []
nicknames = []
def broadcast(message):
    for client, nickname in clients:
        try:
            client.send(message)
        except:
            
            remove_client((client, nickname))

def remove_client(client):
    clients.remove(client)
    nicknames.remove(client[1])

def clientthread(client, nickname):
    while True:
        try:
            message = client.recv(2048)
            if message:
               
                broadcast(f"{nickname}: {message}")
            else:
               
                remove_client((client, nickname))
                break
        except:
           
            remove_client((client, nickname))
            break


while True:
        conn, addr = server.accept()
        conn.send('NICKNAME'.encode('utf-8'))
        nickname = conn.recv(2048).decode('utf-8')
        list_of_clients.append(conn)
        nicknames.append(nickname)
        print (nickname +'connected!')
        new_thread = Thread(target= clientthread,args=(conn,nickname))
        new_thread.start()                                           