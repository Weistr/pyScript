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
    u0 = 1.26*10**-6
    N1 = 20
    L1 = 905 * 10**-6
    Ae = 39.6 * 10**-6
    N2 = 63
    L2 = 755 * 10**-6
    lg = (u0*Ae)*(N2**2 / L2 - N1**2 / L1)
    print(lg*10**3)

def calc_Ntons():
    L2 = 755 * 10**-6
    Isat = 1.2
    Bmax = 0.4
    L1 = 905 * 10**-6
    N1 = 20   
    Ae = 39.6 * 10**-6
    u0 = 1.26 * 10**-6

    lg,N2 = sympy.symbols('lg,N2')
    eq1 = (u0*Ae)*(N2**2 / L2 - N1**2 / L1)-lg
    eq2 = (N1**2 / L1 + lg/(u0*Ae))*Ae*Bmax / N2 - Isat
    solv = sympy.solve(
        [eq1,eq2],
        [lg,N2]
    )
    lg = solv[0][0]*10**3
    N2 = solv[0][1]
    print("lg=",solv[0][0]*10**3,"mm  ","N2=",solv[0][1])

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



calc_Ntons()
#testSympy()