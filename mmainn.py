from datetime import datetime
from socket import *  # import socket

serverPort = 6500  # initialize port number to 6500
try:
    # AF_INET is the address family (the network is using IPv4), and sock_stream means oriented connection
    serverSocket = socket(AF_INET, SOCK_STREAM)
    print("--- Socket created! ---")
except:
    # associate the socket with host name and port number
    print("--- Creation Socket Failed! ---")
# bind assigns the port number to the server's socket
serverSocket.bind(("", serverPort))
serverSocket.listen(1)  # enable the server to accept one connection

# *****************************************************************************************
while True:

    # getting the client socket object and address
    connection, address = serverSocket.accept()
    sentence = connection.recv(1024).decode(
        'utf-8')  # read data sent by the client
    print("--- The Server Connected With: ", address)
    print("--- Request: \n", sentence)  # print HTTP request message
    # address contains client IP address and socket number
    clientIp = address[0]
    clientPort = address[1]  # port number
    URL = sentence.split()[1]  # get request

 # ****************************************************************************************
 # check the request
    if (URL == "/" or URL == "/index.html"):  # html request
        connection.send("HTTP/1.1 200 OK\r\n".encode())
        print("HTTP/1.1 200 OK\r\n")
        connection.send("Content-Type: text/html \r\n".encode())
        print("Content-Type: text/html \r\n")
        date = datetime.now()  # to send date & time with the response
        print("Date and Time: " + date.strftime("%d/%m/%Y, %H:%M:%S") + "\r\n")
        connection.send("\r\n".encode())  # carriage return, line feed
        mainfile = open("index.html")  # open index.html
        data = mainfile.read().replace('\n', '')
        connection.send(data.encode())
        mainfile.close()

 # ****************************************************************************************

    elif (URL == "/styles.css"):  # css request
        connection.send("HTTP/1.1 200 OK\r\n".encode())
        print("HTTP/1.1 200 OK\r\n")
        connection.send("Content-Type: text/css \r\n".encode())
        print("Content-Type: text/html \r\n")
        date = datetime.now()  # to send date & time with the response
        print("Date and Time: " + date.strftime("%d/%m/%Y, %H:%M:%S") + "\r\n")
        connection.send("\r\n".encode())  # carriage return, line feed
        cssfile = open("styles.css")
        data = cssfile.read().replace('\n', '')
        connection.send(data.encode())
        cssfile.close()

 # ****************************************************************************************

    # this code for get pictures in interface
    elif (URL == "/picture.png"):  # png request
        Image = open("picture.png", "rb")
        connection.send("HTTP/1.1 200 OK\r\n".encode())
        print("HTTP/1.1 200 OK\r\n")
        connection.send("Content-Type: image/png \r\n".encode())
        print("Content-Type: image/png \r\n")
        date = datetime.now()  # to send date & time with the response
        print("Date and Time: " + date.strftime("%d/%m/%Y, %H:%M:%S") + "\r\n")
        connection.send("\r\n".encode())  # carriage return, line feed
        connection.send(Image.read())

 # ****************************************************************************************

    elif (URL == "/cup.jpg"):  # jpg request
        Image = open("cup.jpg", "rb")
        connection.send("HTTP/1.1 200 OK\r\n".encode())
        print("HTTP/1.1 200 OK\r\n")
        connection.send("Content-Type: image/jpg \r\n".encode())
        print("Content-Type: image/jpg \r\n")
        date = datetime.now()  # to send date & time with the response
        print("Date and Time: " + date.strftime("%d/%m/%Y, %H:%M:%S") + "\r\n")
        connection.send("\r\n".encode())  # carriage return, line feed
        connection.send(Image.read())

 # ****************************************************************************************

    elif (URL == "/SortByName"):
        sortfile = open("Books.txt", "r")
        byname = sortfile.read().splitlines()
        sortfile.close()
        byname.sort()  # sort based on names

        connection.send("HTTP/1.1 200 OK\r\n".encode())
        connection.send("Content-Type: text/html; charset=utf-8\r\n".encode())
        connection.send("\r\n".encode())
        request = "<!DOCTYPE html><html><body><h1><font color=#b866c9>Names and prices of Books sorted by Name</font></h1><ol>"
        for i in byname:
          request += "<h2><li>" + str(i) + "$" + "</li></h2>"
        request += "</ol></body></html>"
        request += "\r\n"
        connection.sendall(request.encode())

 # ****************************************************************************************

    elif (URL == "/SortByPrice"):
        sortfile = open("Books.txt", "r")  # open file to read data
        price = sortfile.read().splitlines()
        sortfile.close()
        price.sort(key=lambda x: x.split(':')[1], reverse=True)
        connection.send("HTTP/1.1 200 OK\r\n".encode())
        connection.send("Content-Type: text/html; charset=utf-8\r\n".encode())
        connection.send("\r\n".encode())
        request = "<!DOCTYPE html><html><body><h1><font color=#b866c9>Names and prices of Books sorted by Price</font></h1><ol>"
        for i in price:
            request += "<h2><li>" + str(i) + "$" + "</li></h2>"
        request += "</ol></body></html>"
        request += "\r\n"
        connection.sendall(request.encode())

 # ****************************************************************************************

    else:
        connection.send("HTTP/1.1 200 OK\r\n".encode())
        connection.send("Content-Type: text/html; charset=utf-8\r\n".encode())
        connection.send("\r\n".encode())
        connection.send(("<!DOCTYPE html><html><title>ERROR</title><center><h1> HTTP/1.1 404 Not Found</h1></center>"
                         + "<h2><center><font color=Red> The File Is Not Found</font></center></h2>"
                         + "<h3><center><b>Zeina Odeh-1190083 | Nour Naji-1190270 | Rasha Dar Abu Zidan-1190547</b></center></h3>"
                         + "<h3><center>IP And Port Number Of The Client:"+str(clientIp)+", "+str(clientPort)+"</center></h3></html>") .encode())
    connection.close()
    print("Connection:Close")
