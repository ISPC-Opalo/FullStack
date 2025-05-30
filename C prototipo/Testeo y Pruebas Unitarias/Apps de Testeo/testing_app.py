import random
import time
import json
import paho.mqtt.client as mqtt

# ——— CONFIGURACIÓN —————————————————————————————————————————————
BROKER   = 'test.mosquito.org'     
PORT     = 1883                     
TOPIC    = 'gas/datos'

GATEWAYS = [
    'esp32-central-001',
    'esp32-central-002',
    'esp32-central-003'
]

# RANGOS DE VALORES
MIN_PPM, MAX_PPM       = 0.0,   1000.0
MIN_RATIO, MAX_RATIO   = 0.1,   10.0
MIN_RAW, MAX_RAW       = 0,     1023
UMBRAL                 = 500.0
MIN_VEL, MAX_VEL       = 0,     100
PWM_MAX                = 127

# ————————————————————————————————————————————————————————————————

def generate_payload() -> str:
    """Construye y devuelve el JSON listo para publicar."""
    gateway     = random.choice(GATEWAYS)
    # Si quisieras simular millis() desde arranque:
    timestamp   = int(time.monotonic() * 1000)
    ppm         = round(random.uniform(MIN_PPM, MAX_PPM), 1)
    ratio       = round(random.uniform(MIN_RATIO, MAX_RATIO), 2)
    raw         = random.randint(MIN_RAW, MAX_RAW)
    estado      = "ALERTA" if ppm > UMBRAL else "NORMAL"
    automatico  = random.choice([True, False])
    encendido   = random.choice([True, False])
    transicion  = False
    velocidad   = random.randint(MIN_VEL, MAX_VEL)
    pwm_value   = int(velocidad / 100 * PWM_MAX)
    estadoVent  = (
        f"Pin:27,Velocidad:{velocidad}%"
        f",Objetivo:{velocidad}%"
        f",Encendido:{'SI' if encendido else 'NO'}"
        f",Transicion:{'SI' if transicion else 'NO'}"
        f",PWM:{pwm_value}"
    )

    payload = {
      "gatewayId": gateway,
      "timestamp": timestamp,
      "sensor": {
        "ppm": ppm,
        "ratio": ratio,
        "raw": raw,
        "estado": estado,
        "umbral": UMBRAL
      },
      "control": {
        "automatico": automatico,
        "encendido": encendido,
        "transicion": transicion,
        "velocidad": velocidad
      },
      "estadoVentilador": estadoVent
    }
    return json.dumps(payload)

def main():
    client = mqtt.Client()
    client.connect(BROKER, PORT, keepalive=60)
    payload = generate_payload()
    client.publish(TOPIC, payload)
    print(f"\nPublicado en mqtt://{BROKER}:{PORT}/{TOPIC}:\n")
    print(payload, "\n")
    client.disconnect()

if __name__ == "__main__":
    main()


# ————————————————————————————————————————————————————————————————
# Ejemplo de payload generado:

# {
#   "gatewayId": "esp32-central-001",
#   "timestamp": 12345678,        // millis() desde arranque
#   "sensor": {
#     "ppm": 18.0,
#     "ratio": 1.23,
#     "raw": 512,
#     "estado": "NORMAL",
#     "umbral": 500.0
#   },
#   "control": {
#     "automatico": true,
#     "encendido": true,
#     "transicion": false,
#     "velocidad": 50         // % actual mapeado
#   },
#   "estadoVentilador": "Pin:27,Velocidad:50%,Objetivo:50%,Encendido:SI,Transicion:NO,PWM:127"
# }