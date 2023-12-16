import sys
import socket 
import threading
buffer_size = 2048
connection_close = "close"
active_clients = []
# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address=socket.gethostbyname("linprog.cs.fsu.edu")
# binding the socket to the host
sock.bind((ip_address, 0))
assigned_port=sock.getsockname()[1]
print("enter ctrl+c to terminate")
print(ip_address,assigned_port)
exit_flag=False
#method to handle mutiple connections at a time
def mul_clients(client_socket, client_address):
    while True:
        try:
            msg = client_socket.recv(2048).decode('utf-8')
            if not msg:
                break
            if msg == connection_close:
                print("client{} wants to close the connection".format(client_socket.getpeername()))
                client_socket.send("server is closing the connection".encode('utf-8'))
                active_clients.remove(client_socket)
                print("total number of active clients are {}".format(len(active_clients)))
                break

            else:
                print("{}{}".format(client_address, msg))
                for client in active_clients:
                    # print(client)
                    # print(client_socket)
                    if client != client_socket:
                        msg_a = "{}:{}".format(client_socket.getpeername(),msg)
                        client.send(msg_a.encode('utf-8'))

        except (socket.error, KeyboardInterrupt) as e:
            # Handle disconnection, possibly remove the client from the list
            print("Connection closed by {} due to {}".format(client_socket,e))          
            active_clients.remove(client_socket)
            
            client_socket.close()

    client_socket.close()
# listening to the clients given 5 clients
def process():
    global exit_flag
    sock.listen(10)
# accepting the clients
    while True:
       try:
           client_socket, client_address = sock.accept()
           print("connection established from {}".format(client_address))
           active_clients.append(client_socket)
           client_socket.send("welcome to the server".encode('utf-8'))
           x = threading.Thread(target=mul_clients, args=(client_socket, client_address))
           x.start()
           print("the number active connections{} ".format(len(active_clients)))
       except(socket.error, KeyboardInterrupt) as e:
           #print(active_clients)
           break
    for clients in active_clients[:]:
        
        #print(clients)
        clients.send("server wants to close the connection".encode('utf-8'))
        active_clients.remove(clients)
        clients.close()  
        print("total number of active clients{}".format(len(active_clients)))  

       
        
    print("terminated") 
    # closing the socket    
    sock.close()
    sys.exit(1)
#calling the function
process()
        
   
