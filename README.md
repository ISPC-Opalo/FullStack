![Logo de la Institución ISPC](E%20assets/caratula.png)

# Módulo Programador FullStack IoT
## Tecnicatura Superior en Telecomunicaciones – Segundo Año

---------------------------

### Profesores
- Ing. Morales Jorge Elias | https://github.com/JorEl057
- Mario Alejandro Gonzalez | https://github.com/mariogonzalezispc
- Alejandro Mainero

### Miembros:
- Luciano Lujan | GitHub: https://github.com/lucianoilujan
- Durigutti, Vittorio | GitHub: https://github.com/vittoriodurigutti
- Joaquin Zalazar | GitHub: https://github.com/breaakerr
- Lisandro Juncos | GitHub: https://github.com/Lisandro-05
- Nahuel Velez | GitHub: https://github.com/ISPC-TST-PI-I-2024/ISPC_PI_Lucas_Nahuel_Velez 
- Jose Marquez | GitHub: https://github.com/ISPC-TST-PI-I-2024/josemarquez.git
- Maria Lilen Guzmán | GitHub: https://github.com/lilenguzman01
- Tiziano Paez | Github: https://github.com/tpaez
### Índice

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

### 🔹 Selección del Proyecto  

Sistema de detección y extracción de gases inflamables 🔥​​🚨​

### 🔹 Problemática a tratar
Disponemos de una localización con maquinaria con alta posibilidad de emanación de gases contaminantes inflamables. Los mismos no son problemáticos exceptuando concentración alta durante periodos prolongados. Tenemos distribuidos una serie de de sensores de gas combustibles a lo largo del deposito mencionado, ubicados estratégicamente. El mismo dispone de energía eléctrica provista por generadores, pero no de internet. Mediante la aplicación de dispositivos sensores con comunicación LoRa incorporado buscamos estar informados en el estado a tiempo real dentro de el sitio. Esto nos permite llevar un seguimiento y análisis preventivo, e identificar fallas que deban requerir intervención humana. Pero a su vez, la distancia supone un problema para asistir fallas, por lo que disponemos de dispositivos extractores con potencia variable distribuidos dentro. Nuestro sistema receptor se encarga de la manipulación de los umbrales mediante los cuales se dispara la accion y potencia de dichos extractores. Disponemos como extra de accionadores manuales remotos via apps con los que disparar los extractores ante criterio humano.

-----------------------------

## Stack Tecnológico Común

- Control de Versiones: **Git y GitHub**
- Metodologías Ágiles: **Scrum y Kanban**
- Aprendizaje Basado en Proyectos (ABP)
- Soporte DevOps por parte del docente

## Stack Tecnológico para el desarrollo

- IDE: **Visual Studio Code**
- Simulador: **Wokwi o similar**
-----------------------------

Flujo de Accion (provisorio)

![Flujo de datos](E%20assets/flujoDatos.png)




-----------------------------

Arquitectura del Sistema 

![Arquitectura del sistema](E%20assets/arquitectura.png)

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

## Linea de Trabajo del Proyecto

**Semana 1:** Definición de alcance y arquitectura
- Terminar de definir qué módulos van a tener (control de stock, pedidos, AGV virtual, dashboard).
- Diagramar la arquitectura de conectividad (qué se comunica con qué, cómo).

- Tecnologias a usar: 

----Entregable: Mapa de arquitectura + definición de herramientas.

**Semana 2:** Modelado de stock y pedidos
- Armar una base de datos o sistema simple para manejar inventario.
- Programar la entrada de pedidos manual o simulada (por ejemplo, cada cierto tiempo se genera un pedido).

----Entregable: Simulación de pedidos + base de stock inicial.

**Semana 3:** Simulación de AGV
- Crear un AGV virtual: que "reciba" una orden y la "ejecute" (puede ser moverse en un mapa simple, o simplemente cambiar un estado).
- Que reporte su estado ("En camino", "Entregado", etc.).

----Entregable: AGV funcional en simulación.

**Semana 4:** Automatización de entrada/salida de stock
- Al completar una entrega, el stock debe actualizarse automáticamente.
- Validar pedidos contra stock disponible.

----Entregable: Flujo cerrado: Pedido → AGV → Entrega → Stock actualizado.

**Semana 5:** Dashboard o consola de control
- Montar una vista para monitorear stock, pedidos pendientes y estado de AGVs.
- Puede ser algo sencillo: una web estática con actualizaciones en vivo, un Node-RED dashboard, o un panel en Python.

----Entregable: Dashboard operativo.

**Semana 6:** Testing completo y mejoras
- Hacer correr simulaciones múltiples: varios pedidos, varias entregas.
- Corregir bugs y mejorar la experiencia (por ejemplo, mostrar alarmas si el stock es bajo).

----Entregable: Sistema testeado de punta a punta.

**Semana 7:** Preparación final
- Armado de la presentación.
- Documentación clara de arquitectura, flujo, problemas encontrados, oportunidades de mejora.
- Práctica de la demo.

----Entregable: Demo lista + Informe final + Slides de presentación.

-----------------------------

## Licencia

Este proyecto está licenciado bajo la Licencia Creative Commons Atribución-NoComercial (CC BY-NC). Esta licencia permite que otros remixen, adapten y construyan sobre el trabajo de forma no comercial y, aunque sus nuevos trabajos deben también reconocer al autor original y ser no comerciales, no tienen que licenciar sus obras derivadas en los mismos términos.

Esta licencia es adecuada para un uso educativo y de aprendizaje, permitiendo la libre distribución y utilización del material mientras se protege contra el uso comercial sin autorización previa. Para usos comerciales, es necesario contactar a los autores para obtener permiso.

Para obtener más información sobre esta licencia y ver una copia completa de sus términos, visite [Creative Commons Atribución-NoComercial (CC BY-NC)](https://creativecommons.org/licenses/by-nc/4.0/).
