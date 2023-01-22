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


[curva,pf_curva,reta,pf_reta,pi_reta,pf_pass] = get_data()


true_pi_reta = [38.73799549745399, -9.138472338872601]
true_pf_reta = [38.73795591274537, -9.138953366340852]
true_pf_curva = [38.73790047032445, -9.13911362832949]
true_pf_pass = [38.73755264660175, -9.139080771269057]

true_reta = get_true_points("./Lab2./reta_e.csv")
true_curva = get_true_points("./Lab2./curva_e.csv")




print(true_curva)