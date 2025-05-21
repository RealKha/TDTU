import numpy as np

def bai1():
    so = [1, 3, 5, 2, 9]
    gia_tri = [-1, 3, 15, 27, 29]

    so_luong_so = len(so)
    so_luong_gia_tri = len(gia_tri)

    print('Vector so:')
    print(so)
    print('So luong phan tu trong so:', so_luong_so)

    print('Vector gia_tri:')
    print(gia_tri)
    print('So luong phan tu trong gia_tri:', so_luong_gia_tri)

def bai2():
    n = 10

    b = list(range(12, 12 + 2*n, 2))
    print('Vector b:')
    print(b)

    c = list(range(31, 31 + 2*n, 2))
    print('Vector c:')
    print(c)

    day1 = list(range(-5, 6))
    print('Vector day1:')
    print(day1)

    day2 = list(range(5, -6, -1))
    print('Vector day2:')
    print(day2)

    day3 = list(range(10, -6, -2))
    print('Vector day3:')
    print(day3)

    luy_thua = [1/(2**i) for i in range(8)]
    print('Vector luy_thua:')
    print(luy_thua)

    fibonacci = [1, 1]
    for i in range(2, 8):
        fibonacci.append(fibonacci[i-1] + fibonacci[i-2])
    dao_fibo = [1/f for f in fibonacci]
    print('Vector dao_fibo:')
    print(dao_fibo)

    def lay_n_snt(n):
        so_nt = []
        so = 2
        while len(so_nt) < n:
            la_snt = True
            for i in range(2, int(so**0.5) + 1):
                if so % i == 0:
                    la_snt = False
                    break
            if la_snt:
                so_nt.append(so)
            so += 1
        return so_nt

    snt = lay_n_snt(9)  
    dao_snt = [1/p for p in snt]
    print('Vector dao_snt:')
    print(dao_snt)

    tam_giac = [i*(i+1)//2 for i in range(1, 9)]
    print('Vector tam_giac:')
    print(tam_giac)

    day_n = [1/(i**2 + 1) for i in range(1, 5)]
    print('Vector day_n:')
    print(day_n)

    chia_2 = [i//2 for i in range(6)]
    print('Vector chia_2:')
    print(chia_2)

    chu_thuong = [chr(i) for i in range(ord('a'), ord('z')+1)]
    print('Vector chu_thuong:')
    print(chu_thuong)

    chu_cach = [chr(ord('A') + 3*i) for i in range(9) if ord('A') + 3*i <= ord('Z')]
    print('Vector chu_cach:')
    print(chu_cach)

def bai3(n=5):
    vector_log = np.logspace(1, n, n)
    print('Vector co khoang logarit:')
    print(vector_log)

def bai4():
    a = [1, 2, 3]
    b = [98, 12, 33]
    gop = a + b

    print('Vector a:')
    print(a)
    print('Vector b:')
    print(b)
    print('Vector gop (noi a va b):')
    print(gop)

def bai5():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    ghep = np.vstack((a, b))

    print('Vector a:')
    print(a)
    print('Vector b:')
    print(b)
    print('Vector ghep (chong len nhau):')
    print(ghep)

def bai6():
    so = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

    dau_sau = so[:6]
    print('a) Sau phan tu dau:')
    print(dau_sau)

    cuoi_nam = so[-5:]
    print('b) Nam phan tu cuoi:')
    print(cuoi_nam)

    chon_c = [so[0], so[3], so[-1]]
    print('c) Phan tu 1, 4 va cuoi:')
    print(chon_c)

    chon_d = [so[0], so[2], so[4], so[6]]
    print('d) Phan tu 1, 3, 5, 7:')
    print(chon_d)

    chi_so_le = so[::2]
    print('e) Chi so le:')
    print(chi_so_le)

    chi_so_chan = so[1::2]
    print('f) Chi so chan:')
    print(chi_so_chan)

def bai7():
    du_lieu = [3, 11, -9, -131, -1, 1, -11, 91, -6, 407, -12, -11, 12, 153, 371]

    lon_nhat = max(du_lieu)
    print('a) Gia tri lon nhat:')
    print(lon_nhat)

    nho_nhat = min(du_lieu)
    print('b) Gia tri nho nhat:')
    print(nho_nhat)

    vi_tri_lon_10 = [i for i, val in enumerate(du_lieu) if val > 10]
    print('c) Vi tri lon hon 10:')
    print(vi_tri_lon_10)

    dao_nguoc = du_lieu[::-1]
    print('d) Dao nguoc:')
    print(dao_nguoc)

    tang_dan = sorted(du_lieu)
    print('e) Tang dan:')
    print(tang_dan)

    giam_dan = sorted(du_lieu, reverse=True)
    print('f) Giam dan:')
    print(giam_dan)

    dem = 0
    for i in range(len(du_lieu)):
        for j in range(len(du_lieu)):
            if i != j and du_lieu[i] + du_lieu[j] == 0:
                dem += 1
    dem = dem // 2
    print('g) So cap co tong = 0:')
    print(dem)

    trung_lap = len(du_lieu) - len(set(du_lieu))
    print('h) So luong phan tu trung lap:')
    print(trung_lap)

    n = len(du_lieu)
    tong_doi_xung = [du_lieu[i] + du_lieu[n-i-1] for i in range(n)]
    print('i) Vector tong doi xung:')
    print(tong_doi_xung)

    def la_so_armstrong(so):
        so_chuoi = str(abs(so))
        bac = len(so_chuoi)
        tong_luy_thua = sum(int(ch)**bac for ch in so_chuoi)
        return abs(so) == tong_luy_thua

    so_armstrong = [so for so in du_lieu if la_so_armstrong(so)]
    print('j) So armstrong:')
    print(so_armstrong)

    duong = [so for so in du_lieu if so >= 0]
    print('k) Loai bo so am:')
    print(duong)

    trung_vi = np.median(du_lieu)
    print('l) Trung vi:')
    print(trung_vi)

    trung_binh = np.mean(du_lieu)
    nho_tb = [so for so in du_lieu if so < trung_binh]
    tong_nho_tb = sum(nho_tb)
    print('m) Tong phan tu nho hon trung binh:')
    print(tong_nho_tb)

    tuyet_doi = [abs(so) for so in du_lieu]
    print('n) Gia tri tuyet doi:')
    print(tuyet_doi)