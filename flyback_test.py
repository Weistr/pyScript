from sympy import * 
from math import sqrt




pi = 3.1415926
#电气参数
eff = 0.8 #电源效率
Vo = 15 #输出电压
Io_max = 0.8 #额定输出电流
Pmax = Vo * Io_max / eff #最大功率
print("Pmax = ",Pmax,"W")

Vi_AC_RMS_Min = 220 * (1-0.15)
Vi_AC_RMS_Max = 220 * (1+0.15)

Vbus_pk_Min = Vi_AC_RMS_Min * sqrt(2)#母线电压峰值
Vbus_pk_Max = Vi_AC_RMS_Max * sqrt(2)

#输入电容计算
Fi_AC = 50#输入交流电50Hz
Vbus_pp = 25 #纹波
Vbus_AVG_Min = Vbus_pk_Min - Vbus_pp/2#母线最低平均电压
#单周期内电容充电时间
Tc = 1/(4*Fi_AC) - asin((Vbus_pk_Min-Vbus_pp)/(Vbus_pk_Min))/(2*pi*Fi_AC)#电容充电时间
print("Tc = ",Tc*10**3,"ms")
Td = 1/Fi_AC/2 - Tc
print("Td = ",Td*10**3,"ms")
#母线电容
Cbus = 2*Pmax*(1/(2*Fi_AC) - Tc)/(eff*(Vbus_pk_Min**2 - (Vbus_pk_Min-Vbus_pp)**2))
print("Cbus = ",Cbus*10**6,"uF")



####################################
#整流桥计算
PF = 0.6 #功率因数
Ii_RMS_Max = Pmax/(eff * Vi_AC_RMS_Min * PF)#交流输入电流
print("Ii_RMS = ",Ii_RMS_Max,"A")
print("Vbus_pk_Max = ",Vbus_pk_Max,"V")
####################################
#匝比计算&VRCD计算
mos_VDS_max = 600 #mos耐压600V
k_vds = 0.8#降额系数

mos_VDS = mos_VDS_max * k_vds#mosVDS电压
print("mos应力=",mos_VDS,"v")

VRCD = mos_VDS - Vbus_pk_Max - 0.7
VOR = 0.7*VRCD

VRCD_Diod = VOR + Vbus_pk_Max

print("反射电压VOR=",VOR,"V")
print("RCD电压=",VRCD,"V")
print("RCD二极管应力=",VRCD_Diod,"V")
Nps = VOR/(Vo+0.7)#匝比
print("匝比=",Nps)

####################################
#变压器感量计算

Dmax = 0.45 #占空比
Fsw = 70 * 10**3 #频率
Krp = 1 #脉动系数，它等于一次侧电流脉动值与峰值电流的比值，CCM模式Krp<1
Ii_AVG_Max = Pmax/(eff * Vi_AC_RMS_Min)#线圈最大平均电流
print("电流平均值=",Ii_AVG_Max,"A")
Ipp = Ii_AVG_Max/(1-Krp+Krp/2)**Krp#电流脉动值
print("电流脉动值=",Ipp,"A")
Ii_pk = Ipp/Krp
print("电流峰值=",Ii_pk,"A")


#Lp = Vbus_AVG_Min*Dmax / (Fsw*Ipp) 
#print("计算得初级线圈电感量=",Lp * 10**3 ,"mH")

Z = 0.5#Z是副边损耗与总损耗的比例值。如果没有更好的参数信息，应当取Z=0.5。
Lp = Pmax /(Ii_pk**2 * Krp*(1-Krp/2)*Fsw) * ((Z*(1-eff)+eff)/eff)
print("初级线圈电感量=",Lp*10**6 ,"uH")

####################################
#磁芯估测选型
Sj = 0.15 * sqrt(Pmax) 
print("磁芯截面积估算为",Sj,"cm2","=",Sj*10**2,"mm2")


#AP法选磁芯，Ap = Aw*Ae
Kw = 0.35 #窗口利用率
J = 400 #电流密度A/cm2
Bmax = 0.2 #磁饱和
AP = 0.433*(1+eff)*Pmax/(eff*Kw*Dmax*J*Bmax*Krp*Fsw)*10**4
print("磁芯AP为",AP,"cm4")


#后面的要查表并实测磁芯后才可以继续
input("后面的要查表并实测磁芯后才可以继续")

Ae = 39.6 * 10**-6 #磁芯截面积
u0 = 1.26 * 10**-6 #空气磁导率
#实测磁芯
class mesuredMagCore :
    N1 = 20
    L1 = 780 * 10**-6 #在20匝时的电感量
    N2 = 63
    L2 = 778 * 10**-6 #磨气隙后在63匝时的电感量 

#计算气隙
def oth_calc_lg():
    AL = mesuredMagCore.L1*10**9/mesuredMagCore.N1**2#单位nH/N2
    lg = 40*pi*Ae*10**4*(Np**2/(1000*Lp*10**6) - 1/AL)
    print("气隙长度=",lg,"mm")
#oth_calc_lg()

#计算初级线圈匝数
Np = Lp*Ii_pk / (Bmax*Ae)
print("初级线圈匝数=",Np)

#磁饱和校验
def oth_calc_Bmax():
    Bmax = Lp*Ii_pk/(Np*Ae)
    print("最大磁感应强度Bmax=",Bmax,"T")
#####END###############################

#气隙计算
lg = (u0*Ae)*(Np**2 / Lp - mesuredMagCore.N1**2 / mesuredMagCore.L1)#气隙计算公式
print("气隙长度=",lg*10**3,"mm")






#oth_calc_Bmax()
#calc_Bmax_noGap()
#flybackTransformer_calc()
#testSympy()