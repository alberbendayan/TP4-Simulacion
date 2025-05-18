<h1 align="center">Simulación de Sistemas</h1>
<h3 align="center">TP4: Dinámica Molecular regida por el paso temporal</h3>
<h4 align="center">Primer cuatrimestre 2025</h4>

# Requisitos

* Java versión 21: Para correr el simulador
* Maven: Para compilar el proyecto de Java
* Python ([versión 3.12.9](https://www.python.org/downloads/release/python-3129/)): Para los gráficos
* [UV](https://github.com/astral-sh/uv): Administrador de dependencias para
Python

# Instalando las dependencias

```sh
# Si python 3.12.9 no esta instalado se puede instalar haciendo
uv python install 3.12.9

# Para crear y activar el entorno virtual
uv venv
source .venv/bin/activate  # En Unix
.venv\Scripts\activate     # En Windows

# Para instalar las dependencias
uv sync
```

# Compilando el proyecto

Desde la consola, para compilar el proyecto de **Java**, desde la raíz del
proyecto, correr:

```bash
mvn clean package
```

# Ejecución de la simulación

El proyecto cuenta con dos motores de simulación en Java. Estos representan la
simulación de un oscilador armónico simple y la de un sistema de osciladores
acoplados.

Para correr cada uno simplemente correr:

```bash
java -classpath target/classes ar.edu.itba.ss.<simulacion>.Main PARAM1=X PARAM2=Y ...
```

Donde `<simulacion>` es alguna de las opciones:

- `single`: Para el oscilador armónico simple
- `coupled`: Para el oscilador acoplado

Se le puede especificar una serie de parámetros opcionales para sobrescribir los
valores tomados por defecto. Estos valores son:

- `DT`: diferencial de tiempo
- `T_MAX`: tiempo máximo de la simulación
- `M`: masa de la partícula
- `K`: constante elastica
- `GAMMA`: constante de amortiguamiento
- `X0`: posición inicial
- `V0`: velocidad inicial
- `OMEGA`: velocidad angular
- `N`: cantidad de partículas

# Postprocesamiento

Todo el postprocesamiento se realiza a través de scripts de Python y se corren
de la siguiente manera:

```bash
uv run -m ejX.<module> [args]
```

donde `X` es el número del ejercicio (1 o 2), `<module>` es alguno de los
módulos que se desea correr.

Para `X=1`:

- `comparacion_integradores`
- `ecm_integradores`
- `ecm_vs_dt`

Para `X=2`:

- `animacion`
- `amplitud_maxima_vs_t`
- `amplitud_maxima_vs_w`
- `w_vs_k`
