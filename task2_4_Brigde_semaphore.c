// 2021 March 15, modified 2025 April 17
// Author: G4G, modified by Grok
// Farmer crossing Vermont bridge with semaphore
#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>
#include <semaphore.h>
#include <time.h>

#define MAX_FARMER 10
pthread_t tid[MAX_FARMER];
sem_t north_sem; // Semaphore for North direction
sem_t south_sem; // Semaphore for South direction

void *farmer(void *param) {
    int id = *(int *)param;
    free(param);

    // Randomly assign direction: 0 for North, 1 for South
    int direction = rand() % 2;
    const char *dir_str = (direction == 0) ? "North" : "South";

    printf("Farmer %d from %s arriving at bridge...\n", id, dir_str);

    // Wait for semaphore based on direction
    if (direction == 0) {
        sem_wait(&north_sem); // Acquire North semaphore
    } else {
        sem_wait(&south_sem); // Acquire South semaphore
    }

    printf("Farmer %d from %s entering bridge...\n", id, dir_str);
    sleep(rand() % 5 + 3); // Random time to cross (3-7 seconds)
    printf("Farmer %d from %s leaving bridge...\n", id, dir_str);

    // Release semaphore based on direction
    if (direction == 0) {
        sem_post(&north_sem); // Release North semaphore
    } else {
        sem_post(&south_sem); // Release South semaphore
    }

    return NULL;
}

int main(void) {
    // Initialize random number generator
    srand((unsigned)time(NULL));

    // Initialize semaphores
    sem_init(&north_sem, 0, 1); // North semaphore starts at 1
    sem_init(&south_sem, 0, 1); // South semaphore starts at 1

    // Create farmer threads
    for (int i = 0; i < MAX_FARMER; i++) {
        int *p = malloc(sizeof(int));
        *p = i;
        pthread_create(&tid[i], NULL, farmer, p);
        sleep(rand() % 3); // Random delay between farmer arrivals (0-2 seconds)
    }

    // Wait for all farmers to finish
    for (int i = 0; i < MAX_FARMER; i++) {
        pthread_join(tid[i], NULL);
    }

    // Destroy semaphores
    sem_destroy(&north_sem);
    sem_destroy(&south_sem);

    return 0;
}
