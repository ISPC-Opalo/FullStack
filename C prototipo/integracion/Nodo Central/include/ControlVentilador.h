#ifndef CONTROL_VENTILADOR_H
#define CONTROL_VENTILADOR_H

#include <Arduino.h>

class ControlVentilador {
  private:
    // Pines y control PWM
    int pinPWM;
    int velocidadActual;      // Valor PWM actual (0-255)
    int velocidadObjetivo;    // Valor PWM objetivo (0-255)
    int velocidadMinima;      // PWM mínimo para arranque
    int pwmMaximo;           // PWM máximo permitido (0-255)
    
    // Control de transición suave
    int incrementoVelocidad;
    unsigned long intervaloTransicion;
    unsigned long tiempoAnterior;
    bool transicionActiva;
    
    // Estado del ventilador
    bool ventiladorEncendido;
    bool arranqueSuave;
    
  public:
    // Constructor
    ControlVentilador(int pin, int velocidadMin = 100);
    
    // Funciones principales
    void inicializar();
    void establecerVelocidad(int porcentaje);
    void encender(int porcentaje = 50);
    void apagar();
    void actualizar();
    
    // Configuración
    void configurarTransicion(int incremento, unsigned long intervalo);
    void configurarArranqueSuave(bool habilitado, int velocidadMin = 100);
    void setPwmMax(int pwmMax);              // Nueva función
    void setObjetivo(int porcentaje);        // Nueva función
    
    // Getters
    int pinPWM_;
    int obtenerVelocidadActual();
    int obtenerVelocidadObjetivo();
    int obtenerPwmMax();                     // Nueva función
    bool estaEncendido();
    bool estaEnTransicion();
    String obtenerEstadoCompleto();
    
    // Emergencia
    void paradaEmergencia();
};

#endif