import time
import math
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

class ObjetoFisico(ABC):
    """
    Clase abstracta que define los métodos generales para cualquier objeto en movimiento.
    """
    @abstractmethod
    def calcular_componentes(self):
        pass

class Movible(ABC):
    """
    Interfaz que define la actualización de la posición de un objeto en movimiento.
    """
    @abstractmethod
    def actualizar_posicion(self):
        pass

class Proyectil(ObjetoFisico, Movible):
    """
    Clase que modela un proyectil en movimiento parabólico sin resistencia del aire.
    """
    def __init__(self, velocidad_inicial, angulo, dt=0.01):
        self._velocidad_inicial = velocidad_inicial
        self._angulo = math.radians(angulo)
        self._dt = dt
        self._x = 0
        self._y = 0
        self._vx = velocidad_inicial * math.cos(self._angulo)
        self._vy = velocidad_inicial * math.sin(self._angulo)
        self._gravedad = 9.81
        
        # Calculamos inmediatamente los valores analíticos
        self._tiempo_vuelo = (2 * self._vy) / self._gravedad
        self._altura_maxima = (self._vy ** 2) / (2 * self._gravedad)
        self._alcance = (self._vx * self._tiempo_vuelo)

    @property
    def velocidad_inicial(self):
        return self._velocidad_inicial
    
    @velocidad_inicial.setter
    def velocidad_inicial(self, valor):
        if valor <= 0:
            raise ValueError("La velocidad inicial debe ser positiva")
        self._velocidad_inicial = valor
        # Actualizar componentes dependientes
        self._vx = self._velocidad_inicial * math.cos(self._angulo)
        self._vy = self._velocidad_inicial * math.sin(self._angulo)
        self._recalcular_parametros()
    
    @property
    def angulo(self):
        return math.degrees(self._angulo)
    
    @angulo.setter
    def angulo(self, valor):
        self._angulo = math.radians(valor)
        # Actualizar componentes dependientes
        self._vx = self._velocidad_inicial * math.cos(self._angulo)
        self._vy = self._velocidad_inicial * math.sin(self._angulo)
        self._recalcular_parametros()
    
    @property
    def dt(self):
        return self._dt
    
    @dt.setter
    def dt(self, valor):
        if valor <= 0:
            raise ValueError("El paso de tiempo debe ser positivo")
        self._dt = valor
    
    @property
    def vx(self):
        return self._vx
    
    @property
    def vy(self):
        return self._vy
    
    @property
    def gravedad(self):
        return self._gravedad
    
    @gravedad.setter
    def gravedad(self, valor):
        if valor <= 0:
            raise ValueError("La gravedad debe ser positiva")
        self._gravedad = valor
        self._recalcular_parametros()

    def _recalcular_parametros(self):
        """
        Método privado para recalcular los parámetros derivados cuando cambian los valores base
        """
        self._tiempo_vuelo = (2 * self._vy) / self._gravedad
        self._altura_maxima = (self._vy ** 2) / (2 * self._gravedad)
        self._alcance = (self._vx * self._tiempo_vuelo)

    def calcular_componentes(self):
        return self._vx, self._vy
    
    @property
    def posicion(self):
        return self._x, self._y
    
    def actualizar_posicion(self):
        """
        Método numérico para actualizar la posición
        """
        self._x += self._vx * self._dt
        self._vy -= self._gravedad * self._dt
        self._y += self._vy * self._dt
        return self._x, self._y
    
    def posicion_analitica(self, t):
        """
        Calcula la posición exacta usando las ecuaciones analíticas del movimiento parabólico
        """
        x = self._vx * t
        y = self._vy * t - 0.5 * self._gravedad * t**2
        return x, y
    
    def calcular_tiempo_altura_maxima(self):
        """
        Retorna el tiempo en que se alcanza la altura máxima
        """
        return self._vy / self._gravedad
        
    def calcular_tiempo_vuelo(self):
        """
        Retorna el tiempo de vuelo calculado con la fórmula analítica
        """
        return self._tiempo_vuelo
    
    def calcular_altura_maxima(self):
        """
        Retorna la altura máxima calculada con la fórmula analítica
        """
        return self._altura_maxima
    
    def calcular_alcance(self):
        """
        Retorna el alcance calculado con la fórmula analítica
        """
        return self._alcance

