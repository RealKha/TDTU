// 2021 June 7
// Author: Tran Trung Tin
// Calculating value of PI by Monte Carlo method with Peterson's algorithm
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>
#include <math.h>
#include <sys/syscall.h>
#include <unistd.h>
#include <stdbool.h>

// Maximum number of threads
#define MAX_THREAD 2

int counter = 0; /* Shared data */
int turn;        /* Peterson: Shared variable for turn */
bool flag[2];    /* Peterson: Flags for each thread */

void *runner(void *param); /* Threads call this function */

int main(int argc, char *argv[]) {
    pthread_t tid[MAX_THREAD]; /* Thread identifiers */
    pthread_attr_t attr;       /* Thread attributes */
    struct timeval startwatch, endwatch;

    /* Initialize thread attributes */
    pthread_attr_init(&attr);

    /* Initialize Peterson variables */
    flag[0] = flag[1] = false;
    turn = 0;

    /* Get number of iterations per thread */
    int n_thread = 2; // Fixed to 2 threads
    int iterations = atoi(argv[1]);

    /* Start timing */
    gettimeofday(&startwatch, NULL);

    /* Create threads */
    for (int i = 0; i < n_thread; i++)
        pthread_create(&tid[i], NULL, runner, &iterations);

    /* Wait for threads to finish */
    for (int i = 0; i < n_thread; i++)
        pthread_join(tid[i], NULL);

    /* End timing */
    gettimeofday(&endwatch, NULL);

    /* Print execution time */
    printf("\nGettimeofday() method: %ldus",
           (endwatch.tv_sec - startwatch.tv_sec) * 1000000 +
               (endwatch.tv_usec - startwatch.tv_usec));

    /* Calculate and print Pi */
    printf("\nEstimated PI = %f\n",
           (float)counter / (n_thread * iterations) * 4);

    return 0;
}

/* Thread function */
void *runner(void *param) {
    srand((unsigned int)time(NULL));
    float x, y, distance;
    int a = *(int *)param;
    int thread_id = syscall(SYS_gettid) % 2; // Map thread ID to 0 or 1

    printf("\nThread %d is running.", thread_id);

    for (int i = 0; i < a; i++) {
        x = -1 + ((float)rand() / (float)(RAND_MAX)) * 2;
        y = -1 + ((float)rand() / (float)(RAND_MAX)) * 2;
        distance = sqrt(x * x + y * y);

        if (distance <= 1.0) {
            /* Peterson's algorithm */
            flag[thread_id] = true;
            turn = 1 - thread_id;
            while (flag[1 - thread_id] && turn == 1 - thread_id)
                ; // Busy wait
            /* Critical section */
            counter++;
            /* End critical section */
            flag[thread_id] = false;
        }
    }

    printf("\nThread %d finished.", thread_id);
    pthread_exit(0);
}
