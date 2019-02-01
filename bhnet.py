#!/usr/bin/python

import sys 
import socket
import getopt
import threading
import subprocess

# deinfe some globals here
# nothing too hard here just setting some flags

listen              = False
command             = False
upload              = False
execute             = ""
target              = ""
upload_destination  = ""
port                = 0

# function responsible for handling command line arguments and calling
# the rest of our functions
def usage():
    print "BHP Network Tool"
    print
    print "Usage: bhnet.py -t [target_host] -p [port_number]"
    print "-l --listen                  - listen on [host]:[port] for incoming connections"
    print "-e --execute=file_to_run     - execute the given file upon receiving a connection"
    print "-c --command                 - initialize a command shell"
    print "-u --upload=destination      - upon receiving connection upload a file and write to [destination]"
    print
    print
    print "Example: "
    print "bhnet.py -t 192.168.0.1 -p 5555 -l -c"
    print "bhnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print "bhnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHIJ' | ./netcat_pirata.py -t 192.168.11.12 -p 135"
    sys.exit(0)

# implementation for the features we are building our fake netcat with
def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socekt.SOCK_STREAM)
    try:
        # lets try to connect to our target host
        client.connect((target,port))

        if len(buffer):
            client.send(buffer)
        while True:
            # now lets wait for data to com back to us
            recv_len = 1
            response = ""

            while recv_len:

                data    = client.recv(4096)
                rcv_len = len(data)
                reponse+= data

                if rcv_len < 4096:
                    break

            print response, 

            # wait for more input
            buffer = raw_input("")
            buffer += "\n"

            # lets send our data off
            client.send(buffer)

    except:
        print "[*] Exception! Exiting..."
        # tear down the connection
        client.close()

def server_loop():
    global target

    # if no target is defined we listen on all interfaces
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # spin off a thread to handle pur new client
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def run_command(command):

    # trim the newline
    command = command.strip()

    # run the command and get the output back
    try:
        
        # subprocess library is being used here
        # provides a powerful process-creation 
        # interface that gives you a number of 
        # ways to start and interact with client programs
        # here we are just running the command passed down
        # and returning the output
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)

    except: 

        output = "Failed to execute command.\r\n"

    # send the output back to the client
    return output

# implement the logic to do file uploads, command execution and or shell
def client_handler(client_socket):
    global upload
    global execute
    global command

    # check for upload
    if len(upload_destination):

        # read in all the bytes and write to our own destination
        file_buffer = ""

        # keep reading data until there is none available

        while True:
            data = client_socket.recv(1024)

            if not data: 
                break
            else: 
                file_buffer += data
            # take these bytes and try to write them out
            try:
                file_descriptor = open(upload_destination, "wb")
                file_descriptor.wite(file_buffer)
                file_descriptor.close()

                # acknowledge that we wrote the file out
                client_socket.send("Successfully daves file to %s\r\n" % upload_destination)
            except: 
                client_socket.send("Failed to save file to %s\r\n" % upload_destination)

            # check for command execution

            if len(execute):

                # run the command
                output = run_command(command)
                client.socket.send(output)

                # now we go into another loop if a comman shell was requested

                if command:

                    while True: 
                        # show a simple prompt
                        client_socket.send("NETCATpirata:#> ")
                            
                        # we receive until we see a linefeed
                        cmd_buffer = ""
                        while "\n" not in cmd_buffer:
                            cmd_buffer += client.socket.recv(1024)

                        # send back the command output
                        response = run_command(cmd_buffer)

                        # send back the response
                        client_socket.send(response)

def main():
    global listen
    global port
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # read the command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "target", "port","command","upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
    for o,a in opts: 
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--list"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

        # are we going to listen or jsut send data from stdin?
        if not listen and len(target) and port > 0:

            # read in the buffer from the commandline
            # this will block, so send crl-d if not the sending input
            # to stdin

            buffer = sys.stdin.read()

            # send the data off
            client_sender(buffer)
        # we are going to listern and potentially
        # upload things, execute commands, and drop a shell back
        # depending on our command line options above
        if listen:
            server_loop()
main()

