import proxy
def main():
    s = proxy.StartServer()
    while True:
        print("Listening on host: {0} and port: {1}".format(proxy.HOST,proxy.PORT))
        conn,addr = s.accept()
        request = conn.recv(1024)
        if len(request) > 0:
            data = request.decode("utf-8","ignore")
            serverinfo = data.split()[1]
            print("Accepted")
            print("Method:",data.split()[0])
            print(data,sep = '\n')
            #create multi thread to handle multi request at the same time
            t = proxy.threading.Thread(target = proxy.operation,args = (conn,addr,data,serverinfo,request))
            t.start()
    s.close()
if __name__ == "__main__":
    main()