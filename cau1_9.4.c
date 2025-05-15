// Best-fit Memory Allocation
#include <pthread.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
struct hole
{
    int iPID; //-1 unused
    int iBase;
    int iSize;
    char sName[20];
};
struct hole M[100];
int iHoleCount = 0;
int iPIDcount = 1000;
pthread_t tid[5];

void *fAllocationBestFit(void *param)
{
    int iSizeNew;
    printf("\nSize of process: ");
    scanf("%d", &iSizeNew);

    // Tìm lỗ trống tốt nhất (nhỏ nhất mà đủ lớn để chứa tiến trình)
    int iFound = -1;
    int iBestSize = -1;

    for (int i = 0; i < iHoleCount; i++)
    {
        if (M[i].iPID == -1)
        { // Nếu là lỗ trống
            if (M[i].iSize < iSizeNew)
                continue; // Lỗ trống quá nhỏ, bỏ qua
            else if (iBestSize == -1 || M[i].iSize < iBestSize)
            {
                // Cập nhật lỗ trống tốt nhất nếu lỗ trống này nhỏ hơn lỗ trống tốt nhất hiện tại
                iFound = i;
                iBestSize = M[i].iSize;
            }
        }
    }

    // Nếu tìm thấy lỗ trống phù hợp
    if (iFound != -1)
    {
        // Trường hợp 1: Lỗ trống có kích thước bằng với kích thước yêu cầu
        if (M[iFound].iSize == iSizeNew)
        {
            // Cấp phát trực tiếp, không cần tạo lỗ trống mới
            M[iFound].iPID = iPIDcount++;
            printf("\nNew process allocated PID = %d from %d to %d\n",
                   M[iFound].iPID, M[iFound].iBase, M[iFound].iBase + M[iFound].iSize - 1);
        }
        // Trường hợp 2: Lỗ trống lớn hơn kích thước yêu cầu
        else
        {
            // Tăng số lượng lỗ trống và dịch chuyển các lỗ trống phía sau
            iHoleCount++;
            for (int j = iHoleCount - 1; j > iFound + 1; j--)
                M[j] = M[j - 1];

            // Tạo lỗ trống mới từ phần dư sau khi cấp phát
            M[iFound + 1].iPID = -1;
            M[iFound + 1].iSize = M[iFound].iSize - iSizeNew;
            M[iFound + 1].iBase = M[iFound].iBase + iSizeNew;

            // Cập nhật thông tin về lỗ trống được cấp phát
            M[iFound].iPID = iPIDcount++;
            M[iFound].iSize = iSizeNew;

            printf("\nNew process allocated PID = %d from %d to %d",
                   M[iFound].iPID, M[iFound].iBase, M[iFound].iBase + M[iFound].iSize - 1);
            printf("\nNew hole left over from %d to %d\n",
                   M[iFound + 1].iBase, M[iFound + 1].iBase + M[iFound + 1].iSize - 1);
        }
        return 0;
    }
    else
    {
        // Không tìm thấy lỗ trống phù hợp
        printf("\nFailure to allocate memory.\n");
        return 0;
    }
}

void *fTerminate(void *param)
{
    int iTerminated;
    printf("\nWhich PID terminate? ");
    scanf("%d", &iTerminated);
    for (int i = 0; i < iHoleCount; i++)
    {
        if (iTerminated == M[i].iPID)
        {
            M[i].iPID = -1;
            printf("\nProcess %d has been removed. Memory from %d to %d is free.",
                   iTerminated, M[i].iBase, M[i].iBase + M[i].iSize - 1);
            return 0;
        }
    }
    printf("Process %d cannot be found.", iTerminated);
    return 0;
}

void *fCompact(void *param)
{
    // Code cho việc gom cụm sẽ được thêm sau
    return 0;
}

void *fStatic(void *param)
{
    printf("\nStatic of memory \n");
    for (int i = 0; i < iHoleCount; i++)
    {
        if (M[i].iPID == -1)
            printf("Address [%d : %d]: Unused\n", M[i].iBase, M[i].iBase + M[i].iSize - 1);
        else
            printf("Address [%d : %d]: ProcessID %d\n", M[i].iBase, M[i].iBase + M[i].iSize - 1, M[i].iPID);
    }
    return 0;
}

int main(int argc, char *argv[])
{
    int iOption; // Chon lua trong menu

    if (argc < 2)
    {
        printf("Usage: %s <memory size>\n", argv[0]);
        return 1;
    }

    M[iHoleCount].iSize = atoi(argv[1]); // truyền kích thước vào khi gọi chạy
    M[iHoleCount].iPID = -1;
    M[iHoleCount].iBase = 0; // start of memory
    iHoleCount = 1;

    while (true)
    {
        printf("\nChon option:   1-Cap phat (Best-Fit)   2-Thu hoi   3-Gom cum   4-Thong ke  5-Thoat  \n");
        scanf("%d", &iOption);
        switch (iOption)
        {
        case 1:
            pthread_create(&tid[1], NULL, fAllocationBestFit, NULL);
            pthread_join(tid[1], NULL);
            break;
        case 2:
            pthread_create(&tid[2], NULL, fTerminate, NULL);
            pthread_join(tid[2], NULL);
            break;
        case 3:
            pthread_create(&tid[3], NULL, fCompact, NULL);
            pthread_join(tid[3], NULL);
            break;
        case 4:
            pthread_create(&tid[4], NULL, fStatic, NULL);
            pthread_join(tid[4], NULL);
            break;
        case 5:
            return 0;
        default:
            printf("\nVui long chon 1 - 5.\n");
        }
    }
}