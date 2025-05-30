#ifndef CONTROL_VENTILADOR_H
#define CONTROL_VENTILADOR_H

#include <Arduino.h>

class ControlVentilador {
private:
  int pinPWM;
  int velocidadActual;        // Velocidad actual (0-255)
  int velocidadObjetivo;      // Velocidad objetivo (0-255)
  int incrementoVelocidad;    // Incremento por step
  unsigned long tiempoAnterior;
  unsigned long intervaloTransicion; // Tiempo entre cambios graduales
  bool transicionActiva;
  bool ventiladorEncendido;
  
  // Variables para control de arranque suave
  bool arranqueSuave;
  int velocidadMinima;        // Velocidad mínima para arranque
  
public:
  // Constructor
  ControlVentilador(int pin, int velocidadMin = 100);
  
  // Métodos principales
  void inicializar();
  void establecerVelocidad(int porcentaje);
  void encender(int porcentaje = 50);
  void apagar();
  void actualizar();
  
  // Configuración
  void configurarTransicion(int incremento, unsigned long intervalo);
  void configurarArranqueSuave(bool habilitado, int velocidadMin = 100);
  
  // Getters para monitoreo
  int obtenerVelocidadActual();
  int obtenerVelocidadObjetivo();
  bool estaEncendido();
  bool estaEnTransicion();
  
  // Parada de emergencia
  void paradaEmergencia();
  
  // Obtener estado completo del ventilador
  String obtenerEstadoCompleto();
};

#endif
