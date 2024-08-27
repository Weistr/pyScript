import sympy

def flybackTransformer_calc():
    print(
        "反激变压器计算.\n"
        )
    print("计算输入电流....")
    eff = float(input("电源效率="))
    Vo = float(input("输出电压(V)="))
    Io_max = float(input("最大输出电流(A)="))
    Pmax = Vo * Io_max
    print("计算得最大功率=",Pmax,"W")
    Vimin = float(input("最小输入电压(V)="))
    IiRMS = Pmax / eff / Vimin
    print("计算得最大输入电流Iirms=",IiRMS)

    while True:
        kpp = float(input("纹波电流Ipp = k*IiRMS(k<2), k="))
        Ipp = kpp*IiRMS
        if Ipp/2 < IiRMS :
            Ip = IiRMS + Ipp/2
            print("计算得电流波峰Ip=",Ip,"A")
            break
        else :
            
            print("k过大\n")

    Dmax = float(input("最大占空比Dmax = "))
    Fsw = float(input("开关频率(kHz) = "))

    Lp = Vimin*Dmax / (Fsw*1000*Ipp) 
    print("计算得初级线圈电感量=",Lp * 10**6 ,"uH")

def calc_lg() :
    print("计算气隙lg=")
    pi=3.1415926
    N = 63
    ug = 4*pi*10**-7
    #ug=1
    Ae = 39.6
    L2 = 780
    lg = N**2 * ug * Ae * 10**-6 / (L2*10**-6)
    print(lg*10**3)

def calc_Ntons():
    x = sympy.Symbol('x')
    
    N1 = 20
    L1 = 905 * 10**-6
    L2 = 300 * 10**-6
    N2 = sympy.symbols('N2')
    Ae = 39.6 * 10**-6
    Bmax = 0.4


    sov = sympy.solve(
        (N1**2 / L1 + N2**2 / L2)*Ae*Bmax/N2-1.42,N2
        )
    print(sov)


def calc_Isat_withGap():
    pi=3.1415926
    N1 = 20
    L1 = 905 * 10**-6
    lg = 0.5 * 10**-3
    u0 = 4*pi*10**-7
    Ae = 39.6 * 10**-6
    N2 = 20


    Bmax = 0.4
    sov = (N1**2 / L1 + lg/(u0*Ae))*Ae*Bmax / N2
    
    print(sov)


calc_Isat_withGap()
#testSympy()