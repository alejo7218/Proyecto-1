# Simulador de Movimiento Parabólico

## Descripción
Este proyecto es una simulación avanzada del **movimiento parabólico** de un proyectil en 2D, considerando la **aceleración gravitatoria**. Implementa una estructura **orientada a objetos** con clases abstractas e interfaces que representan objetos físicos en movimiento.

El simulador ofrece tanto soluciones analíticas como numéricas para el movimiento parabólico, permitiendo comparar ambos enfoques. Al ejecutar el programa, el usuario puede especificar las condiciones iniciales de diversas formas (velocidad y ángulo, altura y alcance, etc.) y la simulación calcula y visualiza la trayectoria completa.

## Características
✔️ Simulación del movimiento parabólico mediante **métodos analíticos y numéricos**.  
✔️ Cálculo preciso de **alcance horizontal**, **altura máxima** y **tiempo de vuelo**.  
✔️ **Flexibilidad en la entrada de datos**: múltiples formas de definir las condiciones iniciales.  
✔️ Representación **gráfica detallada** de la trayectoria con marcadores de puntos clave.  
✔️ Implementación robusta con **Programación Orientada a Objetos (POO)**.  
✔️ Uso de **clases abstractas** e **interfaces** para mayor extensibilidad.  
✔️ Implementación de **decoradores** para medir el rendimiento.  
✔️ Estructura modularizada y generalizable a otros problemas físicos.

## Fundamentos Matemáticos
El movimiento parabólico de un proyectil se describe mediante las siguientes ecuaciones:

### Posición en función del tiempo:
$$
x(t) = x_0 + v_{0x} t
$$
$$
y(t) = y_0 + v_{0y} t - \frac{1}{2} g t^2
$$

### Velocidad en función del tiempo:
$$
v_x = v_{0x}
$$
$$
v_y = v_{0y} - g t
$$

### Tiempo de vuelo:
$$
t_f = \frac{2 v_{0y}}{g}
$$

### Alcance horizontal:
$$
R = v_{0x} t_f = \frac{v_0^2 \sin(2\theta)}{g}
$$

### Altura máxima:
$$
h_{\max} = \frac{v_{0y}^2}{2g} = \frac{v_0^2 \sin^2(\theta)}{2g}
$$

## Estructura del Código

### Clases Principales:

- **ObjetoFisico (ABC)**: Clase abstracta base para objetos físicos.
- **Movible (ABC)**: Interfaz para objetos que pueden actualizar su posición.
- **Proyectil**: Implementa un proyectil con comportamiento de movimiento parabólico.
- **Simulacion**: Maneja la simulación y visualización del movimiento.

### Métodos Clave:

- **calcular_componentes()**: Calcula los componentes vectoriales del movimiento.
- **actualizar_posicion()**: Actualiza la posición del proyectil usando el método numérico.
- **posicion_analitica()**: Calcula la posición exacta usando ecuaciones analíticas.
- **calcular_parametros_iniciales()**: Calcula velocidad inicial y ángulo según diferentes casos.
- **graficar()**: Visualiza la trayectoria con información detallada.

### Decoradores:

- **tiempo_ejecucion**: Mide y muestra el tiempo de ejecución de una función.

## Requisitos
- **Python 3.6+**
- Librerías necesarias:
  - `matplotlib`
  - `math`
  - `time`

El programa le pedirá seleccionar un caso para ingresar datos:

1. **Velocidad inicial y ángulo conocidos**
2. **Altura máxima y tiempo de vuelo conocidos**
3. **Altura máxima y alcance conocidos**
4. **Tiempo de vuelo y alcance conocidos**

Dependiendo del caso seleccionado, ingrese los valores solicitados. Luego podrá elegir entre usar el método analítico o numérico para la simulación.

## Extensibilidad

El proyecto está diseñado para ser fácilmente extendido a otros problemas físicos:

1. **Nuevos tipos de movimiento**: Cree nuevas clases que hereden de `ObjetoFisico` y `Movible` para implementar diferentes tipos de movimiento.
2. **Diferentes fuerzas**: Modifique la implementación de `actualizar_posicion()` para incluir otras fuerzas como resistencia del aire.
3. **Diversos contextos físicos**: Ajuste el valor de la gravedad para simular el movimiento en diferentes planetas.
