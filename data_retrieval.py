import numpy as np

rec_file = open("./Lab2./reta_passadeirapf5.txt", "r")
meas = rec_file.read()
name = "reta_p_pf_5"
meas = meas.split("SINGLE")

lat = []
long = []
alt = []
time = []

for i in range(len(meas)):
    if i == 0:
        pass
    else:
        # print(meas[i])
        print(i)
        aux = meas[i].split(" ")
        lat.append(aux[1])
        long.append(aux[2])
        alt.append(aux[3])
        aux = meas[i].split("iteration")
        aux = aux[1]
        aux = aux.split(" ")
        aux = aux[2]
        aux = aux[:15] 
        time.append(aux)

    ()

# print(lat)
# print(long)
# print(alt)
# print(time)

pack=[i for i in zip(lat, long, alt, time)]
pack = np.asarray(pack)
# print(pack)
np.save(name,pack)

# print(meas[24])
# print(meas[24].split(" "))
# print(len(meas))
# print(log[0])
# print(log[0])
# print(log[0])
# print(log[0])
# print(log[0])
# print(log[0])
# print(log[2])
# print(log[1])
# print(log[30])
# print(log[15000])
# print(log)