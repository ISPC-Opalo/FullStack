## Manual de uso.

### Descripcion:
Este pequeño programa funciona como un ejemplo de uso de la libreria <Preferecne.h> en combinacion con funciones asincronicas de MQTT y Wifi demorastrando de manera sensilla el registro de una variable en memoria NVS, resistiendo a reincion del dispositivo fisico, y la actualizacion en tiempo real de la misma via suscripcion a topic "config/* /*".
En este ejemplo demostramos un envio de mensaje tipo string registrando el timestamp en un intervalo regular. Y como responde el mismo ante reincios, desoncexiones, recepcion de mensajes que altera/actualizan el valor guardado en el espacio NVS todo realizado de manera asincronica, de forma que el proceso nunca se ve interrumpido. Asi mismo con control de errores simples, ante por ejeplo, ingreso de un mensaje de configuracion en un formato no esperado.


----

### Estrcutura del directorio:

- ┣ 📂.vscode
- ┃ ┣ 📜c_cpp_properties.json
- ┃ ┣ 📜extensions.json
- ┃ ┗ 📜launch.json
- ┣ 📂include
- ┃ ┣ 📜ConfigStorage.h             // Esta porcion se encargade la clase ConfigStorage. Esto es lectura y escritura de las caracteristicas definidas
- ┃ ┣ 📜MqttManager.h               // Gestion de clase MqttManager para gestion de envio y recepcion de MQTT asincronico
- ┃ ┣ 📜README
- ┃ ┗ 📜WifiManager.h               // Gestion de clase WifiManager para gestion de envio y recepcion de wifi asincronico
- ┣ 📂lib
- ┃ ┗ 📜README
- ┣ 📂src
- ┃ ┗ 📜main.cpp
- ┣ 📂test
- ┃ ┗ 📜README
- ┣ 📜.gitignore
- ┣ 📜manual.md
- ┗ 📜platformio.ini

### Librerias Utilizadas:
- Externas:
    - arvinroger/AsyncMqttClient @ ^0.9.0
    - blanchon/ArduinoJson @ ^7.4.1

- Incluidas por defecto:
    - Preference.h
    - wifi.h
    - funtional.h

### Clases:

- **WifiManager**: Funciona via manejo de eventos, propios de la libreria de wifi. Comenzando con _connect = false de forma que parte como desconectado, y dispara la siguiente cadena de funciones:
    - begin: requiere SSID + Password. Dispara "WiFi.onEven" con lo verifica estado de _connect y pasa a true, luego informa IP via wifi.localIP
    
- **ConfigStorage**: requiere dos definiciones: "nv" que corresponde a nombre de la particion del NVS. Por defecto, sino se define, es "config" y variable "isOpen" (false corresponde a pude leer y escribir en la particion, true es solo lectura). 
    - begin: inicia el acceso a la memoria, y el formado lectura/escritura
    - getX: (formato del valor): funciones por defecto para obtener los diferentes posibles valores, booleanos, integrales, flotantes, o strings
    - putX: igual que get, definiendo el tipo de valor que ingresaremos en la particion
    - end: Siempre debe cerrarse luego de utilizarce

- **MqttManager**: En esta clase declaramos las interfases y miembros privados, obtenidos de las dos direcciones anteriores. **_cfg** para persistir parámetros, **_wifi** para reaccionar a eventos de Wi-Fi, como las desconexiones y reconexiones. Y **_lastPublish** simplemente el timestamp de la ultima lectura. En este caso lo usamos unicamente para discriminar si las lecturas se realizan segun lo que definimos como intervalos
    - begin(host, port): _mqtt.onConnect verifica estado y conecta segun el broker asingado,  _mqtt.subscribe suscribe al topic de donde recibia las modificaciones de intervalo (config/prueba/vitto2 en QoS 0.)
    - _mqtt.onMessage: reaccion ante la reccepcion de un mensaje via el topic indicado anteriormente. Esta diseñado para recibir un json {"interval":int}. Si el mensaje no llega con este formato, responde con un mensaje de error.

----

### Demostracion de Uso:

Arreque, conexion a la red wifi, el broker, y al topic predefinido
![Flujo de datos](asset\inicio.png)

Lecturas regulares (tipo|mensaje|timestamp|intervalo guardado)
![Flujo de datos](asset\lecturaOK.png)

Error en mensaje de configuracion. Indica el json no se puede parsear/leer por error en formato
![Flujo de datos](asset\erro.png)

Actualizacion de valor guardado en NVS via funciones de la clase ConfigStorage (preference), con mensaje pre y pos actualizacion
![Flujo de datos](asset\actualizacion.png)