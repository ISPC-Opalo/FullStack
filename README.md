![Logo de la Institución ISPC](E%20assets/caratula.png)

# Módulo Programador FullStack IoT
## Tecnicatura Superior en Telecomunicaciones – Segundo Año

---------------------------

### Profesores
- Ing. Morales Jorge Elias | https://github.com/JorEl057
- Mario Alejandro Gonzalez | https://github.com/mariogonzalezispc
- Alejandro Mainero

### Miembros:
- Lujan, Luciano | GitHub: https://github.com/lucianoilujan
- Durigutti, Vittorio | GitHub: https://github.com/vittoriodurigutti
- Zalazar, Joaquin | GitHub: https://github.com/breaakerr
- Juncos, Lisandro | GitHub: https://github.com/Lisandro-05
- Velez, Nahuel | GitHub: https://github.com/ISPC-TST-PI-I-2024/ISPC_PI_Lucas_Nahuel_Velez 
- Marquez, Jose | GitHub: https://github.com/ISPC-TST-PI-I-2024/josemarquez.git
- Guzmán, Maria Lilen | GitHub: https://github.com/lilenguzman01
- Paez, Tiziano | Github: https://github.com/tpaez

### Índice


| [![Demostracion del uso automatico](E%20assets\Demostracion_uso.png)](https://youtube.com/shorts/zFDpbnvFVWU?feature=share) | [![Demostracion del uso manual](E%20assets\Demostracion_uso.png)](https://youtube.com/shorts/pIPmyRFcj_Q?feature=share)|



---------------------------
### Estructura del Repositorio

- **A requisitos**: Contiene documentos de requisitos proporcionados por el docente.
- **B investigacion**: Investigaciones realizadas por los estudiantes.
- **C prototipo**: Implementaciones específicas y código prototipo para el proyecto.
- **D presentacion**: Incluye grabaciones y bitácoras de las reuniones de Scrum, así como las presentaciones de progreso.
- **E assets**: Contiene recursos gráficos como imágenes y otros archivos necesarios para la documentación.

### 🔹 Presentación General  

El módulo Programador FullStack IoT es un espacio interdisciplinario que integra las materias Arquitectura y Conectividad, Sistemas de Control y Servicios y Plataformas, orientado al diseño e implementación de soluciones IoT aplicadas a la industria.
Los estudiantes trabajarán en equipos desarrollando un proyecto técnico completo que abarque sensado, conectividad, automatización, visualización de datos y documentación profesional.
El trabajo se organiza bajo el enfoque de Aprendizaje Basado en Proyectos (ABP), con metodologías ágiles Scrum y Kanban.
El desarrollo debe gestionarse en GitHub y documentarse en el propio repositorio.

---------------------------

### Links de Uso y Presentacion:

El proyecto dispone de variedad de paneles de informacion, creados y gestionados via grafana, con los que se expone informacion la informacion recabada por nuestros dispositivos. 
Permitiendo tener en tiempo real una vista del estado de los mismos, y del entorno que sensan. Dejamos a contiunacion una serie de links a cada uno de paneles de forma que puedan observar lo realizado, y tener una mirada del estado de nuestro proyecto

**Dashboard [Grafana]**
- [Mediciones de Gas](http://telecomunicaciones.ddns.net:8080/grafana/public-dashboards/5c6d33af6d3c4dd8b2dc677b6a31fec4)
- [Metricas en Tiempo Real](http://telecomunicaciones.ddns.net:8080/grafana/public-dashboards/8f8a0a1b3fe84d4e86012579bedf86bd)
- [Metricas en Tiempo Real con interaccion via NODE-RED](http://telecomunicaciones.ddns.net:8080/nodered_opalo/ui/#!/0?socketid=M7q85yKFzJ3xeGtpAAAL)


<p align="center">
  <img src="E%20assets/grafana1.png" alt="Imagen 1" width="400"/>
  <img src="E%20assets/grafana2.png" alt="Imagen 2" width="400"/>
  <img src="E%20assets/grafana3.png" alt="Imagen 3" width="400"/>
  <img src="E%20assets/Nodered.png" alt="Imagen 4" width="400"/>
</p>

---------------------------

### 🔹 Selección del Proyecto  

Sistema de detección y extracción de gases inflamables 🔥​​🚨​

### 🔹 Problemática a tratar
Disponemos de una localización con maquinaria con alta posibilidad de emanación de gases contaminantes inflamables. Los mismos no son problemáticos exceptuando concentración alta durante periodos prolongados. Tenemos distribuidos una serie de de sensores de gas combustibles a lo largo del deposito mencionado, ubicados estratégicamente. El mismo dispone de energía eléctrica provista por generadores, pero no de internet. Mediante la aplicación de dispositivos sensores con comunicación LoRa incorporado buscamos estar informados en el estado a tiempo real dentro de el sitio. Esto nos permite llevar un seguimiento y análisis preventivo, e identificar fallas que deban requerir intervención humana. Pero a su vez, la distancia supone un problema para asistir fallas, por lo que disponemos de dispositivos extractores con potencia variable distribuidos dentro. Nuestro sistema receptor se encarga de la manipulación de los umbrales mediante los cuales se dispara la accion y potencia de dichos extractores. Disponemos como extra de accionadores manuales remotos via apps con los que disparar los extractores ante criterio humano.

-----------------------------

### Stack Tecnológico Común

- Control de Versiones: **Git y GitHub**
- Metodologías Ágiles: **Scrum y Kanban**
- Aprendizaje Basado en Proyectos (ABP)
- Soporte DevOps por parte del docente

### Stack Tecnológico para el desarrollo

- IDE: **Visual Studio Code**
- Simulador: **Wokwi**

### Base de Datos y visualizacion:

- DB: **MariaDB**
- Dashboard: **Grafana**, **Node Red**

###  Despliegue

- Contendores: **Docker**

### Comunicacion + Protocolos
- [API_en_python](C%prototipo/Backend_API/Readme.md)
- MQTT: Broker: Mosquitto (test.mosquitto.org) | 
- Lora: Sin protocolo LoRaWAN - Comunicacion punto-punto TX-RX  
- Wifi: Nodo con funcion Gateway

-----------------------------

Arquitectura del Sistema 

![Arquitectura del sistema](E%20assets/arquitectura2.png)

-----------------------------

🔁 Organización por Sprints
A continuación, se detalla la planificación semanal del módulo, dividida en tres sprints:  


## SPRINT 1  

### Exploración y Diseño Conceptual (Semanas 1 a 3)
🎯 **Objetivo:** Identificar la problemática industrial, investigar, seleccionar tecnologías y diseñar la arquitectura del sistema.
- Conformación de equipos y análisis de áreas.
- Benchmarking tecnológico y definición del problema.
- Selección de sensores, actuadores y protocolos.
- Diseño preliminar de red IoT y lógica de control.
- Creación del repositorio en GitHub.
- Primeros diagramas de arquitectura y flujo.

-----------------------------

## SPRINT 2  

### Desarrollo e Integración Técnica (Semanas 4 a 7)
🎯 **Objetivo**: Desarrollar el sistema, integrar sensores, lógica de control y plataforma IoT.
- Conexión de sensores físicos o virtuales.
- Implementación de lógica de automatización.
- Ingesta de datos y visualización inicial en dashboard.
- Pruebas funcionales del sistema integrado.
- Validación técnica y mejoras sobre el prototipo.

-----------------------------

## SPRINT 3  

### Optimización y Presentación Final (Semanas 8 a 10)
🎯 **Objetivo**: Optimizar el sistema, completar la documentación técnica y presentar el proyecto final.
- Ajustes técnicos y mejoras visuales.
- Finalización de la documentación por materias.
- Validación cruzada entre equipos (testing).
- Ensayo y presentación final.
- Autoevaluación y coevaluación.

### 🎯 Entregable final (Semana 10)  

**Prototipo funcional (simulado o físico)**

**Dashboard operativo**

**Documentación técnica completa**

**Repositorio Git con historial del trabajo**

**Exposición y defensa del proyecto en equipo**

-----------------------------

## Licencia

Este proyecto está licenciado bajo la Licencia Creative Commons Atribución-NoComercial (CC BY-NC). Esta licencia permite que otros remixen, adapten y construyan sobre el trabajo de forma no comercial y, aunque sus nuevos trabajos deben también reconocer al autor original y ser no comerciales, no tienen que licenciar sus obras derivadas en los mismos términos.

Esta licencia es adecuada para un uso educativo y de aprendizaje, permitiendo la libre distribución y utilización del material mientras se protege contra el uso comercial sin autorización previa. Para usos comerciales, es necesario contactar a los autores para obtener permiso.

Para obtener más información sobre esta licencia y ver una copia completa de sus términos, visite [Creative Commons Atribución-NoComercial (CC BY-NC)](https://creativecommons.org/licenses/by-nc/4.0/).
