# Librería Control PWM Ventilador
## Referencia de métodos

### ------| Métodos principales |------

#### `inicializar()`
Configura el pin como salida PWM e inicializa el ventilador apagado.

```cpp
ventilador.inicializar();
```

#### `encender(int porcentaje = 50)`
Enciende el ventilador con la velocidad especificada (0-100%).

```cpp
ventilador.encender(75);    // 75% de velocidad
ventilador.encender();      // 50% por defecto
```

#### `apagar()`
Apaga el ventilador gradualmente hasta velocidad 0.

```cpp
ventilador.apagar();
```

#### `establecerVelocidad(int porcentaje)`
Cambia la velocidad objetivo del ventilador (0-100%).

```cpp
ventilador.establecerVelocidad(30);  // Cambiar a 30%
```

#### `actualizar()`  **CRÍTICO** ⚠
Procesa las transiciones de velocidad. **TIENE** que llamarse en cada ciclo del `loop()`.

```cpp
void loop() {
    ventilador.actualizar();  // Obligatorio!
}
```

#### `paradaEmergencia()`
Detiene inmediatamente el ventilador sin transición gradual.

```cpp
ventilador.paradaEmergencia();
```



--------------------------------------------------------------------------



### ------| Métodos de configuración |------

#### `configurarTransicion(int incremento, unsigned long intervalo)`
Ajusta la velocidad de las transiciones.

```cpp
// Transición más rápida: incremento 10, cada 20ms
ventilador.configurarTransicion(10, 20);

// Transición más suave: incremento 2, cada 100ms  
ventilador.configurarTransicion(2, 100);
```

**Parámetros:**
- `incremento`: Cambio de PWM por step (1-50)
- `intervalo`: Tiempo entre cambios en milisegundos (10-1000ms)


#### `configurarArranqueSuave(bool habilitado, int velocidadMin = 100)`
Configura el arranque suave para proteger el motor.
```cpp
ventilador.configurarArranqueSuave(true, 120);   // Habilitado, PWM mín: 120
ventilador.configurarArranqueSuave(false);       // Deshabilitado
```



--------------------------------------------------------------------------



### ------| Métodos de monitoreo |------

#### `obtenerVelocidadActual()`
Retorna la velocidad actual en porcentaje (0-100%).

```cpp
int velocidad = ventilador.obtenerVelocidadActual();
Serial.println("Velocidad actual: " + String(velocidad) + "%");
```

#### `obtenerVelocidadObjetivo()`
Retorna la velocidad objetivo en porcentaje (0-100%).

```cpp
int objetivo = ventilador.obtenerVelocidadObjetivo();
```

#### `estaEncendido()`
Retorna `true` si el ventilador está encendido.

```cpp
if (ventilador.estaEncendido()) {
    Serial.println("Ventilador funcionando");
}
```

#### `estaEnTransicion()`
Retorna `true` si el ventilador está cambiando de velocidad.

```cpp
if (ventilador.estaEnTransicion()) {
    Serial.println("Cambiando velocidad...");
}
```

#### `obtenerEstadoCompleto()`
Retorna un String con toda la información del ventilador.

```cpp
String estado = ventilador.obtenerEstadoCompleto();
Serial.println(estado);
// Output: "Pin:9,Velocidad:75%,Objetivo:75%,Encendido:SI,Transicion:NO,PWM:191"
```
