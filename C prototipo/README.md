![Logo de la Institución ISPC](/E%20assets/caratula.png)

# INSTITUTO SUPERIOR POLITECNICO CORDOBA
## TECNICATURA SUPERIOR EN TELECOMUINICACIONES - COHORTE 2024.


# C - Prototipo

El prototipo es la materialización práctica de nuestro proyecto orientado al monitoreo y gestión de dispositivos en entornos con riesgo de acumulación de gases inflamables. En esta etapa implementamos y validamos la solución IoT, integrando sensores, comunicación (LoRa, MQTT y WiFi), procesamiento de datos y accionamiento automatizado y manual de dispositivos extractores.

## Descripción del Prototipo

El sistema desarrollado permite:
- **Monitoreo en tiempo real:** Captura de datos de sensores de gas distribuidos estratégicamente.
- **Comunicación eficiente:** Transmisión de datos mediante LoRa (punto a punto) y MQTT (broker privado, provisto por el docente) a través de un nodo WiFi que actúa como gateway.
- **Accionamiento automatizado y manual:** Activación de extractores con potencia variable cuando los niveles de gas superan los umbrales establecidos y mediante accionadores remotos vía aplicaciones.
- **Visualización e integración de datos:** Almacenamiento en MariaDB y monitoreo en tiempo real mediante dashboards en Grafana y Node-Red.

## Arquitectura del Sistema

El prototipo se compone de los siguientes módulos:
- **Sensores de Gas:** Simulados y validados en el entorno de Wokwi.
- **Módulo de Comunicación:**  
  - **LoRa:** Comunicación punto a punto para la transmisión directa de datos.  
  - **MQTT:** Utilización del broker Mosquitto (test.mosquitto.org) para la mensajería.
  - **WiFi Gateway:** Nodo que integra la comunicación en un entorno sin conexión a internet.
- **Backend y Base de Datos:** Implementación de MariaDB para el almacenamiento estructurado de datos.
- **Dashboards de Visualización:** Uso de Grafana y Node-Red para el monitoreo interactivo y en tiempo real.
- **Sistema de Accionamiento:** Control de extractores basado en umbrales configurables, incorporando pruebas de activación tanto automáticas como manuales.

## Herramientas y Tecnologías Utilizadas

- **IDE:** Visual Studio Code.
- **Simulador:** Wokwi para la validación y pruebas de dispositivos y comunicación.
- **Contenedorización:** Docker, que facilita el despliegue modular y escalable del prototipo.
- **Protocolos de Comunicación:**  
  - MQTT: Broker Mosquitto (test.mosquitto.org).  
  - LoRa: Comunicación punto a punto sin protocolo LoRaWAN.  
  - WiFi: Nodo con función de gateway.
- **Base de Datos y Visualización:**  
  - MariaDB para el almacenamiento.  
  - Grafana y Node-Red para la monitorización en tiempo real.

---

## Pruebas y Validación

- **Simulación de Sensores:**  
  Uso del simulador Wokwi para ejecutar pruebas con dispositivos virtuales, comprobando la correcta recepción de datos.
- **Unit Testing e Integración:**  
  Implementación de pruebas unitarias e integradas para asegurar la estabilidad de cada módulo del prototipo.
- **Validación de Umbrales y Accionamiento:**  
  Pruebas que confirman la activación automática de extractores al detectar concentraciones elevadas, así como la respuesta ante intervenciones manuales.

## Futuras Mejoras y Consideraciones

- **Optimización de la Interfaz:** Mejorar la usabilidad y la representación gráfica de los dashboards.
- **Integración de Análisis Predictivo:** Incorporar módulos de inteligencia artificial para prever incidencias basadas en patrones recogidos.
- **Ampliación de la Red de Sensores:** Desplegar el sistema en condiciones reales y aumentar la densidad de sensores para mayor precisión.

## Conclusión

El prototipo demuestra la viabilidad técnica y funcional de nuestro sistema IoT para el monitoreo y la respuesta en entornos industriales críticos. Gracias al enfoque ABP y la integración de metodologías ágiles, hemos podido iterar sobre el diseño, validar conceptos y sentar las bases para una implementación final sólida y escalable.

---

Este README resume el desarrollo e implementación del prototipo, ofreciendo directrices claras para reproducir, probar y validar el sistema. Si deseas profundizar en algún componente o revisar los detalles técnicos, consulta las secciones correspondientes en el repositorio.  

---

## 📄 Licencia

Distribuido bajo la Licencia Creative Commons.

---
