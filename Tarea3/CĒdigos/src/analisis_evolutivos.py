import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import shutil

def data(file):
    data = {}
    max = []
    min = []
    mean = []
    median = []
    std = []
    for line in file:
        l = line.split(" ")
        if l[0] == "max":
            max.append(float(l[1]))
        if l[0] == "min":
            min.append(float(l[1]))
        if l[0] == "mean":
            mean.append(float(l[1]))
        if l[0] == "median":
            median.append(float(l[1]))
        if l[0] == "std":
            std.append(float(l[1]))
    data['max'] = max
    data['min'] = min
    data['mean'] = mean
    data['median'] = median
    data['std'] = std
    return data

def str_data(data):
    n = len(data['max'])
    s = "max      min      mean      median      std\n"
    for i in range(n):
        s += "{}\t{}\t{}\t{}\t{}\n".format(data['max'][i],
                                           data['min'][i],
                                           data['mean'][i],
                                           data['median'][i],
                                           data['std'][i])
    return s
if __name__ == "__main__":
    import sys
    import os

    root = os.path.abspath("./")
    p_root = root + "/docs/out/stats/"
    flag_f = False
    if len(sys.argv) == 3:
        if sys.argv[1] == "-f":
            flag_f = True
            file_data_name = os.path.join(p_root,sys.argv[2])
            f = sys.argv[2].split(".")
            file_out = os.path.join(p_root,f[0]+"_analisis."+f[1])
        else:
            print("Mal uso de stdin lea Readme para ver el uso de stdin.")
            exit(-1)
    else:
        file_data_name = os.path.join(p_root,sys.argv[1])
        file_out = None
    file = open(file_data_name,'r')
    data = data(file)
    file.close()
    out = "Estadisticas sobre todas las ejecuciones del evolutivo.\n"
    out += "max\t{}\nmin\t{}\nmean\t{}\nmedian\t{}\nstd:\n".format(np.max(np.array(data['max'])),
                                                                   np.min(np.array(data['min'])),
                                                                   np.mean(np.array(data['mean'])),
                                                                   np.median(np.array(data['median'])))
    out += "\tmax: {}\n\tmin: {}\n\tmean: {}\n\tmedian: {}\n".format(np.max(np.array(data['std'])),
                                                                     np.min(np.array(data['std'])),
                                                                     np.mean(np.array(data['std'])),
                                                                     np.median(np.array(data['std'])))
    out += str_data(data)
    if flag_f:
        f_out = open(file_out,'w')
        f_out.write(out)
        f_out.flush()
        f_out.close()
    else:
        print(out)