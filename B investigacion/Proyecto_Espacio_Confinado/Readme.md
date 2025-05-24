![Logo de la Institución ISPC](/E%20assets/caratula.png)  

# Módulo Programador FullStack IoT
## Tecnicatura Superior en Telecomunicaciones – Segundo Año

---------------------------

### Profesores
- Morales Jorge (Arquitectura y conectividad) | [https://github.com/JorEl057](https://github.com/JorEl057)
- Gonzalez Mario (Sistemas de control y servicios) | 
- Mainero Alejandro (Plataformas) | 

### Miembros:
- Luciano Lujan | GitHub: https://github.com/lucianoilujan
- Durigutti, Vittorio | GitHub: https://github.com/vittoriodurigutti
- Joaquin Zalazar | GitHub: https://github.com/breaakerr
- Lisandro Juncos | GitHub: https://github.com/Lisandro-05
- Nahuel Velez | GitHub: https://github.com/ISPC-TST-PI-I-2024/ISPC_PI_Lucas_Nahuel_Velez 
- Jose Marquez | GitHub: https://github.com/ISPC-TST-PI-I-2024/josemarquez.git
- Maria Lilen Guzmán | GitHub: https://github.com/lilenguzman01


### Índice

---------------------------

### 🔹 Presentación General  

El módulo Programador FullStack IoT es un espacio interdisciplinario que integra las materias Arquitectura y Conectividad, Sistemas de Control y Servicios y Plataformas, orientado al diseño e implementación de soluciones IoT aplicadas a la industria.
Durante 10 semanas, los estudiantes trabajarán en equipos de 3 a 8 integrantes, desarrollando un proyecto técnico completo que abarque sensado, conectividad, automatización, visualización de datos y documentación profesional.
El trabajo se organiza bajo el enfoque de Aprendizaje Basado en Proyectos (ABP), con metodología Scrum: tres sprints, entregas semanales y seguimiento por parte de los docentes de cada materia. El desarrollo debe gestionarse en GitHub y documentarse en cada etapa.

--- 
## Proyecto "ESPACIOS CONFINADOS"


### De acuerdo con la siguiente situacion se plantea una solucion IOT para resolver la problematica que se describe a continuación:

*Disponemos de una localización con maquinaria con alta posibilidad de emanación de gases contaminantes inflamables. Los mismos no son problemáticos exceptuando concentración alta durante periodos prolongados.*

*Se propone tener distribuidos una serie de de **sensores de gas  combustibles (MQ-4)** a lo largo del deposito mencionado, ubicados estratégicamente.  El mismo dispone de energía eléctrica provista por generadores, pero no de internet.*
 
*Mediante la aplicación de dispositivos sensores con comunicación mediante módulos LoRa, y utilizando el protocolo de comunicación LORAWAN buscamos estar informados en el estado a tiempo real dentro de el sitio.*

*Esto nos permite llevar un seguimiento y análisis preventivo, e identificar fallas que deban requerir intervención humana.  La distancia para acceder al sitio y las condiciones del aire suponen un problema para asistir fallas, por lo que disponemos de dispositivos extractores con potencia variable distribuidos dentro.*

*Nuestro sistema receptor se encarga de la manipulación de los umbrales mediante los cuales se dispara la accion y potencia de dichos equipos.  Disponemos como extra de accionadores *"manuales"* remotos via apps con los que disparar los extractores ante criterio humano.*

**Para el desarrollo del diseño de una solucion para el desafío planteado, nos propusimos llevar adelante el proyecto de acuerdo a las siguientes herramientas de desarrollo de dispositivos IOT:**

### **1. Hardware**

-   **Microcontroladores:**
    -   **ESP32:** Dos módulos ESP32 se utilizan como dispositivos IoT. Uno para leer el sensor de gas y otro para controlar el extractor de aire.
    -   **Sensor MQ-4:** Sensor de gas para detectar niveles de gases nocivos (como metano).
    -   **Módulo LoRa:** Para comunicación inalámbrica entre los dos ESP32.
    -   **Extractor de aire:** Controlado mediante PWM desde el segundo ESP32 (simulado con un cooler).

----------

### **2. Software para los ESP32 (Firmware)**

#### **Lenguaje:**

-   **C++:** Los ESP32 se programan utilizando Arduino C++.

#### **Framework:**

-   **Arduino Framework:** Simplifica la programación de microcontroladores con una API amigable.

#### **Bibliotecas:**

-   **SPI.h y LoRa.h:** Para manejar la comunicación LoRa.
-   **WiFi.h y PubSubClient.h:** Para conectarse a redes WiFi y publicar datos en un broker MQTT.
-   **ArduinoJson:** Para trabajar con mensajes JSON en el ESP32 que recibe datos por LoRa.

#### **Herramienta de desarrollo:**

-   **PlatformIO:** Entorno de desarrollo integrado (IDE) basado en VS Code para gestionar dependencias, compilar y cargar el firmware en los ESP32.

----------

### **3. Backend (API para procesar datos MQTT)**

#### **Lenguaje:**

-   **JavaScript/Node.js:** Para crear el backend que procesa los datos MQTT y los almacena en la base de datos.

#### **Framework:**

-   **Express.js:** Framework minimalista para construir APIs RESTful y servidores HTTP en Node.js.

#### **Bibliotecas:**

-   **mqtt:** Cliente MQTT para suscribirse a los mensajes del broker.
-   **mysql2:** Biblioteca para interactuar con MariaDB.
-   **body-parser:** Middleware para analizar el cuerpo de las solicitudes HTTP.

#### **Base de datos:**

-   **MariaDB:** Sistema de gestión de bases de datos relacional para almacenar los datos de los sensores.

#### **Herramientas adicionales:**

-   **npm:** Gestor de paquetes para instalar dependencias en Node.js.
-   **Logging personalizado:** Archivo `logger.js` para registrar eventos importantes.

----------

### **4. Broker MQTT**

-   **Broker privado:** Se utiliza un broker MQTT privado **telecomunicaciones.ddns.net:2480** para transmitir los datos desde el ESP32 al backend.
-   Se defininan el/los topicos para la comunicacion de los dispositivos hacia el broker MQTT.

----------

### **5. Frontend (Dashboard para visualización en tiempo real)**

#### **Herramientas:**

**GRAFANA:** Tablero de visualización en tiempo real.

----------

### **6. Base de datos**

-   **MariaDB:** Base de datos relacional para almacenar los datos de los sensores.
-   **SQL:** Lenguaje de consulta utilizado para crear tablas, insertar datos y realizar consultas.

----------

### **7. Herramientas de desarrollo**

#### **Editor de código:**

-   **Visual Studio Code (VS Code):** Editor de código principal para desarrollar tanto el firmware de los ESP32 como el backend y frontend.

#### **Extensiones de VS Code:**

-   **PlatformIO IDE:** Para desarrollar, compilar y cargar el firmware de los ESP32.

#### **Herramientas adicionales:**

-   **MQTT Explorer:** Cliente MQTT para depurar y monitorear los mensajes publicados en el broker.
-   **HeidiSQL o MySQL Workbench:** Para administrar y visualizar la base de datos MariaDB.

----------

### **8. Comunicaciones**

#### **Protocolos:**

-   **LoRa:** Para comunicación inalámbrica de larga distancia entre los dos ESP32.
-   **MQTT:** Protocolo de mensajería ligero para enviar datos desde el ESP32 al backend.
-   **HTTP:** Para futuras APIs RESTful que puedan exponer datos desde el backend.

#### **Formato de datos:**

-   **JSON:** Todos los datos se envían y almacenan en formato JSON para facilitar su procesamiento.

----------

### **Resumen del stack tecnológico**

**Componente**

Tecnología/Lenguaje/Herramienta

**Hardware**

ESP32, Sensor MQ-4, Módulo LoRa, Extractor

**Firmware**

C++, Arduino Framework, PlatformIO, VS Code

**Backend**

Node.js, Express.js, MariaDB, MQTT

**Frontend**

Grafana

**Comunicaciones**

LoRa, MQTT, JSON

**Base de datos**

MariaDB, SQL

**Desarrollo**

VS Code, PlatformIO, npm, MQTT Explorer
