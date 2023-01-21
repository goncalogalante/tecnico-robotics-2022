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
    a = load_vect(basename + "curva_e_",10,36)
    b = load_vect(basename + "curva_e_pf_",5,21)
    c = load_vect(basename + "reta_e_",8,57)
    d = load_vect(basename + "reta_e_pf_",5,17)
    e = load_vect(basename + "reta_e_pi_",4,15)
    f = load_vect(basename + "reta_p_pf_",5,20)

    return [a,b,c,d,e,f]


def get_points(vect):
    ()


[curva,pf_curva,reta,pf_reta,pi_reta,pf_pass] = get_data()


true_pi_reta = [38.73799549745399, -9.138472338872601, 81]
true_pf_reta = [38.73795591274537, -9.138953366340852, 81]
true_pf_curva = [38.73790047032445, -9.13911362832949, 81]
true_pf_pass = [38.73755264660175, -9.139080771269057, 81]

print(pi_reta[0])