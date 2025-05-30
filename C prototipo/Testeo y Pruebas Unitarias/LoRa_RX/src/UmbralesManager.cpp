#include "UmbralesManager.h"

void UmbralesManager::begin() {
    prefs.begin(NAMESPACE, false);
}

void UmbralesManager::load() {
    umbrales.minvelocidad  = prefs.getInt(KEY_MIN,  30);  // valor por defecto
    umbrales.maxvelocidad  = prefs.getInt(KEY_MAX,  90);
    umbrales.histeresis= prefs.getInt(KEY_HIST,  5);
}

void UmbralesManager::save() const {
    prefs.putInt(KEY_MIN,  umbrales.minvelocidad);
    prefs.putInt(KEY_MAX,  umbrales.maxvelocidad);
    prefs.putInt(KEY_HIST, umbrales.histeresis);
}

void UmbralesManager::updateFromJson(const JsonDocument& doc) {
    if (doc.containsKey("minvelocidad"))   umbrales.minvelocidad   = doc["minvelocidad"];
    if (doc.containsKey("maxvelocidad"))   umbrales.maxvelocidad   = doc["maxvelocidad"];
    if (doc.containsKey("histeresis"))     umbrales.histeresis     = doc["histeresis"];
    save();  // persisto cambios automáticamente
}

Umbrales UmbralesManager::get() const {
    return umbrales;
}
