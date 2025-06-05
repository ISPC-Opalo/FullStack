![Logo de la Institución ISPC](/E%20assets/caratula.png)

## DISEÑO DE LA BASE DE DATOS:

### a. Argumentos del Diseño:  

### * ***Tabla Dispositivo:***  

- Campos:
  
**dispositivo_id:** ID único del dispositivo (clave primaria).
  
**nombre:** Nombre del dispositivo.

**descripcion:** Descripción del dispositivo.

**ubicacion:** Ubicación del dispositivo.


	*Relación: Cada dispositivo puede tener múltiples sensores (1:N).* 

---
### - ***Tabla Sensor:*** 

- Campos:
  
**sensor_id:** ID único del sensor (clave primaria).

**dispositivo_id:** ID del dispositivo al que pertenece el sensor (clave foránea).

**ppm:** Nivel de gas en partes por millón.

**valor:** Valor general del sensor.

**crudo:** Valor crudo del sensor.

**estado_sensor:** Estado del sensor.

**umbral:** Umbral de gas para activar alarmas.


	*Relación: Cada sensor está vinculado a un dispositivo (1:1).*

---
### - ***Tabla Medicion:***

- Campos:
  
**medicion_id:** ID único de la medición (clave primaria).

**dispositivo_id:** ID del dispositivo al que pertenece la medición (clave foránea).

**auto:** Indica si el control es automático.

**encendido:** Indica si el actuador está encendido.

**vel_actual:** Velocidad actual del actuador.

**vel_objetivo:** Velocidad objetivo del actuador.

**transicion:** Indica si hay una transición gradual.

**timestamp:** Fecha y hora de la medición.


	*Relación: Cada dispositivo puede tener múltiples mediciones (1:N).*

---
### - ***Tabla Actuador:***

- Campos:
  
**id:** ID único del actuador (clave primaria).

**medicion_id:** ID de la medición al que pertenece el actuador (clave foránea).

**pin:** Pin del actuador.

**velocidad:** Velocidad actual del actuador.

**objetivo:** Velocidad objetivo del actuador.

**encendido:** Estado del actuador (SI/NO).

**transicion:** Indica si hay una transición gradual (SI/NO).

**pwm:** Valor PWM del actuador.

**nombre:** Nombre del actuador.


	*Relación: Cada medición puede tener múltiples actuadores (1:N).*

---
### b. Normalización:

***Primera Forma Normal (1NF):***

*Todas las tablas cumplen con la 1NF, ya que cada campo es atómico (no hay campos que contengan múltiples valores).*

***Segunda Forma Normal (2NF):***

*Todas las tablas cumplen con la 2NF, ya que cada tabla tiene una clave primaria única y no hay dependencias parciales.*

***Tercera Forma Normal (3NF):***

*Todas las tablas cumplen con la 3NF, ya que no hay dependencias transitivas entre campos no clave.*

---
### c. Código de la base de datos:
 
---
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
-- Host: telecomunicaciones.ddns.net    Database: OpaloDB
-- Server version	11.7.2-MariaDB-ubu2404
-- ------------------------------------------------------

    CREATE DATABASE IF NOT EXISTS OpaloDB;
	USE Opalobd;
    
    CREATE TABLE IF NOT EXISTS dispositivo (
        dispositivo_id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(50),
        descripcion VARCHAR(100),
        ubicacion VARCHAR(100)
    );
    
    CREATE TABLE IF NOT EXISTS sensor (
        sensor_id INT AUTO_INCREMENT PRIMARY KEY,
        dispositivo_id INT,
        ppm FLOAT,
        valor FLOAT,
        crudo INT,
        estado_sensor VARCHAR(20),
        umbral FLOAT,
        FOREIGN KEY (dispositivo_id) REFERENCES dispositivo(dispositivo_id)
            ON DELETE CASCADE
    );
    
    CREATE TABLE IF NOT EXISTS medicion (
        medicion_id INT AUTO_INCREMENT PRIMARY KEY,
        dispositivo_id INT,
        auto BOOLEAN,
        encendido BOOLEAN,
        vel_actual INT,
        vel_objetivo INT,
        transicion BOOLEAN,
        timestamp DATETIME,  -- ahora usa fecha y hora
        FOREIGN KEY (dispositivo_id) REFERENCES dispositivo(dispositivo_id)
            ON DELETE CASCADE
    );
    
    CREATE TABLE IF NOT EXISTS actuador (
        id INT AUTO_INCREMENT PRIMARY KEY,
        medicion_id INT,
        pin INT,
        velocidad INT,
        objetivo INT,
        encendido VARCHAR(2),   -- 'SI' o 'NO'
        transicion VARCHAR(2),  -- 'SI' o 'NO'
        pwm INT,
        nombre VARCHAR(50),
        FOREIGN KEY (medicion_id) REFERENCES medicion(medicion_id)
            ON DELETE CASCADE
    );


*Importante solo para administradores:*
				
***En caso de necesitar eliminar y recrear la base de datos completa, usa:***

sql

- **DROP DATABASE IF EXISTS OpaloDB;**

- **CREATE DATABASE OpaloDB;**

Para ejecutar: Copia todo el código y ejecútalo en tu cliente SQL (MySQL Workbench, phpMyAdmin, etc.)

Las claves foráneas garantizan integridad referencial con ON DELETE CASCADE
