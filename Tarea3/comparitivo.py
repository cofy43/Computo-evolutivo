# Comparativa entre dos algoritmos evolutivos
# Utilizando la prueba de Wilcoxon rank sum
from genetico import EA, fa
from evolutivo_simple import algoritmo_evolutivo
from problemas import fa, parallelFa
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import stats
np.random.seed(42)

nvars= 2
lb = -500*np.ones(nvars)
ub = 500*np.ones(nvars)
pc = 0.9    
pm = 0.5
npop = 10
ngen = 10000
q = 0.5
ejecucionMinima = False
guardar_resultados = False
np.set_printoptions(formatter={'float': '{0: 0.6f}'.format})

#Los evolutivos en eggholder
s1 = EA(fa, lb, ub, pc, pm, nvars, npop, ngen, q, ejecucionMinima, guardar_resultados, 0)[0] #Salida de algoritmo de Tarea 2
s2 = algoritmo_evolutivo(parallelFa, lb, ub, pc, pm, nvars, npop, ngen)[0] #Salida de algoritmo de Tarea 3
print("np.mean(s1)")
print(s1)
print("np.mean(s2)")
print(s2)


fig1, ax1 = plt.subplots()
ax1.hist(np.concatenate((s1, s2)), bins = 50)
plt.show()

fig2, ax2 = plt.subplots()
ax2.boxplot(np.concatenate((s1, s2)))
plt.show()
print("temina con las gráficas")
print(stats.ranksums(s1, s2, alternative='two-sided'))
print(stats.ranksums(s1, s2, alternative='less'))
print(stats.ranksums(s1, s2, alternative='greater'))


x = stats.ranksums(s1, s2, alternative='less')
if stats.ranksums(s1, s2, alternative='less').pvalue <= 0.05:
    print('Gana s1')
elif stats.ranksums(s2, s1, alternative='less').pvalue <= 0.05:
    print('Gana s2')
else:
    print('Empate')