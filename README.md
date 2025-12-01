# Proyecto Final - Analítica de Datos E-commerce Olist

## Grupo 8

### Integrantes
- Modesto Calixto, Keler
- Ormeño Vasquez, Leonardo
- Romero Llamoca, Carlos
- Salazar Herrera, Oscar Miguel
- Villar Arias, Angelo

## Objetivo del Proyecto

El presente proyecto tiene como objetivo realizar un análisis integral de datos del e-commerce brasileño Olist, aplicando los cinco tipos de análisis de datos (Descriptivo, Diagnóstico, Predictivo, Prescriptivo y Cognitivo) para extraer insights accionables que permitan mejorar la satisfacción del cliente, optimizar operaciones logísticas y aumentar las ventas de la plataforma.

## Dataset

Se trabajará con el conjunto de datos públicos de Olist, compuesto por 8 archivos CSV que contienen información sobre:
- Órdenes de compra
- Clientes
- Productos
- Vendedores
- Pagos
- Reseñas
- Geolocalización

## Estructura del Análisis

### 1. Análisis Descriptivo: ¿Qué pasó?

El análisis descriptivo nos permite entender el estado actual del negocio mediante indicadores clave de rendimiento (KPIs).

#### KPI 1: Ventas Totales y Evolución
- **Archivos**: `olist_orders_dataset.csv` + `olist_order_payments_dataset.csv`
- **Método**: Unir por `order_id`, sumar `payment_value` y agrupar por `order_purchase_timestamp` (mes/año)
- **Pregunta**: ¿Cuánto vendimos y cuál es la tendencia de ventas?

#### KPI 2: Geografía de Clientes
- **Responsable**: Carlos
- **Archivo**: `olist_customers_dataset.csv`
- **Método**: Contar `customer_unique_id` agrupando por `customer_state`
- **Pregunta**: ¿Dónde se concentran nuestros clientes?
- **Visualización**: Mapa de Brasil con distribución de clientes

#### KPI 3: Categorías de Productos más Vendidas
- **Responsable**: Leonardo
- **Archivos**: `olist_order_items_dataset.csv` + `olist_products_dataset.csv` + `product_category_name_translation.csv`
- **Método**: Unir por `product_id` y `product_category_name`, contar `order_item_id` por `product_category_name_english`
- **Pregunta**: ¿Qué categorías de productos vendemos más?

#### KPI 4: Métodos de Pago Preferidos
- **Responsable**: Angelo
- **Archivo**: `olist_order_payments_dataset.csv`
- **Método**: Contar `order_id` agrupando por `payment_type`
- **Pregunta**: ¿Cómo prefieren pagar nuestros clientes?

### 2. Análisis Diagnóstico: ¿Por qué pasó?

**Problema Central**: ¿Por qué tenemos reseñas de 1 estrella?

#### Hipótesis 1: Demora en la Entrega
- **Archivos**: `olist_orders_dataset.csv` + `olist_order_reviews_dataset.csv`
- **Análisis**:
  - Calcular Tiempo de Entrega Real: `order_delivered_customer_date - order_purchase_timestamp`
  - Calcular Diferencia con Estimación: `order_estimated_delivery_date - order_delivered_customer_date` (valor negativo = entrega tardía)
  - Correlacionar `review_score = 1` con diferencia de entrega
- **Diagnóstico esperado**: Identificar si los retrasos están correlacionados con reseñas negativas

#### Hipótesis 2: Costo del Envío
- **Archivos**: `olist_order_reviews_dataset.csv` + `olist_order_items_dataset.csv`
- **Análisis**: Correlacionar `review_score` con `freight_value`
- **Diagnóstico esperado**: Determinar si el costo de envío influye en la satisfacción del cliente

#### Hipótesis 3: Vendedores Problemáticos
- **Archivos**: `olist_order_reviews_dataset.csv` + `olist_order_items_dataset.csv`
- **Análisis**: Agrupar por `seller_id` y calcular `review_score` promedio por vendedor
- **Diagnóstico esperado**: Identificar vendedores con bajo desempeño que concentran reseñas negativas

### 3. Análisis Predictivo: ¿Qué pasará?

#### Modelo 1: Predicción de Satisfacción del Cliente (Clasificación)
- **Objetivo**: Predecir si una orden recibirá una mala calificación (`review_score = 1`)
- **Variable Objetivo (Y)**: `review_score` (binaria: 1 = Malo, 0 = Bueno)
- **Variables Predictoras (X)**:
  - `price`, `freight_value` (de `olist_order_items_dataset.csv`)
  - `product_category_name`, `product_weight_g` (de `olist_products_dataset.csv`)
  - `tiempo_estimado_entrega` (calculada de `olist_orders_dataset.csv`)
  - `seller_state` (de `olist_sellers_dataset.csv`)
