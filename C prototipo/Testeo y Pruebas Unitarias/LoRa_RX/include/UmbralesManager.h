#ifndef THRESHOLD_MANAGER_H
#define THRESHOLD_MANAGER_H

#include <Preferences.h>
#include <ArduinoJson.h>

/// Estructura de umbrales para el ventilador
struct Umbrales {
    int minvelocidad;
    int maxvelocidad;
    int histeresis;
};

class UmbralesManager {
public:
    /// Inicializa el almacenamiento en EEPROM (Preferences)
    void begin();

    /// Carga los umbrales desde EEPROM  
    void load();

    /// Guarda los umbrales actuales en EEPROM  
    void save() const;

    /// Actualiza umbrales desde un JSON recibido por MQTT  
    void updateFromJson(const JsonDocument& doc);

    /// Getter de toda la estructura  
    Umbrales get() const;

private:
    Preferences prefs;      // handle de Preferences
    Umbrales   umbrales{};  // valores en RAM
    static constexpr const char* NAMESPACE = "ventilador";
    static constexpr const char* KEY_MIN     = "minVelocidad";
    static constexpr const char* KEY_MAX     = "maxVelocidad";
    static constexpr const char* KEY_HIST    = "histeresis";
};

#endif // THRESHOLD_MANAGER_H
