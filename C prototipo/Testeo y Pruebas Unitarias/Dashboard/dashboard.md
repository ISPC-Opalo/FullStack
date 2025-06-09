## 📊 Visualización con Grafana

Una vez que los datos provenientes del ESP32 fueron almacenados en la base de datos, se procedió a **conectar Grafana como herramienta de visualización**. A través de esta integración, fue posible consultar la base de datos en tiempo real y diseñar distintos **dashboards interactivos** que permiten monitorear los valores registrados por los sensores.

En Grafana se crearon **paneles personalizados** para:

- Visualizar la **concentración de gas** medida (en ppm).
- Establecer **umbrales críticos** de seguridad.
- Observar el **estado de los extractores** (encendido/apagado).
- Mostrar la **velocidad actual y la velocidad objetivo** del extractor.
- Analizar el **historial de mediciones**.

Esta visualización facilita la interpretación de los datos, la detección temprana de condiciones peligrosas y el control eficiente del sistema.

<img src="asset/img1.png" alt="Aplicación" width="700" height="300">

<img src="asset/img2.png" alt="Aplicación" width="700" height="300">

<img src="asset/img3.png" alt="Aplicación" width="700" height="300">
