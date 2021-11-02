# Implementacion de un algoritmo evolutivo genético

dado la siguiente funcion:
> f($x_{1}$, $x_{2}$) = 418.9829*2 - $x_{1} * sin(\sqrt{|x_{1}|)})$ - $x_{2}*sin(\sqrt{|x_{2}|})$

En un dominio de [-500, 500] para cada variable, se pretende mediante un algoritmo genetico con los siguientes operadores/representaciones:
* Representacion: Real *
* Selección de padres: Ruleta *
* Escalamiento: Jerarquías no lineales -
* Cruza: De un punto *
* Mutación: Inversión de un bit *
* Selección: Más *

### Pre-requisitos 📋

Se requiere la biblioteca [numpy](https://numpy.org/install/) para instalar en Linux:
```bash
pip3 install numpy
```
Opcional:
Se requiere la biblioteca [matplotlib](https://pypi.org/project/matplotlib/) para instalar en Linux:
```bash
pip3 install matplotlib
```

# Resultados
Con los siguientes datos 
* nvars= 2
* lb = -500*np.ones(nvars)
* ub = 500*np.ones(nvars)
* pc = 0.9    
* pm = 0.5
* npop = 6
* ngen = 2
* q = 0.5

Tenemos los siguientes resultados
## Ejecución mínima
> 971.3843147142522
## Promedio de los resultados
> 1230.7871657784322
## Gráfica
![Alt text](grafica.png?raw=true "Title")