import socket, time, sys
import threading
import pprint
import rsa
from Crypto.PublicKey import RSA

clientCount = 0


def keygen():
    k = RSA.generate(1024)
    pk = k.publickey()
    return pk
  
def encr(msg,key):
   return rsa.encrypt(msg,key) 
   
def decr(msg,key):
      return rsa.decrypt(msg,key)

def server_connection():
    TCP_IP = '' 
    TCP_PORT = 8888
    BUFFER_SIZE = 1024    

    class server():

        def __init__(self):
            self.CLIENTS = []        


        def startServer(self):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((TCP_IP,TCP_PORT))
                s.listen(10)
                while 1:
                    client_socket, addr = s.accept()
                    print ('Connected with ' + addr[0] + ':' + str(addr[1]))
                    global clientCount
                    clientCount = clientCount+1
                    print (clientCount)
                    # register client
                    self.CLIENTS.append(client_socket)
                    threading.Thread(target=self.welcomeNewClient, args=(client_socket,)).start()
                s.close()
            except socket.error as msg:
                print ('Could Not Start Server Thread. Error Code : ') #+ str(msg[0]) + ' Message ' + msg[1]
                sys.exit()


    #client handler :one of these loops is running for each thread/player   
        def welcomeNewClient(self, client_socket):
            #send public key to new client
            pk=keygen() 
            keysend = pk.exportKey("PEM")
            print(type(keysend))               
            client_socket.send(keysend)
            
            while 1:
                data = client_socket.recv(BUFFER_SIZE)
                if not data: 
                    break
                #print ('Data : ' + repr(data) + "\n")
                #data = data.decode("UTF-8")
                # broadcast
                for client in self.CLIENTS.values():
                    client.send(data)

            # the connection is closed: unregister
            self.CLIENTS.remove(client_socket)
            #client_socket.close() #do we close the socket when the program ends? or for ea client thead?

        def broadcast(self, message):
            for c in self.CLIENTS:
                (pubkey, privkey)=keygen()
                temp="Hello World"
                print(pubkey)
                c.send(temp.encode("utf-8"))           

        def _broadcast(self):        
            for sock in self.CLIENTS:           
                try :
                    self._send(sock)
                except socket.error:                
                    sock.close()  # closing the socket connection
                    self.CLIENTS.remove(sock)  # removing the socket from the active connections list

        def _send(self, sock):  
            # (pubkey, privkey)=keygen()
            temp="Hello World"
            # print(pubkey)
            sock.send(temp.encode("utf-8"))       
            
            
   
    s = server() #create new server listening for connections
    threading.Thread(target=s.startServer).start()

    while 1:       
        s._broadcast()
        #pprint.pprint(s.CLIENTS)
        print("No of connected clients are : " ,len(s.CLIENTS)) #print out the number of connected clients every 5s
        time.sleep(5) 


def client_connection():
    connected = False
    #connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    client_socket.connect((host,8888))
    connected = True

    while connected == True:
        #wait for server commands to do things, now we will just display things
        data = client_socket.recv(2048)        
        publickey = RSA.importKey(data)
        print(type(publickey))
        


t1 = threading.Thread(target=server_connection) 
t2 = threading.Thread(target=client_connection) 

t1.start() 
t2.start() 

t1.join()
t2.join() 




