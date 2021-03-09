# Benjamin Dinh 915987386
# Jessica Wu 918374404
# ProxyServer.py

from socket import *
import sys
import re
import os
import time

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)

# Fill in start.
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpSerPort = 8888
serverip = sys.argv[1]
tcpSerSock.bind((serverip, tcpSerPort))
tcpSerSock.listen(5)
# Fill in end.

while 1:
    
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    # Fill in start.
    raw_message = tcpCliSock.recv(1024).decode()
    # Fill in end.
    print('raw message: ', raw_message)

    # Extract the filename from the given message
    path = raw_message.split()[1]
    print("path: ", path)
    filename = path[1:]
    if "Referer:" not in raw_message:
        hostn = filename.replace("www.", "", 1)
        filename = ""
    else:
        referer = re.search('Referer:(.+)\\r', raw_message)
        referer = referer.group(0)
        hostn = referer.split("/")[-1].replace("\r", "")
    print("Host Name: ", hostn)
    print("filename: ", filename)

    filetouse = "cache/" + hostn + path
    cache_path = "/".join(filetouse.split("/")[:-1])
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)

    print("cache file name", filetouse)
    start = time.time()
    try:
        # Check whether the file exist in the cache
        f = open(filetouse, "r")
        outputdata = f.read()
        # ProxyServer finds a cache hit and generates a response message

        tcpCliSock.send(outputdata)
        print('Read from cache')
        f.close()

    # Error handling for file not found in cache
    except IOError:
        print('Not in cache')

        # Create a socket on the proxyserver
        c = socket(AF_INET, SOCK_STREAM)

        try:
            # Connect to the socket to port 80
            c.connect((hostn, 80))
            # Create a temporary file on this socket and ask port 80 for the file requested by the client

            out_message = raw_message.replace(path, "http://" + hostn + "/" + filename)
            print("out message", out_message)
            fileobj = c.makefile('r', 0)
            fileobj.write(out_message)
            # Read the response into buffer

            buffer = fileobj.read()

            # Create a new file in the cache for the requested file.
            # Also send the response in the buffer to client socket and the corresponding file in the cache
            tmpFile = open(filetouse, "wb")
            tmpFile.write(buffer)
            tcpCliSock.send(buffer)
            tmpFile.close()

            # c.close()
        except Exception as e:
            print(str(e))
    else:
        # HTTP response message for file not found
        # Fill in start.
        # tcpCliSock.send("HTTP/1.0 404 Not Found\r\n")
        # tcpCliSock.send("Content-Type:text/html\r\n")
        # tcpCliSock.send("\r\n")
        print("404 Error")
        # Fill in end.
        # Close the client and the server sockets
    end = time.time()
    print ("Elapsed time: " + str(end-start))
    tcpCliSock.close()


# Fill in start.
if __name__ == '__main__':
    main()
# Fill in end.
