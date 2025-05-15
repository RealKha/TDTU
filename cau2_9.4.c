// Worst-fit Memory Allocation
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

void *fAllocationWorstFit(void *param)
{
    int iSizeNew;
    printf("\nSize of process: ");
    scanf("%d", &iSizeNew);

    // Tìm lỗ trống lớn nhất
    int iFound = -1;
    int iWorstSize = -1; // Kích thước lỗ trống lớn nhất

    for (int i = 0; i < iHoleCount; i++)
    {
        if (M[i].iPID == -1)
        { // Nếu là lỗ trống
            if (M[i].iSize < iSizeNew)
                continue; // Lỗ trống quá nhỏ, bỏ qua
            else if (M[i].iSize > iWorstSize)
            {
                // Cập nhật lỗ trống lớn nhất
                iFound = i;
                iWorstSize = M[i].iSize;
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

            // Kiểm tra và gộp các lỗ trống liền kề sau khi thu hồi
            // Kiểm tra lỗ trống phía trước
            if (i > 0 && M[i - 1].iPID == -1)
            {
                // Gộp lỗ trống hiện tại với lỗ trống phía trước
                M[i - 1].iSize += M[i].iSize;

                // Dịch chuyển các phân vùng phía sau lên
                for (int j = i; j < iHoleCount - 1; j++)
                {
                    M[j] = M[j + 1];
                }
                iHoleCount--;
                i--; // Cập nhật lại chỉ số sau khi gộp
            }

            // Kiểm tra lỗ trống phía sau
            if (i < iHoleCount - 1 && M[i + 1].iPID == -1)
            {
                // Gộp lỗ trống hiện tại với lỗ trống phía sau
                M[i].iSize += M[i + 1].iSize;

                // Dịch chuyển các phân vùng còn lại lên
                for (int j = i + 1; j < iHoleCount - 1; j++)
                {
                    M[j] = M[j + 1];
                }
                iHoleCount--;
            }

            return 0;
        }
    }
    printf("Process %d cannot be found.", iTerminated);
    return 0;
}

void *fCompact(void *param)
{
    int iReAlloc = 0;
    int iHoleCollect = 0;
    int iSizeCollect = 0;

    // Duyệt qua tất cả các phân vùng
    for (int i = 0; i < iHoleCount; i++)
    {
        if (M[i].iPID == -1)
        { // Nếu là lỗ trống
            iReAlloc -= M[i].iSize;
            iHoleCollect++;
            iSizeCollect += M[i].iSize;
        }
        else
        { // Nếu là tiến trình
            // Di chuyển tiến trình về phía trước
            M[i - iHoleCollect].iPID = M[i].iPID;
            M[i - iHoleCollect].iBase = M[i].iBase + iReAlloc;
            M[i - iHoleCollect].iSize = M[i].iSize;
            strcpy(M[i - iHoleCollect].sName, M[i].sName);
        }
    }

    // Giảm số lượng phân vùng và tạo một lỗ trống lớn ở cuối
    iHoleCount = iHoleCount - iHoleCollect + 1;
    // Tạo một lỗ trống lớn ở cuối
    M[iHoleCount - 1].iPID = -1;
    M[iHoleCount - 1].iBase = (iHoleCount > 1) ? M[iHoleCount - 2].iBase + M[iHoleCount - 2].iSize : 0;
    M[iHoleCount - 1].iSize = iSizeCollect;

    printf("\nMemory compaction completed. Created a hole of size %d at address %d.\n",
           iSizeCollect, M[iHoleCount - 1].iBase);

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

    // Tính tỉ lệ phân mảnh bộ nhớ
    int totalMemory = 0;
    int totalHoles = 0;

    for (int i = 0; i < iHoleCount; i++)
    {
        if (i == 0)
        {
            totalMemory = M[i].iSize; // Lấy kích thước bộ nhớ từ phân vùng đầu tiên
        }

        if (M[i].iPID == -1)
        {
            totalHoles += M[i].iSize;
        }
    }

    float fragRatio = (float)totalHoles / totalMemory;
    printf("\nPhân mảnh bộ nhớ: %.2f%%\n", fragRatio * 100);

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
        printf("\nChon option:   1-Cap phat (Worst-Fit)   2-Thu hoi   3-Gom cum   4-Thong ke  5-Thoat  \n");
        scanf("%d", &iOption);
        switch (iOption)
        {
        case 1:
            pthread_create(&tid[1], NULL, fAllocationWorstFit, NULL);
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