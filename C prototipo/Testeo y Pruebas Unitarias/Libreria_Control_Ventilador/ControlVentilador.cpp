#include "ControlVentilador.h"

// Constructor
ControlVentilador::ControlVentilador(int pin, int velocidadMin) {
  pinPWM = pin;
  velocidadActual = 0;
  velocidadObjetivo = 0;
  velocidadMinima = velocidadMin;
  incrementoVelocidad = 5;
  intervaloTransicion = 50; // 50ms entre cambios
  tiempoAnterior = 0;
  transicionActiva = false;
  ventiladorEncendido = false;
  arranqueSuave = true;
}

// Inicializar el ventilador
void ControlVentilador::inicializar() {
  pinMode(pinPWM, OUTPUT);
  analogWrite(pinPWM, 0);
  Serial.println("Ventilador inicializado en pin " + String(pinPWM));
}

// Establecer velocidad objetivo (0-100%)
void ControlVentilador::establecerVelocidad(int porcentaje) {
  // Validar rango
  porcentaje = constrain(porcentaje, 0, 100);
  
  // Convertir porcentaje a valor PWM (0-255)
  if (porcentaje == 0) {
    velocidadObjetivo = 0;
    ventiladorEncendido = false;
  } else {
    // Aplicar velocidad mínima si está habilitada
    int valorPWM = map(porcentaje, 0, 100, 0, 255);
    if (arranqueSuave && valorPWM > 0 && valorPWM < velocidadMinima) {
      valorPWM = velocidadMinima;
    }
    velocidadObjetivo = valorPWM;
    ventiladorEncendido = true;
  }
  
  transicionActiva = true;
  Serial.println("Nueva velocidad objetivo: " + String(porcentaje) + "% (PWM: " + String(velocidadObjetivo) + ")");
}

// Encender ventilador con velocidad específica
void ControlVentilador::encender(int porcentaje) {
  establecerVelocidad(porcentaje);
}

// Apagar ventilador gradualmente
void ControlVentilador::apagar() {
  establecerVelocidad(0);
}

// Función principal - debe llamarse en el loop()
void ControlVentilador::actualizar() {
  unsigned long tiempoActual = millis();
  
  // Solo actualizar si hay transición activa y ha pasado el tiempo suficiente
  if (transicionActiva && (tiempoActual - tiempoAnterior >= intervaloTransicion)) {
    
    if (velocidadActual != velocidadObjetivo) {
      // Calcular siguiente paso
      if (velocidadActual < velocidadObjetivo) {
        velocidadActual = min(velocidadActual + incrementoVelocidad, velocidadObjetivo);
      } else {
        velocidadActual = max(velocidadActual - incrementoVelocidad, velocidadObjetivo);
      }
      
      // Aplicar nueva velocidad
      analogWrite(pinPWM, velocidadActual);
      
      // Debug info
      Serial.println("Velocidad actual: " + String(map(velocidadActual, 0, 255, 0, 100)) + "% (PWM: " + String(velocidadActual) + ")");
      
    } else {
      // Transición completada
      transicionActiva = false;
      Serial.println("Transición completada - Velocidad final: " + String(map(velocidadActual, 0, 255, 0, 100)) + "%");
    }
    
    tiempoAnterior = tiempoActual;
  }
}

// Configurar parámetros de transición
void ControlVentilador::configurarTransicion(int incremento, unsigned long intervalo) {
  incrementoVelocidad = constrain(incremento, 1, 50);
  intervaloTransicion = constrain(intervalo, 10, 1000);
}

// Habilitar/deshabilitar arranque suave
void ControlVentilador::configurarArranqueSuave(bool habilitado, int velocidadMin) {
  arranqueSuave = habilitado;
  velocidadMinima = constrain(velocidadMin, 50, 200);
}

// Getters para monitoreo
int ControlVentilador::obtenerVelocidadActual() {
  return map(velocidadActual, 0, 255, 0, 100);
}

int ControlVentilador::obtenerVelocidadObjetivo() {
  return map(velocidadObjetivo, 0, 255, 0, 100);
}

bool ControlVentilador::estaEncendido() {
  return ventiladorEncendido;
}

bool ControlVentilador::estaEnTransicion() {
  return transicionActiva;
}

// Parada de emergencia
void ControlVentilador::paradaEmergencia() {
  velocidadActual = 0;
  velocidadObjetivo = 0;
  transicionActiva = false;
  ventiladorEncendido = false;
  analogWrite(pinPWM, 0);
  Serial.println("PARADA DE EMERGENCIA - Ventilador detenido");
}

// Obtener estado completo del ventilador (para reportes)
String ControlVentilador::obtenerEstadoCompleto() {
  String estado = "Pin:" + String(pinPWM) + 
                  ",Velocidad:" + String(obtenerVelocidadActual()) + "%" +
                  ",Objetivo:" + String(obtenerVelocidadObjetivo()) + "%" +
                  ",Encendido:" + (estaEncendido() ? "SI" : "NO") +
                  ",Transicion:" + (estaEnTransicion() ? "SI" : "NO") +
                  ",PWM:" + String(velocidadActual);
  return estado;
}