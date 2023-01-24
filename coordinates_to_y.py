import numpy as np
import math
from matplotlib import pyplot as plt

# estimativa de distância percorrida em cada percurso
# estimativa da posição em cada ponto de cada percurso consoante as medidas
# trajetória real em cada percurso


def load_vect(name,n,max):
    vect = []

    for i in range(n):
        vect.append(0)

    for i in range(n+1):
        if i==0:
            pass
        else:
            try:
                # vect[i-1] = np.load(name + str(i) + ".npy") 
                aux = np.load(name + str(i) + ".npy")
                s = aux.shape
                # print(s)
                z = max-s[0]
                # print(z)
                z = np.zeros((z,4))
                # print(z)
                # print(aux)
                aux = np.append(aux,z)
                aux = np.resize(aux,(max,4))
                # print(aux.shape)
                # print(vect[i-1].shape)
                vect[i-1] = aux
            except:
                print("Wrong file name")
                exit()

    return vect


def get_data():
    basename = "./Lab2./Dados./"
    c_e = load_vect(basename + "curva_e_",10,36)
    c_e_pf = load_vect(basename + "curva_e_pf_",5,21)
    r_e = load_vect(basename + "reta_e_",8,57)
    r_e_pf = load_vect(basename + "reta_e_pf_",5,17)
    r_e_pi = load_vect(basename + "reta_e_pi_",4,15)
    r_p_pf = load_vect(basename + "reta_p_pf_",5,20)

    return [c_e,c_e_pf,r_e,r_e_pf,r_e_pi,r_p_pf]


def get_true_points(name):
    rec_file = open(name, "r")
    vect = rec_file.read()
    vect = vect.split("\n")
    for i in range(len(vect)):
        vect[i] = vect[i].split(",")
    
    vect[len(vect)-1]=[0,0]

    # aux = vect[0][0]
    # vect[0] = [0,0]
    # vect[0][0]=aux
    # vect[0][1]=vect[1][0]
    # for i in range(len(vect)):
    #     if i==0:
    #         pass
    #     elif not(vect[i][1]==""):
    #         print(i)
    #         vect[i][0]=vect[i][1]
    #         vect[i][1]=vect[i+1][0]
    #     else:
    #         vect[i]=[0,0]
    #     ()
    
    return vect


def get_points(vect,c_to_x,c_to_y,ref):
    pts = []
    l = len(vect)

    if not(l>11):
        for i in range(l):
            for k in range(len(vect[i])):
                if not(vect[i][k][2]=="0.0"):
                    aux = [0,0]
                    aux[0] = c_to_x[0]*(float(vect[i][k][0]) - float(ref[0])) + c_to_x[1]*(float(vect[i][k][1]) - float(ref[1]))
                    aux[1] = c_to_y[0]*(float(vect[i][k][0]) - float(ref[0])) + c_to_y[1]*(float(vect[i][k][1]) - float(ref[1]))
                    vect[i][k][0] = aux[0]
                    vect[i][k][1] = aux[1]

                    pts.append(vect[i][k])
                else:
                    pass
    else:
        for i in range(l):
            if not(vect[i][1]==0):
                aux = [0,0]
                aux[0] = c_to_x[0]*(float(vect[i][0]) - float(ref[0])) + c_to_x[1]*(float(vect[i][1]) - float(ref[1]))
                aux[1] = c_to_y[0]*(float(vect[i][0]) - float(ref[0])) + c_to_y[1]*(float(vect[i][1]) - float(ref[1]))
                vect[i][0] = aux[0]
                vect[i][1] = aux[1]

                pts.append(vect[i])
            else:
                pass             
    return pts



def get_transf(ref,dist1,dist2):

    long_dif_1 = float(ref[1][0])-float(ref[0][0])
    lat_dif_1 = float(ref[1][1]) - float(ref[0][1])
    long_dif_2 = float(ref[2][0])-float(ref[1][0])
    lat_dif_2 = float(ref[2][1]) - float(ref[1][1])

    aux = long_dif_1*lat_dif_2*(-1)
    aux = aux/lat_dif_1
    aux = aux + long_dif_2
    long_to_x = float(dist2[0])/aux - float(dist1[0])/lat_dif_1*lat_dif_2

    aux = aux*lat_dif_1
    aux = long_dif_1/aux
    lat_to_x = (-1)*float(dist2[0])*aux + float(dist1[0])/lat_dif_1


    aux = long_dif_2*lat_dif_1*(-1)
    aux = aux/lat_dif_2
    aux = aux + long_dif_1
    long_to_y = float(dist1[1])/aux - float(dist2[1])/lat_dif_2*lat_dif_1

    aux = aux*lat_dif_2
    aux = long_dif_2/aux
    lat_to_y = (-1)*float(dist1[1])*aux + float(dist2[1])/lat_dif_1

    return [[lat_to_x,long_to_x],[lat_to_y,long_to_y]]




[curva,pf_curva,reta,pf_reta,pi_reta,pf_pass] = get_data()


true_pi_reta = [38.73799549745399, -9.138472338872601]
true_pf_reta = [38.73795591274537, -9.138953366340852]
true_pf_curva = [38.73790047032445, -9.13911362832949]
true_pf_pass = [38.73755264660175, -9.139080771269057]
ref_dist = [[0,33.63],[-9.78,0]]

true_reta = get_true_points("./Lab2./reta_e.csv")
true_curva = get_true_points("./Lab2./curva_e.csv")
ref_points = get_true_points("./Lab2./reference.csv")

# print(true_reta)

[coord_to_x,coord_to_y] = get_transf(ref_points,ref_dist[0],ref_dist[1])

pi_reta = get_points(reta,coord_to_x,coord_to_y,true_pi_reta)

true_reta = get_points(true_reta,coord_to_x,coord_to_y,true_pi_reta)


print(len(pi_reta))
x=[]
y=[]
for i in range(len(pi_reta)):
    # print(pi_reta[i])
    x.append(float(pi_reta[i][0]))
    y.append(float(pi_reta[i][1]))

xt=[]
yt=[]
for i in range(len(true_reta)):
    print(true_reta[i])
    xt.append(float(true_reta[i][0]))
    yt.append(float(true_reta[i][1]))


plt.plot(x,y,"ro")
plt.plot(xt,yt)
# plt.ylim(0, 14)
plt.show()