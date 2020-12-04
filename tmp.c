#include <unistd.h>          //Provides API for POSIX(or UNIX) OS for system calls
#include <stdio.h>           //Standard I/O Routines
#include <stdlib.h>          //For exit() and rand()
#include <pthread.h>         //Threading APIs
#include <semaphore.h>       //Semaphore APIs

sem_t cnt;
int sum=0;
void *thread(void *tmp)
{
	sem_wait(&cnt);
	sum++;
	sem_post(&cnt);
}
void main()
{
	pthread_t t;
	sem_init(&cnt, 0, 1);
	int i;
	int status = pthread_create(&t, NULL, (void*)thread, (void*)&i);
	pthread_join(t, NULL);
	printf("%d\n", sum);
}