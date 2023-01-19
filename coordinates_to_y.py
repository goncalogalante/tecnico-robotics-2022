import numpy as np
import math

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

basename = "./Lab2./Dados./"
curva = load_vect(basename + "curva_e_",10,36)
pf_curva = load_vect(basename + "curva_e_pf_",5,21)
reta = load_vect(basename + "reta_e_",8,57)
pf_reta = load_vect(basename + "reta_e_pf_",5,17)
pi_reta = load_vect(basename + "reta_e_pi_",4,15)
pf_pass = load_vect(basename + "reta_p_pf_",5,20)

