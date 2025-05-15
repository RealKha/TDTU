// Memory Allocation with Fragmentation Calculation
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

// Hàm cấp phát bộ nhớ theo First-fit
void *fAllocation(void *param)
{
    int iSizeNew;
    printf("\nSize of process: ");
    scanf("%d", &iSizeNew);
    for (int i = 0; i < iHoleCount; i++)
    {
        if (M[i].iPID == -1)
        {
            if (M[i].iSize < iSizeNew)
                continue;
            if (M[i].iSize == iSizeNew)
            {
                // allocate to replace this hole, no new hole left.
                M[i].iPID = iPIDcount++;
                // M[i].iBase and iSize no change
                printf("\nNew process allocated PID = %d from %d to %d\n", M[i].iPID, M[i].iBase, M[i].iBase + M[i].iSize - 1);
                return 0;
            }
            else if (M[i].iSize > iSizeNew)
            { // allocate to this hole, but left a new smaller hole
                iHoleCount++;
                for (int j = iHoleCount; j > i + 1; j--)
                    M[j] = M[j - 1]; // shift right all hole to make new hole.
                M[i + 1].iPID = -1;
                M[i + 1].iSize = M[i].iSize - iSizeNew;
                M[i + 1].iBase = M[i].iBase + iSizeNew;
                M[i].iPID = iPIDcount++;
                // M[i].iBase no change;
                M[i].iSize = iSizeNew;
                printf("\nNew process allocated PID = %d from %d to %d", M[i].iPID, M[i].iBase, M[i].iBase + M[i].iSize - 1);
                printf("\nNew hole left over from %d to %d\n", M[i + 1].iBase, M[i + 1].iBase + M[i + 1].iSize - 1);
                return 0;
            }
        } // end of hole found
    } // end of for
    printf("\nFailure to allocate memory.\n"); // no hole fit
    return 0;
}

// Hàm thu hồi bộ nhớ với gộp lỗ trống liền kề
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
            // Trường hợp 1: Kiểm tra lỗ trống phía trước
            if (i > 0 && M[i - 1].iPID == -1)
            {
                printf("\nMerging with previous hole...");
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

            // Trường hợp 2: Kiểm tra lỗ trống phía sau
            if (i < iHoleCount - 1 && M[i + 1].iPID == -1)
            {
                printf("\nMerging with next hole...");
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

// Hàm chống phân mảnh bộ nhớ
void *fCompact(void *param)
{
    printf("\nCompacting memory...");
    int iReAlloc = 0;
    int iHoleCollect = 0;
    int iSizeCollect = 0;

    // Duyệt qua tất cả các phân vùng
    for (int i = 0; i < iHoleCount; i++)
    {
        if (M[i].iPID == -1)
        { // Nếu là lỗ trống
            iReAlloc += M[i].iSize;
            iHoleCollect++;
            iSizeCollect += M[i].iSize;
        }
        else
        { // Nếu là tiến trình
            // Di chuyển tiến trình về phía trước
            if (iHoleCollect > 0)
            {
                M[i - iHoleCollect].iPID = M[i].iPID;
                M[i - iHoleCollect].iBase = M[i].iBase - iReAlloc;
                M[i - iHoleCollect].iSize = M[i].iSize;
                strcpy(M[i - iHoleCollect].sName, M[i].sName);

                printf("\nProcess %d moved from %d to %d",
                       M[i].iPID, M[i].iBase, M[i - iHoleCollect].iBase);
            }
        }
    }

    // Giảm số lượng phân vùng và tạo một lỗ trống lớn ở cuối
    int newHoleCount = iHoleCount - iHoleCollect + 1;

    // Kiểm tra xem còn ít nhất một tiến trình
    if (newHoleCount > 1)
    {
        // Tạo một lỗ trống lớn ở cuối
        M[newHoleCount - 1].iPID = -1;
        M[newHoleCount - 1].iBase = M[newHoleCount - 2].iBase + M[newHoleCount - 2].iSize;
        M[newHoleCount - 1].iSize = iSizeCollect;

        // Cập nhật số lượng phân vùng
        iHoleCount = newHoleCount;

        printf("\nMemory compacted. Created a hole of size %d at address %d.\n",
               iSizeCollect, M[newHoleCount - 1].iBase);
    }
    else
    {
        // Trường hợp chỉ có lỗ trống, không có tiến trình
        M[0].iPID = -1;
        M[0].iBase = 0;
        M[0].iSize = iSizeCollect;
        iHoleCount = 1;

        printf("\nNo processes in memory. Entire memory is free.\n");
    }

    return 0;
}

// Hàm thống kê tình trạng bộ nhớ và tính tỉ lệ phân mảnh
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
    int holeCount = 0;
    int usedMemory = 0;

    // Tính tổng kích thước bộ nhớ
    for (int i = 0; i < iHoleCount; i++)
    {
        totalMemory += M[i].iSize;

        // Tính tổng kích thước lỗ trống
        if (M[i].iPID == -1)
        {
            totalHoles += M[i].iSize;
            holeCount++;
        }
        else
        {
            usedMemory += M[i].iSize;
        }
    }

    printf("\n--- Thông kê bộ nhớ ---");
    printf("\nTổng dung lượng bộ nhớ: %d", totalMemory);
    printf("\nSố lượng phân vùng: %d", iHoleCount);
    printf("\nBộ nhớ đã sử dụng: %d (%.2f%%)", usedMemory, (float)usedMemory * 100 / totalMemory);
    printf("\nSố lượng lỗ trống: %d", holeCount);
    printf("\nTổng dung lượng lỗ trống: %d (%.2f%%)", totalHoles, (float)totalHoles * 100 / totalMemory);

    // Chỉ tính tỉ lệ phân mảnh khi có ít nhất 1 lỗ trống và bộ nhớ đã sử dụng
    if (holeCount > 0 && usedMemory > 0)
    {
        // Tỉ lệ phân mảnh = Tổng dung lượng các lỗ trống / Tổng dung lượng bộ nhớ
        float fragRatio = (float)totalHoles / totalMemory;
        printf("\nTỉ lệ phân mảnh bộ nhớ: %.2f%%", fragRatio * 100);

        // Kiểm tra khả năng cấp phát sau khi chống phân mảnh
        int maxHoleSize = 0;
        for (int i = 0; i < iHoleCount; i++)
        {
            if (M[i].iPID == -1 && M[i].iSize > maxHoleSize)
            {
                maxHoleSize = M[i].iSize;
            }
        }

        printf("\nLỗ trống lớn nhất hiện tại: %d", maxHoleSize);
        printf("\nLỗ trống có thể sau khi chống phân mảnh: %d", totalHoles);

        if (totalHoles > maxHoleSize)
        {
            printf("\nChống phân mảnh sẽ giúp cấp phát được các tiến trình có kích thước lớn hơn.");
        }
    }

    printf("\n");
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
        printf("\nChon option:   1-Cap phat   2-Thu hoi   3-Gom cum   4-Thong ke  5-Thoat  \n");
        scanf("%d", &iOption);
        switch (iOption)
        {
        case 1:
            pthread_create(&tid[1], NULL, fAllocation, NULL);
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