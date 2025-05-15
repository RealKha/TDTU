// 2021 Jun 14
// Author: Tran Trung Tin
// Banker's Algorithm
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#define NUMBER_OF_CUSTOMERS 5
#define NUMBER_OF_RESOURCES 3
#define MAX_FILENAME_LENGTH 256

/*the maximum demand of each customer */
int maximum[NUMBER_OF_CUSTOMERS][NUMBER_OF_RESOURCES];

/* the amount currently allocated to each customer */
int allocation[NUMBER_OF_CUSTOMERS][NUMBER_OF_RESOURCES];

/* the remaining need of each customer */
int need[NUMBER_OF_CUSTOMERS][NUMBER_OF_RESOURCES];

/* available resources */
int available[NUMBER_OF_RESOURCES];

int safety_algorithm(int *available);
int request_resources(int customer_num, int request[]);
void release_resources(int customer_num, int release[]);

// Structure to pass parameters to thread function
typedef struct
{
    char filename[MAX_FILENAME_LENGTH];
    int matrix[NUMBER_OF_CUSTOMERS][NUMBER_OF_RESOURCES];
    int status;
} thread_data;

// Function to read matrix from file
void *read_matrix_from_file(void *arg)
{
    thread_data *data = (thread_data *)arg;
    FILE *file = fopen(data->filename, "r");

    if (file == NULL)
    {
        printf("Error opening file %s\n", data->filename);
        data->status = -1;
        pthread_exit(NULL);
    }

    for (int i = 0; i < NUMBER_OF_CUSTOMERS; i++)
    {
        for (int j = 0; j < NUMBER_OF_RESOURCES; j++)
        {
            if (fscanf(file, "%d", &data->matrix[i][j]) != 1)
            {
                printf("Error reading from file %s\n", data->filename);
                data->status = -1;
                fclose(file);
                pthread_exit(NULL);
            }
        }
    }

    fclose(file);
    data->status = 0;
    pthread_exit(NULL);
}

// Function to copy matrix data
void copy_matrix(int dest[NUMBER_OF_CUSTOMERS][NUMBER_OF_RESOURCES],
                 int src[NUMBER_OF_CUSTOMERS][NUMBER_OF_RESOURCES])
{
    for (int i = 0; i < NUMBER_OF_CUSTOMERS; i++)
    {
        for (int j = 0; j < NUMBER_OF_RESOURCES; j++)
        {
            dest[i][j] = src[i][j];
        }
    }
}

int main(int argc, char **argv)
{
    pthread_t threads[2];
    thread_data t_data[2];

    // Check if enough arguments are provided
    if (argc < NUMBER_OF_RESOURCES + 3)
    {
        printf("Usage: %s <available_resources> <maximum_file> <allocation_file>\n", argv[0]);
        printf("Example: %s 3 3 2 task3_maximum.txt task3_allocation.txt\n", argv[0]);
        return -1;
    }

    // Set available resources from command line arguments
    for (int i = 0; i < NUMBER_OF_RESOURCES; i++)
    {
        available[i] = atoi(argv[i + 1]);
    }

    // Setup thread data for maximum matrix
    strncpy(t_data[0].filename, argv[NUMBER_OF_RESOURCES + 1], MAX_FILENAME_LENGTH - 1);
    t_data[0].filename[MAX_FILENAME_LENGTH - 1] = '\0';
    t_data[0].status = 0;

    // Setup thread data for allocation matrix
    strncpy(t_data[1].filename, argv[NUMBER_OF_RESOURCES + 2], MAX_FILENAME_LENGTH - 1);
    t_data[1].filename[MAX_FILENAME_LENGTH - 1] = '\0';
    t_data[1].status = 0;

    // Create threads to read matrices
    if (pthread_create(&threads[0], NULL, read_matrix_from_file, (void *)&t_data[0]) != 0)
    {
        printf("Error creating thread for maximum matrix\n");
        return -1;
    }

    if (pthread_create(&threads[1], NULL, read_matrix_from_file, (void *)&t_data[1]) != 0)
    {
        printf("Error creating thread for allocation matrix\n");
        return -1;
    }

    // Wait for threads to complete
    pthread_join(threads[0], NULL);
    pthread_join(threads[1], NULL);

    // Check if both files were read successfully
    if (t_data[0].status != 0 || t_data[1].status != 0)
    {
        printf("Error reading input files\n");
        return -1;
    }

    // Copy data from thread structures to global matrices
    copy_matrix(maximum, t_data[0].matrix);
    copy_matrix(allocation, t_data[1].matrix);

    // Print the matrices for verification
    printf("Maximum matrix:\n");
    for (int i = 0; i < NUMBER_OF_CUSTOMERS; i++)
    {
        for (int j = 0; j < NUMBER_OF_RESOURCES; j++)
        {
            printf("%d ", maximum[i][j]);
        }
        printf("\n");
    }

    printf("\nAllocation matrix:\n");
    for (int i = 0; i < NUMBER_OF_CUSTOMERS; i++)
    {
        for (int j = 0; j < NUMBER_OF_RESOURCES; j++)
        {
            printf("%d ", allocation[i][j]);
        }
        printf("\n");
    }

    printf("\nAvailable resources: ");
    for (int i = 0; i < NUMBER_OF_RESOURCES; i++)
    {
        printf("%d ", available[i]);
    }
    printf("\n\n");

    // Run safety algorithm
    safety_algorithm(available);
    return 0;
}

