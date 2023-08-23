#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int connect_smtp(const char* host, int port);
void send_smtp(int sock, const char* msg, char* resp, size_t len);



/*
  Use the provided 'connect_smtp' and 'send_smtp' functions
  to connect to the "lunar.open.sice.indian.edu" smtp relay
  and send the commands to write emails as described in the
  assignment wiki.
 */
int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <email-to> <email-filepath>", argv[0]);
    return -1;
  }
int socket = connect_smtp("lunar.open.sice.indiana.edu", 25);
char* rcpt = argv[1];
  char* filepath = argv[2];
  FILE *fp;
  char *text;

  fp=fopen(filepath,"r");
  char resp[4096];
 if (fp == NULL)
{
	printf("Error while opening the file");
	return 1;
}

 
fseek(fp,0L,SEEK_END);
long numbytes=ftell(fp);
fseek(fp,0L,SEEK_SET);
text=(char*)calloc(numbytes,sizeof(char));
size_t s=fread(text,sizeof(char),numbytes,fp);
fclose(fp);
printf("%zu\n",s);
char buff[4096];
char rcpt1[200], rcpt2[200];
sprintf(buff,"%s \r\n.\r\n",text);
sprintf(rcpt1,"MAIL FROM:%s\n",rcpt);
sprintf(rcpt2,"RCPT TO:%s\n",rcpt);
send_smtp(socket,"HELO client.example.com\n",resp,4096);
printf("%s\n",resp);
send_smtp(socket,rcpt1,resp,4096);
printf("%s\n",resp);
send_smtp(socket,rcpt2,resp,4096);
printf("%s\n",resp);
send_smtp(socket,"DATA\n",resp,4096);
printf("%s\n",resp);
send_smtp(socket,buff,resp,4096);
printf("%s\n",resp);
send_smtp(socket,"QUIT\n",resp,4096);
printf("%s",resp);
  return 0;
}
