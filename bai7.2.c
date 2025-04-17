// 2021 June 7, modified 2025 April 17
// Author: Tran Trung Tin, modified by Grok
// Calculating value of PI by Monte Carlo method with Peterson's algorithm
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>
#include <math.h>
#include <unistd.h>
#include <stdbool.h>

// Maximum number of threads
#define MAX_THREAD 2

int counter = 0; /* Shared data */
int turn;        /* Peterson: Shared variable for turn */
bool flag[2];    /* Peterson: Flags for each thread */

void *runner(void *param); /* Threads call this function */

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <iterations_per_thread>\n", argv[0]);
        return 1;
    }

    pthread_t tid[MAX_THREAD]; /* Thread identifiers */
    pthread_attr_t attr;       /* Thread attributes */
    struct timeval startwatch, endwatch;

    /* Initialize thread attributes */
    pthread_attr_init(&attr);

    /* Initialize Peterson variables */
    flag[0] = flag[1] = false;
    turn = 0;

    /* Get number of iterations per thread */
    int iterations = atoi(argv[1]);
    if (iterations <= 0) {
        fprintf(stderr, "Iterations must be a positive integer\n");
        return 1;
    }

    /* Seed random number generator */
    srand((unsigned int)time(NULL));

    /* Start timing */
    gettimeofday(&startwatch, NULL);

    /* Create threads with thread index as parameter */
    int thread_ids[MAX_THREAD];
    for (int i = 0; i < MAX_THREAD; i++) {
        thread_ids[i] = i;
        pthread_create(&tid[i], &attr, runner, &thread_ids[i]);
    }

    /* Wait for threads to finish */
    for (int i = 0; i < MAX_THREAD; i++) {
        pthread_join(tid[i], NULL);
    }

    /* End timing */
    gettimeofday(&endwatch, NULL);

    /* Print execution time */
    printf("Gettimeofday() method: %ld us\n",
           (endwatch.tv_sec - startwatch.tv_sec) * 1000000 +
               (endwatch.tv_usec - startwatch.tv_usec));

    /* Calculate and print Pi */
    printf("Estimated PI = %f\n",
           (float)counter / (MAX_THREAD * iterations) * 4.0);

    /* Clean up */
    pthread_attr_destroy(&attr);
    return 0;
}

/* Thread function */
void *runner(void *param) {
    int thread_id = *(int *)param; /* Get thread index (0 or 1) */
    int iterations = *(int *)param; /* Get iterations from main */
    unsigned int seed = time(NULL) + thread_id; /* Unique seed for each thread */
    float x, y, distance;

    printf("Thread %d is running.\n", thread_id);

    for (int i = 0; i < iterations; i++) {
        x = -1.0 + ((float)(rand_r(&seed)) / RAND_MAX) * 2.0;
        y = -1.0 + ((float)(rand_r(&seed)) / RAND_MAX) * 2.0;
        distance = sqrt(x * x + y * y);

        if (distance <= 1.0) {
            /* Peterson's algorithm */
            flag[thread_id] = true;
            turn = 1 - thread_id;
            while (flag[1 - thread_id] && turn == 1 - thread_id)
                ; /* Busy wait */
            /* Critical section */
            counter++;
            /* End critical section */
            flag[thread_id] = false;
        }
    }

    printf("Thread %d finished.\n", thread_id);
    pthread_exit(0);
}
