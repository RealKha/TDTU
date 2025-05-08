Lab 9.1
Yêu cầu 1:
--- Trong chương trình trên, các lệnh trả khóa (unlock) tại các dòng 42, 43 (trong do_work_one) và 53, 54 (trong do_work_two) không được thực thi nếu xảy ra deadlock. Lý do là:
•	Deadlock: Khi Thread 1 khóa first_mutex (dòng 38) và chờ second_mutex (dòng 40), trong khi Thread 2 khóa second_mutex (dòng 49) và chờ first_mutex (dòng 51), cả hai thread bị kẹt trong trạng thái chờ lẫn nhau. Không thread nào có thể tiến hành để đến các lệnh pthread_mutex_unlock.
•	Hậu quả: Vì các thread không thể vượt qua các lệnh pthread_mutex_lock đang chờ, các lệnh trả khóa (pthread_mutex_unlock) tại dòng 42, 43 (Thread 1) và 53, 54 (Thread 2) không bao giờ được thực thi trong trường hợp deadlock.
Tóm lại, nếu deadlock xảy ra, các lệnh trả khóa này sẽ không được thực hiện.

--- Chương trình không kết thúc nếu xảy ra deadlock.

--- Thay đổi thứ tự khóa trong do_work_two khiến cả hai thread khóa mutex theo cùng thứ tự (first_mutex rồi second_mutex), loại bỏ deadlock. 
Chương trình sẽ thực thi thành công, in thông điệp từ cả hai thread và kết thúc bình thường.

  Yêu cầu 2:
--- pthread_mutex_trylock() tránh deadlock vì:
•	Không chặn thread khi mutex đã bị khóa, trả về ngay nếu thất bại.
•	Thread thất bại sẽ mở khóa mutex đang giữ và thử lại, phá vỡ circular wait.
•	Đảm bảo một thread sẽ hoàn thành, cho phép thread kia tiếp tục, tránh kẹt.

--- Starvation xảy ra vì:
•	Thread cạnh tranh mutex không công bằng, một thread có thể liên tục giành mutex do lịch trình hệ thống ưu tiên.
•	pthread_mutex_trylock() không đảm bảo thứ tự cấp khóa, khiến thread kém may mắn bị bỏ đói tài nguyên (mutex).

--- Tính liveness là khả năng chương trình hoặc thread tiến triển và hoàn thành công việc, tránh các trạng thái như deadlock, starvation, hoặc livelock.
Yêu cầu 3:
--- Deadlock xảy ra khi cả 5 triết gia đồng thời giữ một đũa và chờ đũa kia, tạo thành vòng chờ vô hạn.
--- Không còn deadlock, nhưng có thể xảy ra starvation.
--- Liveness tốt hơn (không deadlock), nhưng vẫn có thể bị giảm do starvation.
