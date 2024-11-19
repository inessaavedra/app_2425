# Análisis de Preferencias en Netflix

## Descripción de la Aplicación

Esta aplicación, permite analizar las preferencias de visualización de perfiles de Netflix, proporcionando una experiencia interactiva para entender los hábitos de consumo de contenido. La aplicación utiliza **Dash** para la creación de gráficos y paneles dinámicos, integrando análisis de datos avanzados y un modelo predictivo para determinar si el perfil analizado prefiere ver series o películas.

## Funcionalidades

- **Selección de perfil**: Los usuarios pueden seleccionar un perfil de Netflix para visualizar estadísticas específicas.
- **Número total de visualizaciones**: Muestra la cantidad total de visualizaciones para el perfil seleccionado.
- **Predicción del género preferido**: Basado en un modelo predictivo, la aplicación determina si el perfil tiene una preferencia por series o películas.
- **Justificación de la predicción**: Proporciona gráficos comparativos que explican la decisión del modelo.
- **Gráficos interactivos**:
  - **Duración semanal de visualización**: Un gráfico de línea que muestra la evolución del tiempo de visualización por semana.
  - **Top 10 series y películas**: Gráficos de barra que destacan los títulos más vistos.
  - **Frecuencia de visualización por día y hora**: Gráficos de barra y distribución que muestran los días y horas preferidos para consumir contenido.

## Modelo Predictivo

La aplicación utiliza un modelo de clasificación entrenado con datos del historial de visualización para predecir si el usuario prefiere ver series o películas. Este modelo se reentrena dinámicamente según el perfil seleccionado para asegurar predicciones personalizadas.

## Tecnologías Utilizadas

- **Dash**: Framework de Python para la creación de aplicaciones web interactivas.
- **Plotly**: Librería para la visualización de gráficos avanzados.
- **Pandas**: Para el procesamiento y análisis de datos.
- **Scikit-learn**: Para el entrenamiento del modelo predictivo.
- **Gunicorn**: Servidor WSGI para desplegar la aplicación en producción.

## Estructura del Proyecto

Estructura del Proyecto

app_2425/
├── app.py   # Archivo principal de la aplicación

├── requirements.txt        # Dependencias necesarias

├── Procfile                # Configuración de Gunicorn para el despliegue

├── runtime.txt             # Versión de Python utilizada

├── src/

│   ├── netflix_genre_model.py  # Módulo para el modelo predictivo

│   ├── ViewingActivity.csv     # Dataset de visualización de Netflix


## Despliegue 

La aplicación ha sido desplegada con Render en el siguiente link: https://app-2425.onrender.com

## Running the App

Opcion 1) Navegar al link de Render: https://app-2425.onrender.com

Opción 2) Run `python3 app.py` y navegar a http://127.0.0.1:8050/
