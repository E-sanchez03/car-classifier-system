# 🚗 Sistema Clasificador de Coches en Tiempo Real con IA y Kafka

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?style=for-the-badge&logo=tensorflow)](https://www.tensorflow.org/)
[![Keras](https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=keras)](https://keras.io/)
[![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-231F20?style=for-the-badge&logo=apachekafka)](https://kafka.apache.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)

</div>

---

## 📖 Tabla de Contenidos

- [📝 Acerca del Proyecto](#-acerca-del-proyecto)
- [✨ Características Principales](#-características-principales)
- [🏛️ Arquitectura del Sistema](#️-arquitectura-del-sistema)
- [🛠️ Stack Tecnológico](#️-stack-tecnológico)
- [🚀 Instalación y Puesta en Marcha](#-instalación-y-puesta-en-marcha)
  - [Prerrequisitos](#prerrequisitos)
  - [Pasos de Instalación](#pasos-de-instalación)
- [🕹️ Uso](#️-uso)
- [📊 Dataset](#-dataset)
- [🔮 Mejoras Futuras](#-mejoras-futuras)
- [📄 Licencia](#-licencia)

---

## 📝 Acerca del Proyecto

Este proyecto implementa un sistema completo para la clasificación de modelos de coches a partir de imágenes, simulando un pipeline de datos en tiempo real. La solución está diseñada para emular un escenario de producción donde una cámara captura imágenes de vehículos, y un servicio de inteligencia artificial las procesa para su identificación.

La arquitectura está desacoplada en microservicios que se comunican a través de un bus de mensajería (Apache Kafka), lo que permite que el sistema sea escalable, robusto y fácil de mantener.

---

## ✨ Características Principales

* **Clasificación de Imágenes de Alta Precisión:** Utiliza un modelo `ResNet50` pre-entrenado y afinado (*fine-tuning*) sobre el dataset CompCars para lograr una clasificación detallada de modelos de vehículos.
* **Pipeline de Datos en Tiempo Real:** Simula un flujo de datos continuo desde una cámara mediante **Apache Kafka**, una tecnología estándar en la industria para el streaming de eventos.
* **Arquitectura Desacoplada:** El sistema se divide en un **Productor** (la cámara simulada) y un **Consumidor** (el servicio de clasificación), permitiendo que operen y escalen de forma independiente.
* **Infraestructura Contenerizada:** El backend de mensajería (Kafka y su dependencia ZooKeeper) se gestiona de forma limpia y reproducible a través de **Docker** y **Docker Compose**.

---

## 🏛️ Arquitectura del Sistema

El flujo de trabajo del sistema está diseñado para ser simple y eficiente. El productor captura una imagen, la serializa y la envía a un tópico de Kafka. El consumidor, que está suscrito a dicho tópico, la recoge para su análisis y clasificación.

```mermaid
graph TD
    A[Productor - Cámara<br>(productor_camara.py)] -- Envía Imagen (JSON + Base64) --> B(Tópico Kafka<br>'taller_camara_stream');
    B -- Recibe Mensaje --> C[Consumidor - Clasificador<br>(consumidor_clasificador.py)];
    C -- Procesa y Predice --> D{Resultado<br>Marca, Modelo, Confianza};
```

---

## 🛠️ Stack Tecnológico

A continuación se listan las tecnologías y librerías clave utilizadas en este proyecto:

* **Modelado de IA:**
    * `TensorFlow 2.x` / `Keras 3`
* **Streaming de Datos:**
    * `Apache Kafka`
* **Infraestructura y Contenerización:**
    * `Docker` / `Docker Compose`
* **Lenguaje y Librerías Principales:**
    * `Python 3.10+