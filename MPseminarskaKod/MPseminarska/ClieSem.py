import socket,threading,pickle,struct,tkinter,pygame
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sl=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

pom=0
beat=500
m=0
i=0
cor=[]

class light_signal:
  def __init__(self,name,C,offset):
    self.name = name 
    self.color=name
    self.C = C 
    self.offset = offset 

    o1=3
    o2=100

    for i in range (0,8):
        C.create_oval(o1,offset+10,o2,offset+110,fill="grey")
        o1+=110
        o2+=110
    self.setColor()

  def setColor(self):
      
    self.Light1 = self.C.create_oval(3,self.offset+10,100,self.offset+110,fill=self.color)
    self.Light2 = self.C.create_oval(113,self.offset+10,210,self.offset+110,fill=self.color)
    self.Light3 = self.C.create_oval(223,self.offset+10,320,self.offset+110,fill=self.color)
    self.Light4 = self.C.create_oval(333,self.offset+10,430,self.offset+110,fill=self.color)
    self.Light5 = self.C.create_oval(443,self.offset+10,540,self.offset+110,fill=self.color)
    self.Light6 = self.C.create_oval(553,self.offset+10,650,self.offset+110,fill=self.color)
    self.Light7 = self.C.create_oval(663,self.offset+10,760,self.offset+110,fill=self.color)
    self.Light8 = self.C.create_oval(773,self.offset+10,870,self.offset+110,fill=self.color)
    
       

  def clearAll(self):
    self.C.delete(self.Light1)
    self.C.delete(self.Light2)
    self.C.delete(self.Light3)
    self.C.delete(self.Light4)
    self.C.delete(self.Light5)
    self.C.delete(self.Light6)
    self.C.delete(self.Light7)
    self.C.delete(self.Light8)
    
class light_intersection:
  def __init__(self,top):
    self.pom=1
    self.top = top # hold a window frame
    self.C = tkinter.Canvas(self.top, bg="white", height=470, width=880)
    self.light={} 
    self.light["red"] = light_signal("red",self.C,0)
    self.light["green"] = light_signal("green",self.C,110)
    self.light["blue"] = light_signal("blue",self.C,220)    
    self.light["yellow"] = light_signal("yellow",self.C,330) 
    
    self.C.pack()

    # Create a statemachine here

    self.C.after(0,self.timerExpire) #create first event in simulation
  def timerExpire(self) :
      global pom
      global i
      global beat
      if pom==1:
          self.function(i)
          i+=4
          if i>=len(A):
              i=0
          pom=0
      else:
          self.clear()
          pom=1
      self.C.after(beat, self.timerExpire)  #create next event in simulation execute after 5 seconds

          
  def function(self,i):
      global A
      if A[i]==1:
          self.light["red"] = light_signal("red",self.C,0)
      if A[i+1]==1:
          self.light["green"] = light_signal("green",self.C,110)
      if A[i+2]==1:
          self.light["blue"] = light_signal("blue",self.C,220)
      if A[i+3]==1:
          self.light["yellow"] = light_signal("yellow",self.C,330)
  def clear(self):
      self.light["red"].clearAll()
      self.light["green"].clearAll()
      self.light["blue"].clearAll()
      self.light["yellow"].clearAll()



s.bind(('127.0.0.1',54326))
sl.bind(('127.0.0.1',0))
print(sl.getsockname())
print(s.getsockname())
srv=('127.0.0.1',1060)
schemes={}

def stringToList(s):
    cornum=[]
    cor=s.split(",")
    for n in cor:
        cornum.append(int(n))
    return cornum

def recv_all(sock, length):
    data = ''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('socket closed %d bytes into a %d-byte message' % (len(data), length))
        data += more.decode('latin1')
    return data.encode('latin1')
def hear(sl):
    sl.listen(10)
    while True:
        sc,socketname=sl.accept()
        data=recv_all(sc, struct.unpack("!i", recv_all(sc, 4))[0]).decode('latin1')
        sc.sendall(struct.pack("!i", len(schemes[data][0]+"|"+schemes[data][1]))+(schemes[data][0]+"|"+schemes[data][1]).encode('latin1'))
        sc.close()

def stop(si,top):
    pygame.mixer.music.stop()
    si=light_intersection(top)
    

def player(B,naslov,b):
    global A
    A=B
    print(len(A))
    top = tkinter.Tk() # create a window frame
    si = light_intersection(top)# construct intersection
    pygame.mixer.init()      
    global beat
    beat=b
    pygame.mixer.music.load(naslov)
    pygame.mixer.music.play(loops=0)

    but=tkinter.Button(top, text="STOP",command=lambda:stop(si,top))
    but.pack()    
    top.mainloop() # start GUI

        
n=input("Enter number of entries\n")
for i in range(int(n)):
    ime=input("Enter name of song\n")
    text=input("Enter lightning scheme\n")
    beat=input("Enter beat\n")
    schemes[ime]=[]
    schemes[ime].append(text)
    schemes[ime].append(beat)
s.connect(srv)
# threading.Thread(target=hear, args=(sl,)).start()
t = threading.Thread(target=hear, args=(sl,))
t.start()
while True:
    command=input("Connect to server or search for text\n")
    if command=="connect":
        msg="connect|"+sl.getsockname()[0]+"|"+str(sl.getsockname()[1])
        s.sendall(struct.pack("!i", len(msg))+msg.encode('latin1'))
        schemes_keys = []
        for key in schemes.keys():
            schemes_keys.append(key)
        msg=pickle.dumps(schemes_keys)
        s.sendall(struct.pack("!i", len(msg))+msg)
        dat=recv_all(s, struct.unpack("!i", recv_all(s, 4))[0])
        print(dat.decode("latin1"))
        dat=recv_all(s, struct.unpack("!i", recv_all(s, 4))[0])
        print("Avalible songs: \n"+dat.decode("latin1"))
    elif command=="search":
        c=input("Enter title\n")
        if c in schemes.keys():
            cornum=stringToList(schemes[c][0])
            player(cornum,"audio/"+c+".mp3",int(schemes[c][1]))
        else:
            msg="search|"+c
            s.sendall(struct.pack("!i", len(msg))+msg.encode('latin1'))
            dat=recv_all(s, struct.unpack("!i", recv_all(s, 4))[0])
            d=dat.decode('latin1').split('|')
            if d[0]=="OK":
                if d[2]=="server":
                    print(d[1])
                    beat=int(d[3])
                    print(beat)
                    cornum=stringToList(d[1])              
                else:
                    sv=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    if d[1]=="0.0.0.0":
                       d[1]="127.0.0.1"
                    print(d[1], int(d[2]))
                    sv.connect((d[1],int(d[2])))
                    sv.send(struct.pack("!i", len(c))+c.encode('latin1'))
                    rez=recv_all(sv, struct.unpack("!i", recv_all(sv, 4))[0]).decode('latin1')
                    print(rez)
                    corbeat=rez.split('|')
                    sv.close()
                    cornum=stringToList(corbeat[0])
                    beat=corbeat[1]
                player(cornum,"audio/"+c+".mp3",beat)
                
            elif d[0]=="Error":
                print(d[1])