class Simulacion:
    """
    Clase que maneja la simulación del proyectil y la representación gráfica.
    """
    def __init__(self, proyectil, usar_analitico=True):
        self._proyectil = proyectil
        self._trayectoria = []
        self._trayectoria_analitica = []
        self._usar_analitico = usar_analitico
    
    @property
    def proyectil(self):
        return self._proyectil
    
    @proyectil.setter
    def proyectil(self, nuevo_proyectil):
        if not isinstance(nuevo_proyectil, Proyectil):
            raise TypeError("El objeto debe ser de tipo Proyectil")
        self._proyectil = nuevo_proyectil
        self._trayectoria = []
        self._trayectoria_analitica = []
    
    @property
    def usar_analitico(self):
        return self._usar_analitico
    
    @usar_analitico.setter
    def usar_analitico(self, valor):
        self._usar_analitico = bool(valor)
    
    @property
    def trayectoria(self):
        return self._trayectoria
    
    @property
    def trayectoria_analitica(self):
        return self._trayectoria_analitica
    
    @staticmethod
    def tiempo_ejecucion(func):
        def wrapper(*args, **kwargs):
            inicio = time.time()
            resultado = func(*args, **kwargs)
            fin = time.time()
            print(f"Tiempo de ejecución: {fin - inicio:.4f} s")
            return resultado
        return wrapper
    
    def simular_numerico(self):
        """
        Simula el movimiento del proyectil usando el método numérico
        """
        self._trayectoria = []
        x, y = self._proyectil.posicion
        while y >= 0:
            x, y = self._proyectil.actualizar_posicion()
            self._trayectoria.append((x, y))
        return self._trayectoria
    
    def simular_analitico(self):
        """
        Simula el movimiento del proyectil usando las ecuaciones analíticas
        """
        self._trayectoria_analitica = []
        tiempo_vuelo = self._proyectil.calcular_tiempo_vuelo()
        steps = int(tiempo_vuelo / self._proyectil.dt) + 1
        
        for i in range(steps):
            t = i * self._proyectil.dt
            x, y = self._proyectil.posicion_analitica(t)
            self._trayectoria_analitica.append((x, y))
        
        return self._trayectoria_analitica
    
    @tiempo_ejecucion
    def graficar(self):
        """
        Grafica la trayectoria del proyectil
        """
        plt.figure(figsize=(10, 6))
        
        if self._usar_analitico:
            # Usar solución analítica
            self.simular_analitico()
            x_vals, y_vals = zip(*self._trayectoria_analitica)
            plt.plot(x_vals, y_vals, 'b-', label='Trayectoria analítica')
        else:
            # Usar solución numérica
            self.simular_numerico()
            x_vals, y_vals = zip(*self._trayectoria)
            plt.plot(x_vals, y_vals, 'r--', label='Trayectoria numérica')
        
        # Añadir una cuadrícula y líneas de referencia
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Marcar altura máxima
        altura_max = self._proyectil.calcular_altura_maxima()
        tiempo_altura_max = self._proyectil.calcular_tiempo_altura_maxima()
        x_altura_max = self._proyectil.vx * tiempo_altura_max
        plt.plot(x_altura_max, altura_max, 'ro', label=f'Altura máxima: {altura_max:.2f} m')
        plt.axhline(y=altura_max, color='r', linestyle=':', alpha=0.5)
        
        # Marcar alcance
        alcance = self._proyectil.calcular_alcance()
        plt.axvline(x=alcance, color='g', linestyle=':', alpha=0.5)
        plt.plot(alcance, 0, 'go', label=f'Alcance: {alcance:.2f} m')
        
        # Añadir información del movimiento en la leyenda
        plt.xlabel('Distancia (m)')
        plt.ylabel('Altura (m)')
        plt.title(f'Simulación de Tiro Parabólico (v₀={self._proyectil.velocidad_inicial:.2f} m/s, θ={self._proyectil.angulo:.2f}°)')
        plt.legend(loc='best')
        
        # Ajustar límites de la gráfica
        plt.xlim(-1, alcance * 1.1)
        plt.ylim(-1, altura_max * 1.2)
        
        plt.tight_layout()
        plt.show()

