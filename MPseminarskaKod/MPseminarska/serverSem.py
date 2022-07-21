import socket, pickle, threading, struct
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv=('127.0.0.1',1060)
s.bind(srv)
s.listen(5)

library={}
mylibrary={"Manca":["0,1,1,0,1,0,0,1","500"],"Ingilosi":["1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,1,1,1,1","300"],
           "all_in_you":["1,1,0,0,0,0,1,1,1,0,1,0,0,1,0,1,1,1,1,1","400"]}

l = threading.Lock()
def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele+"\n" 
    return str1
    
def recv_all(sock, length):
    data = ''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('socket closed %d bytes into a %d-byte message' % (len(data), length))
        data += more.decode('latin1')
    return data.encode('latin1')

def serve(sc,socketname):
    while True:
        data=recv_all(sc, struct.unpack("!i", recv_all(sc, 4))[0])
        zb=data.decode('latin1').split('|')
        if zb[0]=="connect":
            print("Client ",socketname," requesting to connect")
            length = struct.unpack("!i", recv_all(sc, 4))
            print(length)
            data=recv_all(sc, length[0])
            datal=pickle.loads(data)
            with l:
                for i in datal:
                    if i not in library:
                        library[i]=(zb[1],zb[2]);
            sc.sendall(struct.pack("!i", len("Connection OK, list accepted"))+"Connection OK, list accepted".encode('latin1'))
            avalibility= listToString(library.keys())+listToString(mylibrary.keys())
            sc.sendall(struct.pack("!i", len(avalibility))+avalibility.encode('latin1'))
            print("connection with client ",socketname," successfully completed")
        elif zb[0]=="search":
            with l:
                if zb[1] in mylibrary:
                    print(zb[1],"is found at server side")
                    msg="OK|"+mylibrary[zb[1]][0]+"|server|"+mylibrary[zb[1]][1]
                    sc.sendall(struct.pack("!i", len(msg))+msg.encode('latin1'))
                if zb[1] in library:
                    print(zb[1],"is found at ",library[zb[1]])
                    msg="OK|"+library[zb[1]][0]+"|"+library[zb[1]][1]
                    sc.sendall(struct.pack("!i", len(msg))+msg.encode('latin1'))
                else:
                    msg="Error|No such entry in player"
                    sc.sendall(struct.pack("!i", len(msg))+msg.encode('latin1'))

while True:
    sc,socketname=s.accept()
    t = threading.Thread(target=serve, args=(sc,socketname,))
    t.start()

