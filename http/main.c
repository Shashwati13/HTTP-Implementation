#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void send_http(char* host, char* msg, char* resp, size_t len);


/*
  Implement a program that takes a host, verb, and path and
  prints the contents of the response from the request
  represented by that request.
 */
int main(int argc, char* argv[]) {
//  if (argc != 4) {
 //   printf("Invalid arguments - %s <host> <GET|POST> <path>\n", argv[0]);
  //  return -1;
  //}
  char* host = argv[1];
  char* verb = argv[2];
  char* path = argv[3];
  char *buff = malloc(strlen(argv[2]) + strlen(argv[3]));
       buff = realloc(buff,200); 
    if (buff == NULL) {
	            fprintf(stderr, "No memory\n");
		            return 1;
			        }
    strcpy(buff,verb);
    strcat(buff," ");
    strcat(buff,path);
    strcat(buff," HTTP/1.1\r\nHost:");
    strcat(buff,host);

   int result=strcmp(verb,"GET");
   int res=strcmp(verb,"POST");
    if (result==0){
	  strcat(buff,"\r\n\r\n"); 	    
    }
    if (res==0){
	  strcat(buff,"\r\nContent-Length: ");
	  strcat(buff,"10\r\n\r\nThis is it\r\n\r\n");
    }

 char response[4096];
 send_http(host, buff, response, 4096);
printf("%s\n", response);

  return 0;
}
