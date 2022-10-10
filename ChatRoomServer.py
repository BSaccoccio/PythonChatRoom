#UDP ChatRoom Server Program

import socket
import datetime

HOST = "127.0.0.1"
PORT = 1234

BUFFER_SIZE = 4096
userList = []



def connectUser(user):
    msg = ("%s #%s has connected to the chatroom" % (user[0], user[1]))
    print("[%s] %s" % (datetime.datetime.now(), msg))
    sendGlobal(userList[0], msg)


def disconnectUser(user):
    msg = ("%s #%s has disconnected from the chatroom" % (user[0], user[1]))
    print("[%s] %s" % (datetime.datetime.now(), msg))
    sendGlobal(userList[0], msg)



#Sends a message to a specific user
def sendDirect(fromUser, toUser, message):
    msg = ("%s #%s -> #%s: %s" % (fromUser[0], fromUser[1], toUser[0], toUser[1], message))
    print("[%s] %s" % (datetime.datetime.now(), msg))
    msg = bytes(msg, "utf-8")
    s.sendto(msg, (HOST, toUser[1]))


#sends a message to all users
def sendGlobal(fromUser, message):
    msg = ("%s #%s -> All: %s" % (fromUser[0], fromUser[1], message))
    print("[%s] %s" % (datetime.datetime.now(), msg))
    msg = bytes(msg, "utf-8")
    i = 1
    while (i < len(userList)):
        s.sendto(msg, (HOST, (userList[i])[1]))
        i = i + 1


def getUserFromPort(portnum):
    i = 0
    for u in userList:
            if (u[1] == int(portnum)):
                return userList[i]
            i = i + 1
    return -1


def listUsers():
    for u in userList:
        print("%s #%s" % (u[0], u[1]))
        

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print("[%s] Chatroom server started on http://%s:%s\n" % (datetime.datetime.now(), HOST, PORT))
    userList.append(['SERVER', PORT])
    
    while True:
        msg, source = s.recvfrom(BUFFER_SIZE)
        sourcePort = source[1]
        msg = msg.decode("utf-8")
        if (msg[0 : 1] != '/'):
            sendGlobal(getUserFromPort(sourcePort), msg)
            
        elif (msg.split(" ")[0] == "/connect"):
            userList.append([msg.split(" ")[1], sourcePort])
            connectUser(userList[len(userList)-1])

        elif (msg.split(" ")[0] == "/disconnect"):
            disconnectUser(userList.pop(userList.index([msg.split(" ")[1], sourcePort])))

        #elif (msg.split(" ")[0] == "/dm"):
        #    print("DM")
        #    m = msg.split(" ")
        #    m.remove[0]
        #    sendDirect(getUserFromPort(sourcePort), getUserFromPort(m[1]), m)
            
