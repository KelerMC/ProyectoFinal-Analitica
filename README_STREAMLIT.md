# Dashboard de Predicción de Demanda - Olist

Este proyecto contiene un dashboard interactivo para visualizar predicciones de demanda usando Prophet.

## 🚀 Instalación

```bash
pip install streamlit pandas numpy plotly prophet pyarrow
```

## 📊 Uso

### 1. Ejecutar el notebook de predicción (primero)

```bash
jupyter notebook modelo_prediccion_demanda.ipynb
```

Esto generará:
- `Data/pronostico_trimestral.csv`
- `Data/metricas_modelo_demanda.csv`

### 2. Lanzar el dashboard

```bash
streamlit run app_streamlit.py
```

El dashboard se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 🌐 Deploy en Streamlit Cloud (Gratis)

1. Sube tu proyecto a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repositorio
4. Selecciona `app_streamlit.py` como archivo principal
5. ¡Listo! Tu dashboard estará disponible públicamente

## 📁 Estructura del Proyecto

```
ProyectoFinal-Analitica/
├── Data/
│   ├── olist_unified_dataset.parquet
│   ├── pronostico_trimestral.csv
│   └── metricas_modelo_demanda.csv
├── modelo_prediccion_demanda.ipynb
├── app_streamlit.py
├── requirements.txt
└── README_STREAMLIT.md
```

## 🎯 Características del Dashboard

- 📊 Visualización interactiva del pronóstico
- 📈 Métricas clave en tiempo real
- 📅 Desglose semanal de predicciones
- 📋 Tabla descargable de resultados
- 💡 Insights y recomendaciones automáticas
- 🎨 Diseño profesional y responsive

## 🔧 Personalización

Edita `app_streamlit.py` para:
- Cambiar colores y estilos
- Agregar nuevas métricas
- Modificar visualizaciones
- Añadir filtros interactivos

## 📝 Notas

- El dashboard carga datos desde `Data/pronostico_trimestral.csv`
- Si no existe el archivo, ejecuta primero el notebook de predicción
- Los datos se cachean para mejorar el rendimiento
- Usa el botón "Reentrenar Modelo" para limpiar cache

## 🎓 Proyecto Académico

Desarrollado para el curso de Análisis Predictivo de Datos  
Universidad: [Tu Universidad]  
Autor: [Tu Nombre]  
Fecha: Diciembre 2025
