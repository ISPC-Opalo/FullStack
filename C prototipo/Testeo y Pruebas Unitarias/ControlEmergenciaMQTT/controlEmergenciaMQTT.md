```cpp
/*
 * ---------------------------------------------------------------------------
 * Método: controlEmergenciaMQTT
 * 
 * Dependencias obligatorias:
 *   #include <PubSubClient.h>  // Librería MQTT (instalar via Arduino Library Manager)
 *   #include <WiFi.h>          // Librería WiFi para ESP32
 *   #include "ControlVentilador.h" //clase personalizada del ventilador
 * 
 * Variables globales requeridas en el programa principal:
 *   WiFiClient espClient;            // Cliente WiFi
 *   PubSubClient client(espClient);  // Cliente MQTT
 *   ControlVentilador ventilador;    // Instancia de tu clase de control
 * 
 * Configuración previa requerida:
 *   1. Tener conexión WiFi establecida (conectar a red en setup())
 *   2. Broker MQTT configurado (ej: client.setServer(broker, puerto))
 *   3. Ventilador inicializado (ej: ventilador.inicializar())
 * ---------------------------------------------------------------------------
 */

// Función de callback para manejar comandos MQTT
void controlEmergenciaMQTT(char* topic, byte* payload, unsigned int length) {

  /* ----------------------------------------------
   * 1. FILTRADO POR TÓPICO MQTT
   * ----------------------------------------------
   * Solo procesa mensajes del tópico especificado
   */
  String strTopic = String(topic);
  if (strTopic != "wokwi/ventilador_control") {//NOTA: usar el topico que pongamos en el código final para controlar los ventiladores
    return;  // Ignorar otros tópicos
  }

  /* ----------------------------------------------
   * 2. PROCESAMIENTO DEL PAYLOAD
   * ----------------------------------------------
   * Construye un String seguro con el mensaje:
   * - Filtra caracteres no imprimibles (seguridad básica)
   * - Elimina espacios innecesarios
   */
  String mensaje = "";
  for (int i = 0; i < length; i++) {
    if (isPrintable(payload[i])) {  // ASCII 32-126
      mensaje += (char)payload[i];
    }
  }
  mensaje.trim(); //Limpieza del mensaje: elimina espacios/tabuladores al inicio y final

  /* ----------------------------------------------
   * 3. LÓGICA DE CONTROL DEL VENTILADOR
   * ----------------------------------------------
   * Acciones compatibles con la clase ControlVentilador:
   * - encender(velocidad)
   * - paradaEmergencia()
   * - estaEncendido()
   */
  if (mensaje == "OFF") {
    if (ventilador.estaEncendido()) {
      ventilador.paradaEmergencia();
      
    }
    
  } else if (mensaje == "ON") {
    if (!ventilador.estaEncendido()) {
      ventilador.encender(100);  // Encender al 100% de velocidad
      
    }
    
  } 
}

/* ---------------------------------------------------------------------------
 * Notas de uso en el programa principal:
 * 
 * 1. En el setup():
 *    - Inicializar WiFi y MQTT:
 *      
 *      void setup() {
 *        Serial.begin(115200);
 *        setup_wifi();  // Tu función de conexión WiFi
 *        client.setServer(MQTT_BROKER, MQTT_PORT);  // Configurar broker
 *        client.setCallback(controlEmergenciaMQTT);  // ¡Asignar este callback!
 *        ventilador.inicializar();  // Inicializar hardware del ventilador
 *      }
 * 
 * 2. En el loop():
 *    - Mantener conexión MQTT activa:
 *      
 *      void loop() {
 *        if (!client.connected()) reconnect();
 *        client.loop();
 *        // ... otras tareas
 *      }
 * 
 * 3. Requiere implementar:
 *    - void setup_wifi() -> Conexión a tu red WiFi
 *    - void reconnect()  -> Reconexión MQTT
 * ---------------------------------------------------------------------------
 */
