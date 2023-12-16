import socket
import threading
import sys
import select
connection_close = "close"
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#takes the first argument as server address and second argument as port number
server_address=sys.argv[1]
server_port=int(sys.argv[2])
exit_event=threading.Event()
print(server_address,server_port)
try:
    client_socket.connect((server_address,server_port))
    message_received = client_socket.recv(2048).decode('utf-8')
    print("Message received from the server: {}".format(message_received))
    print("type'close' to exit")
except Exception as e:
    print("connection failed")
    sys.exit(1)  
# method to receive messages from server 
def receive_messages_from_server():
    while not exit_event.is_set():
        try:
            clist, _, _ = select.select([client_socket], [], [])
            if client_socket in clist:
                reply = client_socket.recv(2048).decode('utf-8')
            if reply:
                print("\nmessage received from Client  : {}".format(reply))
                if reply=="server wants to close the connection":
                    exit_event.set()
                    break
                    #sys.exit(0)
                if reply=="server is closing the connection":
                   exit_event.set()
                   break
                
        except (socket.error,Exception) as e:
            print("Server has closed the connection.")
            client_socket.close()
            break
            #sys.exit(1)  
    client_socket.close()
    #print("close")
    sys.exit(1)  
# method to send messages to clients
def send_messages_to_clients():
    try:
        while not exit_event.is_set():
            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
            if sys.stdin in rlist:
                msg = raw_input()
                client_socket.send(msg.encode('utf-8'))
                if msg.lower() == connection_close:
                    exit_event.set()
                    break
    except KeyboardInterrupt:
        print("closed")
        exit_event.set()
        
  
# creating threads for receiving and sending messages
thread_for_receiving = threading.Thread(target=receive_messages_from_server)
thread_to_send = threading.Thread(target=send_messages_to_clients)
#starting the threads
thread_for_receiving.start()
thread_to_send.start()

# Waiting to finish two threads 
thread_to_send.join()
thread_for_receiving.join()

# closing the thread
client_socket.close()
sys.exit(1)



