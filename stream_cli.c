#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <error.h>
#include <fcntl.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/time.h>
#include <pthread.h>

int read_bytes = 0;
struct timeval start_time, cur_time;
FILE *fp;
pthread_mutex_t lock;
char hostname[100];
char folder[100];

void print_content(){
	float time;
	gettimeofday(&cur_time, NULL);
	time = (float)(cur_time.tv_sec - start_time.tv_sec)*1000.00 + (float)(cur_time.tv_usec - start_time.tv_usec)/1000.00;
	read_bytes = 0;
	fprintf(fp, "%5f\n", time);
	gettimeofday(&start_time, NULL);
}

double getCurTime(){
	struct timeval cur_time;
	gettimeofday(&cur_time, NULL);
	return (cur_time.tv_sec - start_time.tv_sec) + (double)(cur_time.tv_usec - start_time.tv_usec)/1000000;
}

void *Print( char * algo){
	int i = 0;
	double time;
	char filename[100];
	sprintf(filename, "%s/log_%s_%s_%d.txt", folder, hostname, algo, getpid());
	FILE *fp = fopen(filename, "w");
	double cur_time = 0;
	while(1){
		sleep(1);
		if(!i)
			time = getCurTime();
		else
			time = 1.0;
		cur_time += time;
		pthread_mutex_lock(&lock);
		fprintf(fp, "%2f %2f\n", cur_time, (read_bytes/time)/1000000*8);
		read_bytes = 0;
		pthread_mutex_unlock(&lock);
		i++;
		if(i==120)
			exit(EXIT_SUCCESS);
	}
	fclose(fp);
}

int main(int argc, char ** argv){
	int sockfd,i, flag=0;
	struct sockaddr_in seraddr;
	char buffer[1024];
	int num = 0;
	pthread_t thread;

	pthread_mutex_init(&lock, NULL);

	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if(setsockopt(sockfd, IPPROTO_TCP, TCP_CONGESTION, argv[3], strlen(argv[3])+1) < 0)
		exit(EXIT_FAILURE);
	
	seraddr.sin_family = AF_INET;
	seraddr.sin_port = htons((short)atoi(argv[2]));
	inet_aton((char *)argv[1], (struct in_addr *)&seraddr.sin_addr);

	if(connect(sockfd, (struct sockaddr *)&seraddr, sizeof(seraddr)) < 0){
		perror("Connect Failure");
		exit(EXIT_FAILURE);
	}

	send(sockfd, argv[4], strlen(argv[4]), 0);
	gettimeofday(&start_time, NULL);
	
	strcpy(hostname, argv[5]);
	strcpy(folder, argv[6]);
	pthread_create(&thread, NULL, Print, argv[3]);

	while(1){
		pthread_mutex_lock(&lock);
		read_bytes += read(sockfd, buffer, 1024);
		pthread_mutex_unlock(&lock);
	}

	close(sockfd);
	pthread_mutex_destroy(&lock);

	return 1;
}