def calcular_parametros_iniciales(caso, params):
    """
    Calcula velocidad inicial y ángulo según los datos proporcionados
    """
    g = 9.81  # Aceleración debido a la gravedad
    
    if caso == 1:
        # Velocidad inicial y ángulo conocidos
        return params['v0'], params['ang']
        
    elif caso == 2:
        # Altura máxima y tiempo de vuelo conocidos
        h_max = params['h_max']
        t_vuelo = params['t_vuelo']
        
        # Primero calculamos vy inicial
        vy = t_vuelo * g / 2
        
        # Ahora calculamos el ángulo y la velocidad
        ang = math.degrees(math.asin(math.sqrt(2 * g * h_max) / math.sqrt(vy**2 + (t_vuelo*g/2)**2)))
        v0 = vy / math.sin(math.radians(ang))
        
        return v0, ang
        
    elif caso == 3:
        # Altura máxima y alcance conocidos
        h_max = params['h_max']
        alcance = params['alcance']
        
        # Para altura máxima: h_max = (v0*sin(θ))²/(2g)
        # Para alcance: R = (v0²*sin(2θ))/g
        # Despejando:
        ang = math.degrees(math.atan((4 * h_max) / alcance))
        v0 = math.sqrt((alcance * g) / math.sin(2 * math.radians(ang)))
        
        return v0, ang
        
    elif caso == 4:
        # Tiempo de vuelo y alcance conocidos
        t_vuelo = params['t_vuelo']
        alcance = params['alcance']
        
        # Para tiempo de vuelo: T = (2*v0*sin(θ))/g
        # Para alcance: R = (v0*cos(θ))*T
        # Despejando:
        
        # Calculamos primero vx
        vx = alcance / t_vuelo
        
        # Calculamos vy desde t_vuelo
        vy = (t_vuelo * g) / 2
        
        # Calculamos velocidad inicial y ángulo
        v0 = math.sqrt(vx**2 + vy**2)
        ang = math.degrees(math.atan(vy / vx))
        
        return v0, ang

if __name__ == "__main__":
    print("Simulación de Tiro Parabólico")
    print("=============================")
    print("Seleccione el caso correspondiente:")
    print("1. Conozco velocidad inicial y ángulo.")
    print("2. Conozco altura máxima y tiempo de vuelo.")
    print("3. Conozco altura máxima y alcance.")
    print("4. Conozco tiempo de vuelo y alcance.")
    
    try:
        caso = int(input("Ingrese el número de caso (1-4): "))
        
        if caso < 1 or caso > 4:
            raise ValueError("El caso debe estar entre 1 y 4")
            
        params = {}
        if caso == 1:
            params['v0'] = float(input("Velocidad inicial (m/s): "))
            params['ang'] = float(input("Ángulo de lanzamiento (grados): "))
        elif caso == 2:
            params['h_max'] = float(input("Altura máxima (m): "))
            params['t_vuelo'] = float(input("Tiempo de vuelo (s): "))
        elif caso == 3:
            params['h_max'] = float(input("Altura máxima (m): "))
            params['alcance'] = float(input("Alcance total (m): "))
        elif caso == 4:
            params['t_vuelo'] = float(input("Tiempo de vuelo (s): "))
            params['alcance'] = float(input("Alcance total (m): "))
        
        v0, ang = calcular_parametros_iniciales(caso, params)
        
        print("\nResultados calculados:")
        print(f"Velocidad inicial: {v0:.2f} m/s")
        print(f"Ángulo de lanzamiento: {ang:.2f}°")
        
        proyectil = Proyectil(v0, ang)
        print(f"Tiempo total de vuelo: {proyectil.calcular_tiempo_vuelo():.2f} s")
        print(f"Altura máxima alcanzada: {proyectil.calcular_altura_maxima():.2f} m")
        print(f"Distancia total recorrida: {proyectil.calcular_alcance():.2f} m")
        
        metodo = input("\n¿Usar método analítico o numérico? (a/n): ").lower()
        usar_analitico = metodo != 'n'
        
        simulacion = Simulacion(proyectil, usar_analitico)
        simulacion.graficar()
    
    except ValueError as e:
        print(f"Error: {e}")
        print("Por favor, introduzca valores numéricos válidos.")
    except Exception as e:
        print(f"Error inesperado: {e}")