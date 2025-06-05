![Logo de la Institución ISPC](/E%20assets/caratula.png)

# INSTITUTO SUPERIOR POLITECNICO CORDOBA
## TECNICATURA SUPERIOR EN TELECOMUINICACIONES - COHORTE 2024.

# B - Investigación

La fase de investigación es fundamental en nuestro enfoque ABP, ya que nos permite comprender en profundidad la problemática y las soluciones tecnológicas disponibles para la implementación del sistema IoT. Esta etapa integra la revisión de documentación técnica, normativas y estudios de casos, lo que nos ha permitido sentar las bases para el diseño y desarrollo del sistema.

## Objetivos de la Investigación

- **Comprender la problemática:**  
  Analizar el entorno en el que se ubica la maquinaria con riesgo de emisión de gases inflamables y los efectos de concentraciones elevadas durante períodos prolongados.
  
- **Evaluar tecnologías y dispositivos:**  
  Investigar la viabilidad y características de los sensores de gas combustibles, así como los módulos de comunicación LoRa utilizados en el proyecto.

- **Investigar protocolos y comunicación:**  
  Estudiar la integración de protocolos como MQTT (a través del broker privado, provisto por el docente) y la implementación de nodos WiFi con función de gateway, indispensables para entornos sin acceso a internet.

- **Analizar la integración de sistemas de extracción:**  
  Revisar soluciones y mecanismos para el accionamiento automatizado y manual de dispositivos extractores, incluidos los criterios de activación basados en umbrales definidos.

## Fuentes y Materiales de Investigación

- **Datasheets y Documentación Técnica:**  
  Se han revisado los datasheets de sensores de gas, módulos LoRa y extractores de potencia variable, obteniendo información sobre rangos de operación, especificaciones técnicas y procedimientos de integración.

- **Herramientas de Simulación:**  
  Uso del simulador Wokwi para validar la interacción entre sensores, la transmisión mediante LoRa y la comunicación MQTT, permitiendo ensayar el comportamiento del sistema antes de su despliegue.

## Metodología y Enfoque ABP

- **Aprendizaje Basado en Proyectos (ABP):**  
  El enfoque ABP orientó la investigación de forma práctica y colaborativa, combinando la revisión bibliográfica con la experimentación en laboratorio.

- **Metodologías Ágiles:**  
  Se aplicaron técnicas de Scrum y Kanban para organizar las tareas de investigación, garantizando iteraciones y retroalimentación constante durante el proceso.

- **Soporte DevOps:**  
  La asesoría constante del docente y el soporte en temas DevOps facilitaron la integración y el testeo continuo de los prototipos desarrollados.

## Hallazgos y Conclusiones

- **Viabilidad Tecnológica:**  
  La integración de sensores de gas con módulos LoRa, junto con la transmisión de datos a través de MQTT, es factible para el monitoreo en tiempo real del entorno, incluso en ausencia de conexión a internet.

- **Puntos Críticos y Desafíos:**  
  La ausencia de internet impone la necesidad de implementar soluciones locales, como el nodo WiFi con función de gateway. Además, la calibración de umbrales y la distribución estratégica de dispositivos son esenciales para evitar activaciones innecesarias o fallos en el sistema.

- **Potencial de Mejora:**  
  La incorporación de dashboards con Grafana y Node-Red para la visualización de datos en tiempo real ofrece un gran potencial para la optimización del seguimiento y análisis en un entorno industrial.

## Siguientes Pasos

- Realizar pruebas piloto con dispositivos reales en entornos controlados para validar los hallazgos durante la investigación.
- Profundizar en la integración de los protocolos de comunicación y la configuración de parámetros críticos para el accionamiento de dispositivos extractores.
- Documentar detalladamente los resultados y ajustes en el repositorio, asegurando una trazabilidad completa que respalde el proceso de desarrollo.

---

Este documento resume la fase de investigación de nuestro proyecto, estableciendo una base sólida de conocimientos y orientaciones que guiarán el desarrollo e implementación del sistema IoT. La colaboración y el análisis crítico han sido fundamentales para identificar soluciones innovadoras adaptadas a las necesidades específicas del entorno.  

---

## 📄 Licencia  

Distribuido bajo la Licencia Creative Commons.

---
