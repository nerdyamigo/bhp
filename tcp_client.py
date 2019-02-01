import socket

target_host = "0.0.0.0"
target_port = 9999

# create the socket object
# First we create a socket object with the AF_INET and SOCK_STREAM
# params, the AF_INET param is saying we are going to use a standard IPv4 address
# pr hostname and SOCK_STREAM indicated that this will be a TCP
# client.We then connect the client to the server(next step)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the client
# We are going to connect using the connect function, we pass it the host name and
# port number

client.connect((target_host, target_port))

# send some data
# We are simply sending data to the host through the port we specified

client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

# receive the data back
response = client.recv(4096)
# response 
print response

