"""
Dashboard de Predicción de Demanda - Olist E-commerce
Modelo de Series de Tiempo con Prophet

Autor: [Tu Nombre]
Fecha: Diciembre 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from prophet import Prophet
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="Predicción de Demanda - Olist",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Funciones auxiliares
@st.cache_data
def load_data():
    """Cargar datos desde CSV o Parquet"""
    try:
        # Intentar cargar desde CSV de pronóstico si existe
        df_forecast = pd.read_csv('Data/pronostico_trimestral.csv')
        df_forecast['Fecha'] = pd.to_datetime(df_forecast['Fecha'])
        return df_forecast, True
    except:
        return None, False

@st.cache_data
def load_historical_data():
    """Cargar datos históricos"""
    try:
        # Aquí puedes cargar el archivo parquet o CSV con datos históricos
        import pyarrow.parquet as pq
        df = pq.read_table('Data/olist_unified_dataset.parquet').to_pandas()
        
        # Preparar datos de series de tiempo
        df_ts = df[['order_purchase_timestamp', 'payment_value']].copy()
        df_ts.columns = ['fecha', 'ventas']
        df_ts = df_ts.dropna()
        df_ts['fecha'] = pd.to_datetime(df_ts['fecha'])
        
        # Agregar por semana
        df_weekly = df_ts.set_index('fecha').resample('W')['ventas'].sum().reset_index()
        df_weekly.columns = ['ds', 'y']
        
        return df_weekly
    except Exception as e:
        st.error(f"Error cargando datos históricos: {e}")
        return None

@st.cache_resource
def train_prophet_model(df_train):
    """Entrenar modelo Prophet"""
    model = Prophet(
        seasonality_mode='multiplicative',
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=0.05,
        seasonality_prior_scale=10,
        interval_width=0.95
    )
    model.add_country_holidays(country_name='BR')
    model.fit(df_train)
    return model

def create_forecast_chart(df_historical, df_forecast):
    """Crear gráfico de pronóstico"""
    fig = go.Figure()
    
    # Datos históricos
    fig.add_trace(go.Scatter(
        x=df_historical['ds'],
        y=df_historical['y'],
        mode='lines',
        name='Histórico',
        line=dict(color='#1f77b4', width=2),
        hovertemplate='<b>Fecha:</b> %{x}<br><b>Ventas:</b> R$ %{y:,.2f}<extra></extra>'
    ))
    
    # Pronóstico
    fig.add_trace(go.Scatter(
        x=df_forecast['Fecha'],
        y=df_forecast['Predicción'],
        mode='lines+markers',
        name='Pronóstico',
        line=dict(color='#ff7f0e', width=3, dash='dash'),
        marker=dict(size=8, symbol='diamond'),
        hovertemplate='<b>Fecha:</b> %{x}<br><b>Pronóstico:</b> R$ %{y:,.2f}<extra></extra>'
    ))
    
    # Intervalo de confianza
    fig.add_trace(go.Scatter(
        x=df_forecast['Fecha'],
        y=df_forecast['Límite Superior (95%)'],
        mode='lines',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=df_forecast['Fecha'],
        y=df_forecast['Límite Inferior (95%)'],
        mode='lines',
        name='Intervalo Confianza 95%',
        fill='tonexty',
        fillcolor='rgba(255, 127, 14, 0.2)',
        line=dict(width=0),
        hovertemplate='<b>IC 95%:</b> R$ %{y:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': 'Pronóstico de Ventas - Próximo Trimestre',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#1f77b4'}
        },
        xaxis_title='Fecha',
        yaxis_title='Ventas Semanales (R$)',
        height=600,
        hovermode='x unified',
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.8)'),
        plot_bgcolor='white',
        xaxis=dict(gridcolor='lightgray'),
        yaxis=dict(gridcolor='lightgray')
    )
    
    return fig

def create_weekly_breakdown(df_forecast):
    """Crear gráfico de barras semanal"""
    df_forecast['Semana'] = df_forecast['Fecha'].dt.strftime('Sem %U')
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_forecast['Semana'],
        y=df_forecast['Predicción'],
        name='Predicción',
        marker_color='#2ca02c',
        hovertemplate='<b>%{x}</b><br>Ventas: R$ %{y:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Desglose Semanal del Pronóstico',
        xaxis_title='Semana',
        yaxis_title='Ventas (R$)',
        height=400,
        plot_bgcolor='white',
        xaxis=dict(gridcolor='lightgray'),
        yaxis=dict(gridcolor='lightgray')
    )
    
    return fig

# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================

# Header
st.markdown('<p class="main-header">📈 Predicción de Demanda - Olist E-commerce</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/graph.png", width=80)
    st.title("⚙️ Configuración")
    
    st.markdown("### 📊 Datos del Modelo")
    st.info("""
    **Modelo:** Prophet (Meta/Facebook)  
    **Periodo de entrenamiento:** Sep 2016 - Sep 2018  
    **Granularidad:** Semanal  
    **Horizonte:** 13 semanas (1 trimestre)
    """)
    
    st.markdown("### 🎯 Métricas del Modelo")
    
    # Opción para cargar métricas
    try:
        metrics_df = pd.read_csv('Data/metricas_modelo_demanda.csv')
        for _, row in metrics_df.iterrows():
            if 'R$' in row['Métrica']:
                st.metric(row['Métrica'], f"R$ {row['Valor']:,.2f}")
            elif '%' in row['Métrica']:
                st.metric(row['Métrica'], f"{row['Valor']:.2f}%")
            else:
                st.metric(row['Métrica'], f"{row['Valor']:.4f}")
    except:
        st.warning("Métricas no disponibles")
    
    st.markdown("---")
    st.markdown("### 📥 Opciones")
    
    if st.button("🔄 Reentrenar Modelo", use_container_width=True):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.success("Cache limpiado. Recarga la página.")

# Cargar datos
df_forecast, forecast_exists = load_data()
df_historical = load_historical_data()

if not forecast_exists or df_forecast is None:
    st.error("⚠️ No se encontraron datos de pronóstico. Ejecuta el notebook `modelo_prediccion_demanda.ipynb` primero.")
    st.stop()

# ============================================================================
# MÉTRICAS PRINCIPALES
# ============================================================================

st.markdown("## 📊 Resumen Ejecutivo")

col1, col2, col3, col4 = st.columns(4)

total_forecast = df_forecast['Predicción'].sum()
total_lower = df_forecast['Límite Inferior (95%)'].sum()
total_upper = df_forecast['Límite Superior (95%)'].sum()

# Calcular crecimiento (si hay datos históricos)
if df_historical is not None and len(df_historical) >= 13:
    last_13_weeks = df_historical.iloc[-13:]['y'].sum()
    growth = ((total_forecast - last_13_weeks) / last_13_weeks) * 100
else:
    growth = 0

with col1:
    st.metric(
        "💰 Ventas Proyectadas",
        f"R$ {total_forecast:,.0f}",
        f"{growth:+.1f}% vs trimestre anterior"
    )

with col2:
    st.metric(
        "📉 Escenario Pesimista",
        f"R$ {total_lower:,.0f}",
        "IC 95% inferior"
    )

with col3:
    st.metric(
        "📈 Escenario Optimista",
        f"R$ {total_upper:,.0f}",
        "IC 95% superior"
    )

with col4:
    weekly_avg = total_forecast / 13
    st.metric(
        "📅 Promedio Semanal",
        f"R$ {weekly_avg:,.0f}",
        "13 semanas"
    )

st.markdown("---")

# ============================================================================
# VISUALIZACIÓN PRINCIPAL
# ============================================================================

st.markdown("## 📈 Pronóstico Temporal")

tab1, tab2, tab3 = st.tabs(["📊 Vista General", "📅 Desglose Semanal", "📋 Tabla de Datos"])

with tab1:
    if df_historical is not None:
        fig_main = create_forecast_chart(df_historical, df_forecast)
        st.plotly_chart(fig_main, use_container_width=True)
    else:
        st.warning("No hay datos históricos disponibles para visualizar")

with tab2:
    fig_weekly = create_weekly_breakdown(df_forecast)
    st.plotly_chart(fig_weekly, use_container_width=True)
    
    # Estadísticas semanales
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📊 Estadísticas Semanales")
        st.dataframe(df_forecast[['Predicción']].describe(), use_container_width=True)
    
    with col2:
        st.markdown("### 🏆 Top 3 Semanas")
        top_weeks = df_forecast.nlargest(3, 'Predicción')[['Fecha', 'Predicción']]
        top_weeks['Fecha'] = top_weeks['Fecha'].dt.strftime('%d/%m/%Y')
        top_weeks['Predicción'] = top_weeks['Predicción'].apply(lambda x: f"R$ {x:,.2f}")
        st.dataframe(top_weeks, use_container_width=True, hide_index=True)

with tab3:
    st.markdown("### 📋 Datos Completos del Pronóstico")
    
    # Formatear tabla
    df_display = df_forecast.copy()
    df_display['Fecha'] = df_display['Fecha'].dt.strftime('%d/%m/%Y')
    df_display['Predicción'] = df_display['Predicción'].apply(lambda x: f"R$ {x:,.2f}")
    df_display['Límite Inferior (95%)'] = df_display['Límite Inferior (95%)'].apply(lambda x: f"R$ {x:,.2f}")
    df_display['Límite Superior (95%)'] = df_display['Límite Superior (95%)'].apply(lambda x: f"R$ {x:,.2f}")
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    # Botón de descarga
    csv = df_forecast.to_csv(index=False)
    st.download_button(
        label="📥 Descargar CSV",
        data=csv,
        file_name=f"pronostico_demanda_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

st.markdown("---")

# ============================================================================
# INSIGHTS Y RECOMENDACIONES
# ============================================================================

st.markdown("## 💡 Insights y Recomendaciones")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown("### 🎯 Planificación de Inventario")
    st.markdown(f"""
    - **Inventario semanal recomendado:** R$ {weekly_avg:,.0f}
    - **Buffer de seguridad:** R$ {(total_upper - total_forecast)/13:,.0f} adicional por semana
    - **Rango de variación:** R$ {(total_upper - total_lower):,.0f} en el trimestre
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown("### 📊 Análisis de Tendencia")
    
    if growth > 0:
        st.markdown(f"""
        ✅ **Tendencia positiva:** Crecimiento de **{growth:.1f}%** esperado
        - Incrementar stock en productos de alta rotación
        - Preparar campañas de marketing agresivas
        - Evaluar expansión de capacidad logística
        """)
    else:
        st.markdown(f"""
        ⚠️ **Tendencia negativa:** Decrecimiento de **{growth:.1f}%** esperado
        - Reducir inventario gradualmente
        - Implementar promociones para estimular demanda
        - Revisar estrategia de precios
        """)
    st.markdown('</div>', unsafe_allow_html=True)

# Insights adicionales
st.markdown("### 📈 Componentes del Modelo")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    **Tendencia**  
    Captura el patrón de crecimiento/decrecimiento a largo plazo de las ventas.
    """)

with col2:
    st.info("""
    **Estacionalidad Anual**  
    Identifica meses con mayor/menor demanda a lo largo del año.
    """)

with col3:
    st.info("""
    **Estacionalidad Semanal**  
    Detecta días de la semana con patrones de compra específicos.
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>📊 Dashboard creado con Streamlit | 🤖 Modelo: Prophet (Meta/Facebook)</p>
    <p>Proyecto Final - Análisis Predictivo de Datos | 2025</p>
</div>
""", unsafe_allow_html=True)
