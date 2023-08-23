import socket
import threading
import time
import os
def chat_server(iface:str, port:int, use_udp:bool) -> None:
    
    if use_udp:
        UDP_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDP_socket.bind((iface,port))
        print("Hello, I am a server")

        while(1):
            msg,address=UDP_socket.recvfrom(256)
            print("got message from",address)
            msg=msg.decode('utf-8')
            minn=min(255,len(msg))
            msg=msg[:minn]

            if msg =='hello': 
                send_resp='world'
                UDP_socket.sendto(send_resp.encode('utf-8'),address)
            elif msg=='exit':
                send_resp='ok'
                UDP_socket.sendto(send_resp.encode('utf-8'),address)
                break
            elif msg=='goodbye':
                send_resp='farewell'
                UDP_socket.sendto(send_resp.encode('utf-8'),address)
            else:
                send_resp=msg
                UDP_socket.sendto(send_resp.encode('utf-8'),address)

    else:
            socket_server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            socket_server.bind((iface,port))
            print("Hello, I am a server")
            #print("Server is listing on port",port)
            socket_server.listen()
            count=0
            while True:
                stop_threads=False
                connection,address=socket_server.accept()
                print("Connection",count," from the client",str(address))
                print("got message from",address)
                thread_st=threading.Thread(target=accept_clients,args=(connection,))
                thread_st.start()
                count=count+1
            


def chat_client(host:str, port:int, use_udp:bool) -> None:

    host=generate_ip(host,port,use_udp)
    host=str(host)

    if use_udp:
        UDP_client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        address=(host,port)
        print("Hello, I am a client")
        while True:
            message=input()
            minn=min(255,len(message))
            message=message[:minn]
            UDP_client.sendto(message.encode('utf-8'),address)
            reponse,address=UDP_client.recvfrom(256)
            response = reponse.decode('utf-8')
            print(response)
            if message=='exit':
                break
            if message=='goodbye':
                break
    else:
        socket_client=socket.socket()
        socket_client.connect((host,port)) 
        print("Hello, I am a client")
        while True:
            msg=input()
            minn=min(255,len(msg))
            msg=msg[:minn]
            socket_client.send(msg.encode('utf-8'))
            response=socket_client.recv(256).decode('utf-8')
            if response=='ok' and msg=='exit':
                print(response)
                break
            elif response=='ok' and msg=='ok':
                print(response)
            elif response=='farewell':
                print(response)
                break
            else:
                print(response)
        socket_client.close()

def generate_ip(host,port,use_udp):
    if use_udp:
        result = socket.getaddrinfo(host,port,family=socket.AF_UNSPEC,proto=socket.IPPROTO_UDP)
    else:
        result = socket.getaddrinfo(host,port,family=socket.AF_UNSPEC,proto=socket.IPPROTO_TCP)
        
    final_ip = ""
    for itr in result:
        if itr[0]==socket.AddressFamily.AF_INET:
            final_ip=itr[4][0]
            break
    return final_ip

def accept_clients(connection) -> None:
        while connection:
            data=connection.recv(256).decode('utf-8')
            #print(data)
            minn=min(255,len(data))
            data=data[:minn]
            if data=='goodbye':
                send_resp='farewell'
                connection.send(send_resp.encode('utf-8'))
                break
            elif data=='hello':
                send_resp='world'
                # connection.send(send_resp.encode())
            elif data=='exit':
                send_resp='ok'
                connection.send(send_resp.encode('utf-8'))
                connection.close()
                #stop_threads=True
                os._exit(1)      
            else:
                send_resp=data
            connection.send(send_resp.encode('utf-8'))

   
    
