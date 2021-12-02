import sys
import os
import subprocess
import shutil

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

if __name__ == "__main__":
    import subprocess
    import sys
    import os
    root = os.path.abspath("./")
    s_root = root + "/docs/out/stats/"
    p_root = root + "/docs/out/plots/"
    a_root = root+"/src/algoritmo_evolutivo.py"
    e_root = (root+"/docs/out/execs/")
    if len(sys.argv) == 4 and sys.argv[1] == "-o":
        f_dir = s_root + sys.argv[2]
        if os.path.exists(f_dir):
            ow = input("El archivo ya existente. ¿Sobreescribir archivo? (s/n)")
            if ow == "s":
                os.remove(f_dir)
                f_dir = p_root + sys.argv[2]
                os.remove(f_dir)
            else:
                print("Intentelo de nuevo con un nuevo archivo.")
                sys.exit(-1)
        for i in range(int(sys.argv[3])):
                subprocess.Popen(["python3",a_root, sys.argv[2]],stdout=open('/dev/null', 'w'))
    else:
        if len(sys.argv) < 2:
            f_dir = s_root + sys.argv[1]
            if os.path.exists(f_dir):
                ow = input("El archivo ya existente. ¿Sobreescribir archivo? (s/n)")
                if ow == "s":
                    os.remove(f_dir)
                    f_dir = p_root + sys.argv[1]
                    os.remove(f_dir)
                    subprocess.Popen(["python3",a_root, sys.argv[1]],stdout=open(e_root + "exec.txt",'w'))
                else:
                    print("Intentelo de nuevo con un nuevo archivo.")
                    sys.exit(-1)
            else:
                subprocess.Popen(["python3",a_root, sys.argv[1]],stdout=open(e_root + "exec.txt",'w'))
        else:
            if sys.argv[1] == "-d":
                if len(sys.argv) < 4:
                    r_dir = e_root + sys.argv[3] + "/"
                    if not os.path.exists(r_dir):
                        os.mkdir(r_dir)
                    else:
                        rmv = input("El directorio es existente. ¿Limpiar directorio? (s/n)")
                        if rmv == "s":
                            rm(r_dir)
                        else:
                            print("Intentelo de nuevo con un nuevo directorio.")
                            sys.exit(-1)
                    f_dir = s_root + sys.argv[2]
                    if os.path.exists(f_dir):
                        ow = input("El archivo ya existente. ¿Sobreescribir archivo? (s/n)")
                        if ow == "s":
                            os.remove(f_dir)
                            f_dir = p_root + sys.argv[2]
                            os.remove(f_dir)
                            subprocess.Popen(["python3",a_root, sys.argv[2]],stdout=open((r_dir+"exec.txt"),'w'))
                        else:
                            print("Intentelo de nuevo con un nuevo archivo.")
                            sys.exit(-1)
                else:
                    r_dir = e_root + sys.argv[4] + "/"
                    if not os.path.exists(r_dir):
                        os.mkdir(r_dir)
                    else:
                        rmv = input("El directorio es existente. ¿Limpiar direcotorio? (s/n)")
                        if rmv == "s":
                            rm(r_dir)
                        else:
                            print("Intentelo de nuevo con un nuevo directorio.")
                            sys.exit(-1)
                    f_dir = s_root + sys.argv[2]
                    if os.path.exists(f_dir):
                        ow = input("El archivo ya existente. ¿Sobreescribir archivo? (s/n)")
                        if ow == "s":
                            os.remove(f_dir)
                            f_dir = p_root + sys.argv[2]
                            os.remove(f_dir)
                        else:
                            print("Intentelo de nuevo con un nuevo archivo.")
                            sys.exit(-1)
                    for i in range(int(sys.argv[3])):
                        subprocess.Popen(["python3",a_root, sys.argv[2]],
                                            stdout=open((r_dir + "exec{}.txt".format(i+1)), 'w'))
            else:
                for i in range(int(sys.argv[2])):
                    subprocess.Popen(["python3",a_root, sys.argv[1]],
                                        stdout=open(e_root + "exec{}.txt".format(i+1), 'w'))