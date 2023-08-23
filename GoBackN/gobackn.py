
from typing import BinaryIO
import socket
import os
import pickle
from datetime import datetime

class Header:
    def __init__ (self,seqNo,msg):
        self.seqNo=seqNo
        self.msg=msg
      

def gbn_server(iface:str, port:int, fp:BinaryIO) -> None:
    UDP_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDP_socket.bind((iface,port))
    print("Hello, I am a server")
    recSeq=0
    buffer=bytearray()
    while 1:
        file_from_client,address=UDP_socket.recvfrom(2096)
        recievedDgram=pickle.loads(file_from_client)        #Unpickling the data recieved from the client
       # print(recievedDgram.msg)
        if recievedDgram.seqNo==recSeq:
            # print(len(recievedDgram.msg))
            if len(recievedDgram.msg)==0 or not recievedDgram.msg :
                # print("breaking")
                break
            buffer.extend(recievedDgram.msg)
            recSeq=recSeq+1
            h1=Header(recSeq,'ACK')
            sendDgram=pickle.dumps(h1,pickle.DEFAULT_PROTOCOL)
            UDP_socket.sendto(sendDgram,address)
        else:
            h1=Header(recSeq,'NAK')
            sendDgram=pickle.dumps(h1,pickle.DEFAULT_PROTOCOL)
            UDP_socket.sendto(sendDgram,address)
    fp.write(buffer)
    fp.close()



def gbn_client(host:str, port:int, fp:BinaryIO) -> None:
    UDP_client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    address=(socket.gethostbyname(host),port)
    print("Hello, I am a client")
    file_content=[]
    content=fp.read(1024)
    while content:
        file_content.append(content)
        content=fp.read(1024)
    #Added EOF for file 
    file_content.append(bytes())
    windowFrame=4
    sendSeq=0
    baseValue=0
    Flag=False
    j=0
    globalDateTimeout=datetime.utcnow()-datetime(1970,1,1)
    globalSecondsTimeout=(globalDateTimeout.total_seconds())
    globalmilli=round(globalSecondsTimeout*1000)

    while 1:
        if Flag:
            break

        for i in range(baseValue,min(baseValue+windowFrame,len(file_content))):
            msgSent=file_content[i] 
            h=Header(sendSeq,msgSent)
            data_packet=pickle.dumps(h,protocol=pickle.DEFAULT_PROTOCOL)
            UDP_client.sendto(data_packet,address)
            sendSeq=sendSeq+1
        UDP_client.settimeout(0.06)
        try:
            count=0
            while count<windowFrame:
                response,address=UDP_client.recvfrom(4096)
                responseMsg=pickle.loads(response)
                baseValue=responseMsg.seqNo
                sendSeq=baseValue
                count=count+1
            if count==windowFrame:
                windowFrame+=1
        except:
            if windowFrame>1:
                windowFrame=windowFrame-1
            globalendDate=datetime.utcnow()-datetime(1970,1,1)
            globalendSeconds=(globalendDate.total_seconds())
            globalmilliEnd=round(globalendSeconds*1000)    
            if globalmilliEnd-globalmilli>2500:
                break
    fp.close()
    UDP_client.close()

        



