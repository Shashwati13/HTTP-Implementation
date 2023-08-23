
from typing import BinaryIO
import socket
import os

def file_server(iface:str, port:int, use_udp:bool, fp:BinaryIO) -> None:
        if use_udp:
                UDP_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                UDP_socket.bind((iface,port))
                print("Hello, I am a server")
                file_from_client,address=UDP_socket.recvfrom(256)
                with open(fp.name,"bw") as file_pointer:
                        while(True):
                                if not file_from_client:
                                        break
                                else:
                                        file_pointer.write(file_from_client)
                        file_pointer.close()
                os._exit(1) 


        else:
                socket_server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
                socket_server.bind((iface,port))
                print("Hello, I am a server")
                socket_server.listen()
                connection,address=socket_server.accept() 
                with open (fp.name,"wb") as file_pointer:
                        while(1):
                                file_from_client=connection.recv(256)
                                if not file_from_client:
                                        break
                                else:
                                        file_pointer.write(file_from_client)
                                        
        
                        file_pointer.close()
                connection.close()
                

def file_client(host:str, port:int, use_udp:bool, fp:BinaryIO) -> None:
        if use_udp:
                UDP_client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                address=(socket.gethostbyname(host),port)
                print("Hello, I am a client")
                with open(fp.name,"rb") as file_pointer:
                        file_input=file_pointer.read(256)
                        while file_input:
                                UDP_client.sendto(file_input,address)
                                file_input=file_pointer.read(256)
                        file_pointer.close()
        else:
                socket_client=socket.socket()
                socket_client.connect((host,port)) 
                print("Hello, I am a client")
                with open(fp.name,"rb") as file_pointer:
                        file_input=file_pointer.read(256)
                        while file_input:
                                socket_client.send(file_input)
                                file_input=file_pointer.read(256)
        
                        file_pointer.close()
                socket_client.close()


