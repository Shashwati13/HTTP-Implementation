#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <string.h>

#define BUFFER_LENGTH 1000

/*
  Use the `getaddrinfo` and `inet_ntop` functions to convert a string host and
  integer port into a string dotted ip address and port.
 */
int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <host> <port>", argv[0]);
    return -1;
  }
  char* host = argv[1];
  long port = atoi(argv[2]);
  (void)port;

  struct addrinfo hints, *response=NULL;
  memset(&hints,0,sizeof(hints));
  /* Reference for hints, Computer Networks Lab 4 */
  hints.ai_flags= AI_PASSIVE;
  hints.ai_family = AF_UNSPEC;
  hints.ai_socktype= SOCK_STREAM;
  hints.ai_protocol=IPPROTO_TCP;

  getaddrinfo(host,"http",&hints,&response);
  struct addrinfo *itr;
  char buffer[1000];

  for (itr=response;itr!=NULL;itr=itr->ai_next)
  {
   void* raw_addr;
   if (itr->ai_family ==AF_INET){
	struct sockaddr_in *temp =(struct sockaddr_in*)itr ->ai_addr;
	raw_addr =&(temp->sin_addr);
	inet_ntop(AF_INET,raw_addr,buffer,sizeof(buffer));
	printf("IPv4 %s\n",buffer);
}
else {
	struct sockaddr_in6 *temp= (struct sockaddr_in6*)itr ->ai_addr;
	raw_addr =&(temp->sin6_addr);
	inet_ntop(AF_INET6,raw_addr,buffer,sizeof(buffer));
	printf("IPv6 %s\n",buffer);

}



   }


 


  return 0;
}
