import socket
import threading
import time
import os.path
HOST = "127.0.0.1"
PORT = 8888
#Create a server socket
def StartServer():  
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen(10)
    return s
#Get the data from cache
def GetCache(filename):
    #path to the cache file
    path = os.path.join(os.getcwd(),"Cache",filename + ".cache")
    with open(path,'rb') as reader:
        data = reader.read()
        return data
#Send received data back to the client and save it to cache
def SaveCacheAndRespondToClient(filename,host,port,conn,request):
    s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s1.connect((host,port))
    s1.sendall(request)
    path = os.path.join(os.getcwd(),"Cache",filename + ".cache")
    with open(path,'wb') as writter:
        while True:
            data = s1.recv(1024)
            if len(data) > 0:
                conn.sendall(data)
                writter.write(data)
            else:
                break
    s1.close()
#Check the validity of char
def IsValidChar(chr):
    if chr == '/' or chr == '\\' or chr == ':' or chr == ' ':
        return False
    elif chr == '*' or chr == '.' or chr == '-' or chr == '?' or chr == '"':
        return False
    return True
#Get the list of blacklist domain
def ReadBlackList():
    with open("BlackList.cfg",'r') as reader:
        BlackList = reader.read().splitlines()
        return BlackList
def PostMethod(host,port,conn,request):
    NewSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    NewSocket.connect((host,port))
    NewSocket.sendall(request)
    while True:
        data = NewSocket.recv(1024)
        if len(data) > 0:
            conn.sendall(data)
        else:
            break
#Check if the cache file is time out
def IsTimeOut(filename):
    path = os.path.join(os.getcwd(),"Cache",filename + ".cache")
    return time.time() - os.path.getmtime(path) > 10*60
def GetMethod(host,port,conn,request,serverinfo):
    filename = ""
    #Replace the invalid characters
    for i in serverinfo:
        if not (IsValidChar(i)):
            i = '_'
        filename = filename + i
    if os.path.isfile(os.path.join(os.getcwd(),"Cache",filename + ".cache")) and not IsTimeOut(filename):
        data = GetCache(filename)
        conn.sendall(data)
    else:
        SaveCacheAndRespondToClient(filename,host,port,conn,request)
def operation(conn,addr,data,serverinfo,request):
    host,port = "",0
    BlackList = ReadBlackList()
    port = 80
    #Starting from 7 to cut off the "http://" part
    host = serverinfo[7:serverinfo.find('/',7)]
    for i in BlackList:
        #if the domain is in blacklist, send the 403 status code back to client
        if i in host:
            message = "403 Forbidden\nYOU ARE NOT ABLE TO ACCESS THIS SITE"
            conn.sendall(message.encode())
            conn.close()
            return None
    if data.find("GET") != -1:
        GetMethod(host,port,conn,request,serverinfo)
    elif data.find("POST") != -1:
        PostMethod(host,port,conn,request)
    conn.close()
    print("\n\n")