import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- Configuración de la Página ---
st.set_page_config(
    page_title="EduTech ITSM | Dashboard Gerencial",
    page_icon="🖥️",
    layout="wide"
)

# --- 1. Simulación de Datos (Backend Mockup) ---
@st.cache_data
def get_glpi_data():
    """Genera datos simulados de activos y tickets."""
    # --- Datos de Inventario (Activos) ---
    laboratorios = ['Lab Cómputo 1', 'Lab Cómputo 2', 'Biblioteca', 'Admin']
    estados = ['Operativo', 'Mantenimiento', 'Obsoleto', 'Baja']
    
    data_activos = []
    for i in range(150): 
        lab = np.random.choice(laboratorios)
        estado = np.random.choice(estados, p=[0.7, 0.15, 0.1, 0.05])
        ram = np.random.choice(['4GB', '8GB', '16GB'])
        data_activos.append({
            'ID_Activo': f'PC-{1000+i}',
            'Ubicación': lab,
            'Estado': estado,
            'RAM': ram,
            'Antigüedad_Años': np.random.randint(1, 10)
        })
    df_activos = pd.DataFrame(data_activos)

    # --- Datos de Tickets (Incidencias) ---
    categorias = ['Hardware (Falla PC)', 'Software (Office/Windows)', 'Red/Internet', 'Periféricos']
    data_tickets = []
    for i in range(500):
        fecha_creacion = datetime.now() - timedelta(days=np.random.randint(0, 60))
        duracion_resolucion = np.random.randint(1, 48) # Horas
        prioridad = np.random.choice(['Alta', 'Media', 'Baja'])
        
        cumple_sla = True
        if prioridad == 'Alta' and duracion_resolucion > 24:
            cumple_sla = False
            
        data_tickets.append({
            'Ticket_ID': f'TCK-{5000+i}',
            'Fecha': fecha_creacion,
            'Categoría': np.random.choice(categorias),
            'Prioridad': prioridad,
            'Tiempo_Resolución_Hrs': duracion_resolucion,
            'Cumple_SLA': cumple_sla,
            'Ubicación': np.random.choice(laboratorios)
        })
    df_tickets = pd.DataFrame(data_tickets)
    
    return df_activos, df_tickets

# Cargar datos
df_activos, df_tickets = get_glpi_data()

# --- 2. Barra Lateral ---
with st.sidebar:
    st.title("EduTech ITSM ⚙️")
    st.markdown("**Módulo de Analítica** integrado con GLPI.")
    st.markdown("---")
    
    st.header("Filtros Globales")
    filtro_lab = st.multiselect(
        "Seleccionar Ubicación:",
        options=df_activos['Ubicación'].unique(),
        default=df_activos['Ubicación'].unique()
    )
    st.info("Estado: 🟢 Online (Versión Lite)")

# Filtrar DataFrames
if filtro_lab:
    df_activos_filt = df_activos[df_activos['Ubicación'].isin(filtro_lab)]
    df_tickets_filt = df_tickets[df_tickets['Ubicación'].isin(filtro_lab)]
else:
    df_activos_filt = df_activos
    df_tickets_filt = df_tickets

# --- 3. Panel Principal ---
st.title("📊 Monitor de Infraestructura Tecnológica Escolar")
st.markdown("Indicadores clave de rendimiento (KPIs) para la gestión de activos TI.")

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)

total_activos = len(df_activos_filt)
equipos_operativos = len(df_activos_filt[df_activos_filt['Estado'] == 'Operativo'])
tasa_operatividad = (equipos_operativos / total_activos) * 100 if total_activos > 0 else 0
tickets_totales = len(df_tickets_filt)
sla_cumplimiento = (len(df_tickets_filt[df_tickets_filt['Cumple_SLA']]) / tickets_totales) * 100 if tickets_totales > 0 else 0
mttr = df_tickets_filt['Tiempo_Resolución_Hrs'].mean()

col1.metric("Total Activos TI", total_activos)
col2.metric("Operatividad Equipos", f"{tasa_operatividad:.1f}%")
col3.metric("Cumplimiento SLA", f"{sla_cumplimiento:.1f}%")
col4.metric("Tiempo Medio (MTTR)", f"{mttr:.1f} Hrs")

st.divider()

# --- Gráficos Nativos (Sin Plotly) ---
col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("Estado del Parque Informático")
    # Preparamos datos para gráfico de barras simple
    estado_counts = df_activos_filt['Estado'].value_counts()
    st.bar_chart(estado_counts)
    st.caption("Cantidad de equipos por estado.")

with col_der:
    st.subheader("Incidencias por Categoría")
    cat_counts = df_tickets_filt['Categoría'].value_counts()
    st.bar_chart(cat_counts)
    st.caption("Tickets reportados por tipo de problema.")

# --- Alerta de Obsolescencia ---
st.subheader("⚠️ Alerta de Obsolescencia Tecnológica")
equipos_viejos = df_activos_filt[
    (df_activos_filt['Antigüedad_Años'] > 7) | (df_activos_filt['Estado'] == 'Obsoleto')
]

if not equipos_viejos.empty:
    st.warning(f"Se han detectado {len(equipos_viejos)} equipos que requieren renovación urgente.")
    st.dataframe(equipos_viejos[['ID_Activo', 'Ubicación', 'RAM', 'Antigüedad_Años', 'Estado']], use_container_width=True)
else:
    st.success("Todos los equipos se encuentran dentro del ciclo de vida útil.")

# --- Footer ---
st.markdown("---")
st.markdown("© 2025 **Alexander Galiano** | Proyecto Software Libre")