int safety_algorithm(int *available)
{
    int i, j, k;
    int ans[NUMBER_OF_CUSTOMERS], ind = 0;
    bool Finish[NUMBER_OF_CUSTOMERS] = {false};
    int work[NUMBER_OF_RESOURCES]; // Fixed: This should be NUMBER_OF_RESOURCES, not NUMBER_OF_CUSTOMERS

    // STEP 1
    for (i = 0; i < NUMBER_OF_RESOURCES; i++)
        work[i] = *(available + i);

    for (i = 0; i < NUMBER_OF_CUSTOMERS; i++)
    {
        for (j = 0; j < NUMBER_OF_RESOURCES; j++)
            need[i][j] = maximum[i][j] - allocation[i][j];
    }

    // STEP 2
    int y = 0;
    for (k = 0; k < NUMBER_OF_CUSTOMERS; k++)
    {
        for (i = 0; i < NUMBER_OF_CUSTOMERS; i++)
        {
            if (Finish[i] == false)
            {
                int flag = 0;
                for (j = 0; j < NUMBER_OF_RESOURCES; j++)
                {
                    if (need[i][j] > work[j])
                    {
                        flag = 1;
                        break;
                    }
                }
                if (flag == 0)
                { // STEP 3
                    ans[ind++] = i;
                    for (y = 0; y < NUMBER_OF_RESOURCES; y++)
                        work[y] += allocation[i][y];
                    Finish[i] = true;
                }
            }
        }
    }

    // STEP 4
    bool bSafe = true;
    for (i = 0; i < NUMBER_OF_CUSTOMERS; i++)
        if (Finish[i] == false)
            bSafe = false;

    if (bSafe)
    {
        printf("Following is the SAFE Sequence: ");
        for (i = 0; i < NUMBER_OF_CUSTOMERS - 1; i++)
            printf(" P%d ->", ans[i]);
        printf(" P%d.\n", ans[NUMBER_OF_CUSTOMERS - 1]);
        return (0);
    }
    else
    {
        printf("The system is UNSAFE.\n");
        return -1;
    }
}

// Function implementations for request_resources and release_resources
int request_resources(int customer_num, int request[])
{
    int i;

    // Check if request is valid
    for (i = 0; i < NUMBER_OF_RESOURCES; i++)
    {
        if (request[i] > need[customer_num][i])
        {
            printf("Error: Process has exceeded its maximum claim.\n");
            return -1;
        }

        if (request[i] > available[i])
        {
            printf("Resources not available. Process must wait.\n");
            return -1;
        }
    }

    // Try to allocate resources temporarily
    for (i = 0; i < NUMBER_OF_RESOURCES; i++)
    {
        available[i] -= request[i];
        allocation[customer_num][i] += request[i];
        need[customer_num][i] -= request[i];
    }

    // Check if the resulting state is safe
    if (safety_algorithm(available) == -1)
    {
        // If not safe, rollback the allocation
        for (i = 0; i < NUMBER_OF_RESOURCES; i++)
        {
            available[i] += request[i];
            allocation[customer_num][i] -= request[i];
            need[customer_num][i] += request[i];
        }
        printf("Request denied: resulting state would be unsafe.\n");
        return -1;
    }

    printf("Request granted.\n");
    return 0;
}

void release_resources(int customer_num, int release[])
{
    int i;

    // Release resources
    for (i = 0; i < NUMBER_OF_RESOURCES; i++)
    {
        available[i] += release[i];
        allocation[customer_num][i] -= release[i];
        need[customer_num][i] += release[i];
    }

    printf("Resources released.\n");
}