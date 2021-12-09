## Tarea 3
Desarrollar un algoritmo evolutivo en Python con las siguientes características:
 * Seleccionar los componentes básicos del evolutivo
    Representación: Punto flotante Real
    Escalamiento: Escalamiento Sigma
    Selección de padres: Muestreo determinístico
    Cruza: Intermedia
    Mutación: uniforme
    Selección: Más
    Elitismo: 
 * Seleccionar al menos dos técnicas avanzadas
    * Paralelismo *
    * Coevolución
    * Metamodelos
    * Técnicas de diversidad *
    * Meméticos
    * Hiper heurísticas 
 * Aplicar el evolutivo a los siguientes 5 problemas con n=10
    * Rastrigin --
    * Ackley --
    * Rosenbrock --
    * Eggholder --
    * Easom --
 * Realizar un estudio comparativo entre el algoritmo desarrollado en la tarea 2 y el diseñado en está tarea utilizando hasta 10mil evaluaciones de función utilizando la prueba de Wilcoxon rank sum
 * Los parametros del nuevo evolutivo deben estar optimizados con iRace
 *  Resultados promediados de 20 ejecuciones del algoritmo. Soluciones mínima, media, máxima y desviación estándar. Usar mismos parámetros para las 20 ejecuciones y reportarlos. Se debe generar un archivo por cada ejecución del algoritmo
 * Reportar gráfica de convergencia. Eje x número de generaciones, eje y mediana de la mejor aptitud de cada generación
 * PDF con los resultados de la ejecución mínima, resultados promediados, gráfica de convergencia y estimación de tamaño del espacio de búsqueda

# Dependencias:
Se requie la paquetería [Joblib](https://pypi.org/project/joblib/) para llevar a cabo la tarea de paralización
```bash
pip3 install joblib
```

Se requie la paquetería [Scipy](https://pypi.org/project/scipy/) para llevar a cabo la tarea de paralización
```bash
pip3 install scipy
```

Se requie la paquetería [Matplotlib](https://pypi.org/project/matplotlib/) para la generación de gráficas
```bash
pip3 install matplotlib
```