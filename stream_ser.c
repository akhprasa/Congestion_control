#include <netinet/tcp.h>
#include <stdio.h>
#include <signal.h>
#include <netdb.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include <sys/socket.h>
#include <time.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <ctype.h>
#include <errno.h>

int main(int argc, char ** argv){
	struct sockaddr_in seraddr;
	int sockfd, cli_fd;
	int addrlen = sizeof(seraddr);
	char filename[100], buffer[1024];
	int i, fp, read_bytes;
	char *temp = "EOF";

	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	setsockopt(sockfd, IPPROTO_TCP, TCP_CONGESTION, argv[3], strlen(argv[3])+1);

	seraddr.sin_family = AF_INET;
	inet_aton((char *)argv[1], (struct in_addr *)&seraddr.sin_addr);
	seraddr.sin_port = htons((short)(atoi(argv[2])));

	if(bind(sockfd, (struct sockaddr *)&seraddr, sizeof(seraddr)) < 0){
		perror("Bind Failure");
		exit(EXIT_FAILURE);
	}
	
	listen(sockfd, 2);
	
	cli_fd = accept(sockfd, (struct sockaddr *)&seraddr, (socklen_t*)&addrlen);

	memset(filename, '\0', 100);

	read(cli_fd, filename, 100);
	
	fp = open(filename, O_RDONLY);
	if(fp < 0){
		perror("Error opening file");
		exit(EXIT_FAILURE);
	}

	for(i = 0; i >= 0; i++){
		//memset(filename, '\0', 100);
		//read(cli_fd, filename, 100);
		while(1){
			read_bytes = read(fp, buffer, 1024);
		      	if(read_bytes == 0){
				break;
			}
			write(cli_fd, buffer, read_bytes);
		}
		lseek(fp, 0, SEEK_SET);
		//sleep(2);
	}
	
	close(fp);
	close(sockfd);
	close(cli_fd);

	return 1;
}
