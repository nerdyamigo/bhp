import socket

target_host = "127.0.0.1"
target_port = 80
# creater a socket object
# We are usign the DGRAM socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send data
# Send data by calling sendto
# There is a connectionless protocol there is no connection() beforehand
client.sendto("AAABBBCCC", (target_host, target_port))

# receive some data
# We receive the data, returns both data & details from remote host and port 
data, addrr = client.recvfrom(4096)

print data
