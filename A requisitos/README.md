![Logo de la Institución ISPC](/E%20assets/caratula.png)

# INSTITUTO SUPERIOR POLITECNICO CORDOBA
## TECNICATURA SUPERIOR EN TELECOMUINICACIONES - COHORTE 2024.

## **Aqui se describen los requisitos generales para el proyecto a desarrollar y el stack técnologico propuesto.**


# A - Requisitos

La fase de requisitos se define como el punto de partida fundamental para el desarrollo del sistema, enmarcando tanto las necesidades operativas de la instalación como las condiciones del entorno. Este proyecto se desarrolla siguiendo el enfoque ABP, en el que el aprendizaje se potencia a través del trabajo colaborativo, la iteración y la aplicación práctica de tecnologías innovadoras.

## Requisitos Funcionales

- **Monitoreo en Tiempo Real:**  
  - Capturar y transmitir continuamente los datos de sensores de gas combustible distribuidos estratégicamente en las ubicaciones requeridas.
  - Registrar los niveles de gas para un análisis histórico y preventivo.

- **Accionamiento Automatizado y Remoto:**  
  - Configurar umbrales de seguridad que, al ser excedidos, activen automáticamente extractores de potencia variable.
  - Permitir la intervención manual mediante accionadores remotos vía aplicaciones móviles para activar extractores según criterio humano.

- **Comunicación y Transmisión de Datos:**  
  - Utilizar el protocolo MQTT mediante el broker Mosquitto (test.mosquitto.org) para enviar y recibir datos.
  - Implementar comunicación punto a punto utilizando LoRa (sin protocolo LoRaWAN) y nodos WiFi que funcionen como gateway.

- **Visualización e Interfaz de Supervisión:**  
  - Desarrollar dashboards interactivos y de fácil interpretación con Grafana y Node-Red para la visualización en tiempo real del estado del sistema.
  - Facilitar la consulta de información y el seguimiento de incidencias.

## Requisitos No Funcionales

- **Baja Latencia y Alta Responsividad:**  
  - Garantizar que la transmisión y el procesamiento de datos ocurran en tiempo real, minimizando demoras.

- **Seguridad y Privacidad:**  
  - Proteger la integridad y confidencialidad de la información transmitida y almacenada.
  
- **Escalabilidad y Fiabilidad:**  
  - Permitir la incorporación de nuevos dispositivos y sensores sin degradar el rendimiento del sistema.
  - Asegurar la operación continua y resiliente ante condiciones adversas de conectividad.

## Requisitos Tecnológicos y Herramientas

- **Entorno de Desarrollo:**  
  - IDE: Visual Studio Code.  
  - Simulador: Wokwi para pruebas de integración y validación de dispositivos.

- **Gestión y Control de Versiones:**  
  - Uso de Git y GitHub para documentar, gestionar y registrar el avance del proyecto.

- **Base de Datos y Visualización:**  
  - Base de Datos: MariaDB para el almacenamiento estructurado de datos.  
  - Dashboards: Grafana y Node-Red para la presentación visual y análisis de información.

- **Contenedorización y Despliegue:**  
  - Uso de Docker para una implementación modular y escalable del sistema.

- **Protocolos de Comunicación:**  
  - MQTT: Comunicación a través del broker Mosquitto (test.mosquitto.org).  
  - LoRa: Comunicación punto a punto sin protocolo LoRaWAN (TX-RX).  
  - WiFi: Nodo con función de gateway, facilitando la integración en entornos sin conexión a internet.

## Enfoque Metodológico ABP

- **Trabajo Colaborativo y Metodologías Ágiles:**  
  - Desarrollo en equipo mediante Scrum y Kanban, permitiendo iteraciones y retroalimentación constante.
  
- **Soporte y Asesoría:**  
  - Asistencia continua por parte del docente y soporte DevOps para la integración y optimización del sistema.

- **Documentación Continua y Seguimiento:**  
  - Registro detallado de decisiones, pruebas y mejoras en el repositorio de GitHub, asegurando la transparencia y trazabilidad durante el desarrollo.

## Infraestructura y Consideraciones Específicas

- **Energía y Conectividad:**  
  - La instalación cuenta con energía eléctrica proporcionada por generadores, aunque carece de conexión a internet, lo que implica el uso de soluciones locales y nodos de gateway.
  
- **Condiciones del Entorno:**  
  - Adaptación a un entorno industrial donde la emisión de gases inflamables puede representar un riesgo, enfatizando la necesidad de una respuesta rápida y una supervisión continua.

## Validación y Pruebas

- **Simulación y Testeo:**  
  - Uso del simulador Wokwi para validar la funcionalidad de sensores y dispositivos antes de la implementación en el entorno real.
  
- **Configuración de Umbrales:**  
  - Ensayos para establecer y ajustar los parámetros de seguridad que disparen el sistema de extracción, garantizando un análisis preventivo y la detección temprana de fallas.

---

Este apartado de requisitos sienta las bases necesarias para el desarrollo completo del sistema, asegurando que se aborden todas las necesidades operativas y tecnológicas del proyecto en un ambiente de aprendizaje colaborativo y práctica real.  

---

## 📄 Licencia

Distribuido bajo la Licencia Creative Commons.

---
