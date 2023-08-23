from typing import BinaryIO
import socket
import os
import pickle


class Header:
    def __init__ (self,typeId,seqNo,msg):
        self.typeId=typeId
        self.seqNo=seqNo
        self.msg=msg


def stopandwait_server(iface:str, port:int, fp:BinaryIO) -> None:
    UDP_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDP_socket.bind((iface,port))
    print("Hello, I am a server")
    h1=Header(0,0,'')
    while 1:
        file_from_client,address=UDP_socket.recvfrom(2056)
        recievedDgram=pickle.loads(file_from_client)
        if len(recievedDgram.msg)==0 or not recievedDgram.msg :
            break
        if recievedDgram.typeId==2:
            if recievedDgram.seqNo!=0:
                h1.typeId=1
                h1.seqNo=recievedDgram.seqNo
                sendDgram=pickle.dumps(h1,pickle.DEFAULT_PROTOCOL)
                UDP_socket.sendto(sendDgram,address)
            else:
                h1.typeId=1
                h1.seqNo=recievedDgram.seqNo
                sendDgram=pickle.dumps(h1,pickle.DEFAULT_PROTOCOL)
                UDP_socket.sendto(sendDgram,address)
                if recievedDgram.seqNo==1:
                    recievedDgram.seqNo=0
                else:
                    recievedDgram.seqNo=1
                if not recievedDgram.msg or len(recievedDgram.msg)==0 :
                    break
                else:
                    fp.write(recievedDgram.msg)

def stopandwait_client(host:str, port:int, fp:BinaryIO) -> None:
    UDP_client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    address=(socket.gethostbyname(host),port)
    print("Hello, I am a client")
    typeId=2
    msg_send=fp.read(256)
    h=Header(typeId,0,msg_send)
    data_packet=pickle.dumps(h,protocol=pickle.DEFAULT_PROTOCOL)
    while msg_send:
        UDP_client.sendto(data_packet,address)
        UDP_client.settimeout(0.5)   #Course wiki mentioned to set 0.5 sec RTT
        try:
            response,address=UDP_client.recvfrom(1024)
            UDP_client.settimeout(0) 
        except socket.timeout:
            continue
        responseMsg=pickle.loads(response)
        if responseMsg.typeId==1:
            if responseMsg.seqNo==0:
                responseMsg.seqNo=1
            else:
                responseMsg.seqNo=0
            msg_send=fp.read(256)
            typeId=2
            h=Header(typeId,0,msg_send)
            data_packet=pickle.dumps(h,protocol=pickle.DEFAULT_PROTOCOL)
        else:
            continue
    h=Header(typeId,0,bytes())
    data_packet=pickle.dumps(h,protocol=pickle.DEFAULT_PROTOCOL)
    UDP_client.sendto(data_packet,address)
    fp.close()



            
                



        



    
