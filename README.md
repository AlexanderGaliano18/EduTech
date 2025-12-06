# 🖥️ EduTech ITSM | Plataforma de Gestión TI para Escuelas

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED)
![License](https://img.shields.io/badge/License-GPLv3-green)

> **Autor:** Alexander Richard Galiano Diaz  
> **Institución:** Universidad Científica del Sur  
> **Curso:** Software Libre  

## 📖 Descripción del Proyecto

**EduTech ITSM** es una solución tecnológica de código abierto diseñada para optimizar la gestión de activos informáticos y soporte técnico en Instituciones Educativas Estatales del Perú. 

Este repositorio contiene el módulo de **Analítica de Datos e Inteligencia de Negocios**, desarrollado en Python utilizando **Streamlit**. Este módulo se conecta a la infraestructura base (GLPI + MariaDB) para proporcionar a los directivos una visión clara y en tiempo real del estado de sus laboratorios de cómputo.

### 🎯 Objetivos
* **Automatizar** el inventario de hardware mediante agentes libres.
* **Visualizar** indicadores clave de desempeño (KPIs) como MTTR y cumplimiento de SLA.
* **Alertar** sobre la obsolescencia tecnológica para optimizar el presupuesto escolar.
* **Democratizar** el acceso a herramientas ITSM profesionales sin costo de licencias.

---

## 🚀 Características del Dashboard

El archivo `app.py` despliega un panel de control interactivo con las siguientes funcionalidades:

1.  **Monitor de Infraestructura:**
    * Visualización de activos totales e inventariados.
    * Estado de operatividad de los equipos en tiempo real.
2.  **Gestión de Soporte (ITIL):**
    * Métricas de cumplimiento de Acuerdos de Nivel de Servicio (SLA).
    * Cálculo del Tiempo Medio de Resolución (MTTR).
3.  **Gráficos Interactivos:**
    * Distribución de fallas por categoría (Hardware, Software, Red).
    * Estado de conservación del parque informático.
4.  **Alertas Inteligentes:**
    * Detección automática de equipos obsoletos (> 7 años de antigüedad).

---

## 🛠️ Instalación y Uso Local

Sigue estos pasos para ejecutar el proyecto en tu máquina local:

**1. Clonar el repositorio**
```bash
git clone [https://github.com/AlexanderGaliano18/EduTech-ITSM.git](https://github.com/AlexanderGaliano18/EduTech-ITSM.git)
cd EduTech-ITSM