- **Algoritmos**: Logistic Regression, Random Forest
- **Resultado**: Probabilidad de reseña de 1 estrella para cada orden

#### Modelo 2: Predicción de Demanda (Series de Tiempo)
- **Objetivo**: Predecir el volumen de ventas para el próximo trimestre
- **Datos**: Series temporales de `payment_value` por `order_purchase_timestamp`
- **Algoritmos**: Prophet (Meta/Facebook)
- **Resultado**: Pronóstico de ventas para planificación de inventario

### 4. Análisis Prescriptivo: ¿Qué debemos hacer?

#### Prescripción 1: Sistema de Alerta Temprana de Clientes Insatisfechos
- **Regla**: SI el Modelo 1 predice > 75% de probabilidad de reseña de 1 estrella, ENTONCES actuar proactivamente
- **Acciones Recomendadas**:
  - Ofrecer cupón de descuento preventivo
  - Priorizar la entrega en logística
  - Enviar email automático de seguimiento
  - Contacto proactivo del servicio al cliente

#### Prescripción 2: Gestión de Vendedores (Sellers)
- **Regla**: SI un `seller_id` tiene `review_score` promedio < 3.5 estrellas en los últimos 30 días, ENTONCES...
- **Acciones Recomendadas**:
  - Automático: Reducir ranking en resultados de búsqueda
  - Manual: Alerta al equipo de Seller Success
  - Capacitación obligatoria para el vendedor
  - Plan de mejora con seguimiento semanal

### 5. Análisis Cognitivo: IA sobre Datos No Estructurados

**Archivo**: `olist_order_reviews_dataset.csv`  
**Columnas**: `review_comment_message`, `review_comment_title`

#### Análisis 1: Análisis de Sentimiento
- **Responsable**: Leonardo
- **Acción**: Aplicar modelo de NLP pre-entrenado para portugués
- **Objetivo**: Clasificar comentarios como Positivo, Negativo o Neutro
- **Insight**: Validar coherencia entre `review_score` y sentimiento del comentario (detectar discrepancias)

#### Análisis 2: Topic Modeling (Modelado de Temas)
- **Acción**: Aplicar LDA o NMF sobre comentarios con `review_score = 1 o 2`
- **Objetivo**: Extraer temas principales de las quejas automáticamente
- **Tópicos esperados**:
  - Tópico 1: Problemas de logística (entrega, demora, prazo, atraso)
  - Tópico 2: Producto equivocado (errado, diferente, cor, foto)
  - Tópico 3: Producto dañado (quebrado, aberto, amassado)
  - Tópico 4: Mal servicio del vendedor (vendedor, contato, resposta)

## Tecnologías Utilizadas

- **Python**: Pandas, NumPy
- **PySpark**: Para procesamiento de big data
- **Prophet**: Forecasting de series de tiempo
- **Streamlit**: Dashboard interactivo
- **Scikit-learn**: Modelos de Machine Learning
- **NLP**: Análisis de sentimiento y topic modeling

## Estructura del Repositorio

```
ProyectoFinal-Analitica/
├── Data/                                    # Datasets CSV originales
├── Untitled.ipynb                           # Pipeline de preparación de datos
├── analisis_exploratorio_pyspark.ipynb      # Análisis exploratorio con PySpark
├── modelo_prediccion_demanda.ipynb          # Modelo de forecasting (Prophet)
├── app_streamlit.py                         # Dashboard interactivo
├── requirements.txt                         # Dependencias del proyecto
├── ANALISIS_RESULTADOS_MODELO.md            # Análisis detallado de resultados
└── README.md                                # Este archivo
```

## Resultados Esperados

1. **Comprensión profunda del negocio**: KPIs claros sobre ventas, clientes, productos y pagos
2. **Identificación de causas raíz**: Diagnóstico de factores que causan insatisfacción
3. **Capacidad predictiva**: Modelos que anticipen problemas y demanda futura
4. **Acciones concretas**: Prescripciones específicas para mejorar operaciones
5. **Insights de texto**: Comprensión de quejas mediante IA cognitiva

## Cómo Ejecutar el Proyecto

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar notebooks en orden:
   - `Untitled.ipynb` (preparación de datos)
   - `analisis_exploratorio_pyspark.ipynb` (EDA)
   - `modelo_prediccion_demanda.ipynb` (forecasting)

3. Lanzar dashboard:
```bash
streamlit run app_streamlit.py
```

## Contacto

Para consultas sobre este proyecto, contactar a cualquier miembro del Grupo 8.
