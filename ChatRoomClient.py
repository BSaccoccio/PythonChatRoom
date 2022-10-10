#UDP ChatRoom Client Program

import socket
import threading
import os
import sys

HOST = "127.0.0.1"
PORT = 1234

BUFFER_SIZE = 4096
username = ""

#Send messages to the server
def send(): 
    while True:
        msg = ""
        while (len(msg) <= 0):
            msg = input("You > ")
        if msg == "/quit":
            logout()
        #elif msg == "/users":
        #    getUserList()
        server.sendto(bytes(msg, "utf-8"), (HOST, PORT))

#Receive messages from the server
def receive():
    while True:
        msg = server.recvfrom(BUFFER_SIZE)
        print("\t >> " +  msg[0].decode("utf-8"))


#"Connects" the user to the chatroom
def login():
    getUser()
    server.sendto(bytes(("/connect %s" % username), "utf-8"), (HOST, PORT))
    print("\nType or '/quit' to exit.\n") # Type '/commands' to see a list of commands\n")

#"Disconnects" the user from the chatroom
def logout():
    print("\nGoodbye, %s!" % (username))
    server.sendto(bytes(("/disconnect %s" % username), "utf-8"), (HOST, PORT))
    #sys.exit(0)
    os._exit(0) 


#Prompt the user for a username
def getUser():
    global username
    while (len(username) <= 0) or ('#' in username):
        if '#' in username:
            print("Error! Usernames can not include the character '#'\n")
        username = input("Enter your username: ")
        if (len(username) <= 0):
            print("Error! Usernames can not be blank\n")


#Main
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
login()

sender = threading.Thread(target = send)
listener = threading.Thread(target = receive)

sender.start()
listener.start()
