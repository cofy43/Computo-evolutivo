import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import shutil

from numpy.lib.function_base import append


def rm(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def data(file):
    data = {}
    all_data = []
    x = []
    y = []
    for line in file:
        if line ==  ">\n":
            data['x'] = x.copy()
            data['y'] = y.copy()
            all_data.append(data)
            x = []
            y = []
            data = {}
        else:
            l = line.split("\t")
            x.append(int(l[0]))
            y.append(float("{:.4f}".format(float(l[1]))))
    return all_data
    


def plot(data,file):
    plt.plot('x','y','',label="Evolutivo {}".format(i+1),data=data)
    plt.ylabel('Median')
    plt.xlabel('Generaciones')
    plt.legend(loc='upper right')
    plt.savefig(file)
    plt.close()


if __name__ == "__main__":
    import sys
    import os

    root = os.path.abspath("./")
    p_root = root + "/docs/out/plots/"
    r_dir = p_root
    file_data_name = sys.argv[1]
    plot_name_file = os.path.join(p_root,sys.argv[1])
    scale_x = 5
    scale_y = 500
    if len(sys.argv) == 3:
        file_data_name = sys.argv[2]
        plot_name_file = os.path.join(p_root,sys.argv[2])
        r_dir = os.path.join(p_root,sys.argv[2].split(".")[0])
        if not os.path.exists(r_dir):
            os.mkdir(r_dir)
        else:
            rmv = input("El directorio es existente. ¿Limpiar direcotorio? (s/n)")
            if rmv == "s":
                rm(r_dir)
            else:
                print("Intentelo de nuevo con un nuevo directorio.")
                sys.exit(-1)
    plot_file = open(plot_name_file,'r')
    data = data(plot_file)
    for i in range(len(data)):
        d = data[i]
        file = os.path.join(r_dir,"plot{}.png".format(i+1))
        plot(d,file)
    plot_file.close()
    plot_file = open(plot_name_file,'r')
    for i in range(len(data)):
        d = data[i]
        if len(data) <= 20:
            plt.plot('x','y','',label="Evolutivo {}".format(i+1),data=d)
        else:
            plt.plot('x','y','',data=d)
        plt.yscale("linear")
        plt.xscale("linear")
        #plt.xticks(np.arange(min(np.array(d['x']))-scale_x, max(np.array(d['x']))+scale_x, scale_x))
        #plt.yticks(np.arange(min(np.array(d['y']))-scale_y, max(np.array(d['y']))+scale_y, scale_y))
        plt.ylabel('Median')
        plt.xlabel('Generaciones')
    if len(data) <= 20:
        plt.legend(bbox_to_anchor=(1, 0.5), loc='center left', borderaxespad=0.)
    file = os.path.join(r_dir,"plot.png")
    plt.tight_layout()
    plt.savefig(file,bbox_inches="tight")
    plt.show()
    plt.close()
    plot_file.close()
