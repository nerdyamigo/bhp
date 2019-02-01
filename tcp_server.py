import socket 
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the server
server.bind((bind_ip, bind_port))

# listen on the server
# set maximum number of backlog connections = 5
# then we listen for connections to our server
server.listen(5)

print "[*] Listening on %s:%d" % (bind_ip, bind_port)

# this is ou client-handling thread
def handle_client(client_socket):
    # print out what the client sends
    request = client_socket.recv(1024)

    print "[*] Received: %s" % request

    # send back a packet
    client_socket.send("ACK!")

    client_socket.close()

# When a client connects we receive the clients socket into the client variable, and
# the remote connection details into the addr variable
while True:
    client, addr = server.accept()

    print "[*] Accepted connectio  from: %s: %d" % (addr[0], addr[1])

    # spin up our client thread to handle incoming data
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()
