import numpy as np
import math
from matplotlib import pyplot as plt
import statistics

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
    
    return vect

def get_points(vect,c_to_x,c_to_y,ref):
    pts = []
    l = len(vect)
    w=0

    if not(l>11):
        for i in range(l):
            try:
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
            except:
                if w==0:
                    aux = [0,0]
                    aux[0]= c_to_x[0]*(vect[0] - float(ref[0])) + c_to_x[1]*(vect[1] - float(ref[1]))
                    aux[1]= c_to_y[0]*(vect[0] - float(ref[0])) + c_to_y[1]*(vect[1] - float(ref[1]))
                    w = w+1
                    pts.append(aux)
                    pts = pts[0]
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

    long_dif_1 = float(ref[1][1])- float(ref[0][1])
    lat_dif_1 = float(ref[1][0]) - float(ref[0][0])
    long_dif_2 = float(ref[2][1])- float(ref[1][1])
    lat_dif_2 = float(ref[2][0]) - float(ref[1][0])

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

def get_ref_points():
    pi_r = [38.73798483325617, -9.138458445668222]
    pf_r = [38.73794851377695, -9.138959453848711]
    pf_c = [38.73789914742897, -9.139118183872123]
    pf_p = [38.73755264660175, -9.139080771269057]
    ref_d = [[0,33.63],[-9.78,0]]
    r = get_true_points("./Lab2./reta_e.csv")
    c = get_true_points("./Lab2./curva_e.csv")
    ref_p = get_true_points("./Lab2./reference.csv")
    
    return [pi_r,pf_r,pf_c,pf_p,ref_d,r,c,ref_p]

def get_stats(vect):
    x=[]
    y=[]
    for i in range(len(vect)):
        x.append(float(vect[i][0]))
        y.append(float(vect[i][1]))
    mean_x = statistics.fmean(x)
    mean_y = statistics.fmean(y)

    std_x = statistics.stdev(x)
    std_y = statistics.stdev(x)

    mean = [mean_x,mean_y]
    std = [std_x,std_y]

    return [mean,std]

def get_plot(vec1,vec2,tvec1,tvec2,mean,type):
    """Type 0: 1 true point
       Type 1: 1 vect of true points
       Type 2: 2 vects of true points
       Type 3: 1 true point + mean"""

    if (type==0):
        x=[]
        y=[]

        for i in range(len(vec1)):
            x.append(float(vec1[i][0]))
            y.append(float(vec1[i][1]))
        
        plt.plot(x,y,"ro")
        plt.plot(tvec1[0],tvec1[1],"bo")
        plt.show()
    
    elif (type==1):
        x=[]
        y=[]

        for i in range(len(vec1)):
            x.append(float(vec1[i][0]))
            y.append(float(vec1[i][1]))

        xt=[]
        yt=[]
        for i in range(len(tvec1)):
            xt.append(float(tvec1[i][0]))
            yt.append(float(tvec1[i][1]))
        
        plt.plot(x,y,"ro")
        plt.plot(xt,yt)
        plt.show()
    
    elif (type==2):
        x=[]
        y=[]

        for i in range(len(vec1)):
            x.append(float(vec1[i][0]))
            y.append(float(vec1[i][1]))

        for i in range(len(vec2)):
            x.append(float(vec2[i][0]))
            y.append(float(vec2[i][1]))

        xt=[]
        yt=[]
        for i in range(len(tvec1)):
            xt.append(float(tvec1[i][0]))
            yt.append(float(tvec1[i][1]))

        for i in range(len(tvec2)):
            xt.append(float(tvec2[i][0]))
            yt.append(float(tvec2[i][1]))

        plt.plot(x,y,"ro")
        plt.plot(xt,yt)
        plt.show()
    
    elif (type==3):
        x=[]
        y=[]

        for i in range(len(vec1)):
            x.append(float(vec1[i][0]))
            y.append(float(vec1[i][1]))

        plt.plot(x,y,"ro")
        plt.plot(tvec1[0],tvec1[1],"bo")
        plt.plot(mean[0],mean[1],"go")
        plt.show()
    
    else:
        print("Invalid plot type")
        exit()

    return


[curva,pf_curva,reta,pf_reta,pi_reta,pf_pass] = get_data()

[true_pi_reta,true_pf_reta,true_pf_curva,true_pf_pass,
ref_dist,true_reta,true_curva,ref_points] = get_ref_points()

[coord_to_x,coord_to_y] = get_transf(ref_points,ref_dist[0],ref_dist[1])

pi_reta_xy = get_points(pi_reta,coord_to_x,coord_to_y,true_pi_reta)
pf_reta_xy = get_points(pf_reta,coord_to_x,coord_to_y,true_pi_reta)
pf_curva_xy = get_points(pf_curva,coord_to_x,coord_to_y,true_pi_reta)
pf_pass_xy = get_points(pf_pass,coord_to_x,coord_to_y,true_pi_reta)
reta_xy = get_points(reta,coord_to_x,coord_to_y,true_pi_reta)
curva_xy = get_points(curva,coord_to_x,coord_to_y,true_pi_reta)


true_pi_reta_xy = get_points(true_pi_reta,coord_to_x,coord_to_y,true_pi_reta)
true_pf_reta_xy = get_points(true_pf_reta,coord_to_x,coord_to_y,true_pi_reta)
true_pf_curva_xy = get_points(true_pf_curva,coord_to_x,coord_to_y,true_pi_reta)
true_pf_pass_xy = get_points(true_pf_pass,coord_to_x,coord_to_y,true_pi_reta)
true_reta_xy = get_points(true_reta,coord_to_x,coord_to_y,true_pi_reta)
true_curva_xy = get_points(true_curva,coord_to_x,coord_to_y,true_pi_reta)


[mean_pi_r,std_pi_r] = get_stats(pi_reta_xy)
[mean_pf_r,std_pf_r] = get_stats(pf_reta_xy)
[mean_pf_c,std_pf_c] = get_stats(pf_curva_xy)
[mean_pf_p,std_pf_p] = get_stats(pf_pass_xy)

print(reta)

get_plot(reta_xy,0,true_reta_xy,0,0,1)