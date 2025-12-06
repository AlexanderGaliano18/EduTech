import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# --- Configuración de la Página ---
st.set_page_config(
    page_title="EduTech ITSM | Dashboard Gerencial",
    page_icon="🖥️",
    layout="wide"
)

# --- 1. Inicialización del Estado (Session State) ---
# Esto permite que los datos persistan y se puedan editar en la demo
if 'df_activos' not in st.session_state:
    # --- Simulación Inicial de Datos ---
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
    st.session_state.df_activos = pd.DataFrame(data_activos)

if 'df_tickets' not in st.session_state:
    # --- Simulación Inicial de Tickets ---
    laboratorios = ['Lab Cómputo 1', 'Lab Cómputo 2', 'Biblioteca', 'Admin']
    categorias = ['Hardware (Falla PC)', 'Software (Office/Windows)', 'Red/Internet', 'Periféricos']
    data_tickets = []
    for i in range(500):
        fecha_creacion = datetime.now() - timedelta(days=np.random.randint(0, 60))
        duracion_resolucion = np.random.randint(1, 48)
        prioridad = np.random.choice(['Alta', 'Media', 'Baja'])
        cumple_sla = not (prioridad == 'Alta' and duracion_resolucion > 24)
            
        data_tickets.append({
            'Ticket_ID': f'TCK-{5000+i}',
            'Fecha': fecha_creacion,
            'Categoría': np.random.choice(categorias),
            'Prioridad': prioridad,
            'Tiempo_Resolución_Hrs': duracion_resolucion,
            'Cumple_SLA': cumple_sla,
            'Ubicación': np.random.choice(laboratorios)
        })
    st.session_state.df_tickets = pd.DataFrame(data_tickets)

# Recuperar datos del estado
df_activos = st.session_state.df_activos
df_tickets = st.session_state.df_tickets

# --- 2. Barra Lateral (Sidebar) ---
with st.sidebar:
    st.title("EduTech ITSM ⚙️")
    st.markdown("**Gestión & Analítica**")
    st.markdown("---")
    
    # --- MÓDULO DE GESTIÓN (NUEVO) ---
    with st.expander("🛠️ Gestión de Activos (CRUD)", expanded=True):
        st.write("**Registrar / Actualizar Equipo**")
        
        # Formulario para agregar/editar
        nuevo_id = st.text_input("ID del Activo", value=f"PC-{len(df_activos)+1000}")
        nueva_ubicacion = st.selectbox("Ubicación", options=df_activos['Ubicación'].unique())
        nuevo_estado = st.selectbox("Estado Actual", options=['Operativo', 'Mantenimiento', 'Obsoleto', 'Baja'])
        nueva_ram = st.selectbox("Memoria RAM", options=['4GB', '8GB', '16GB', '32GB'])
        nueva_antiguedad = st.slider("Antigüedad (Años)", 0, 15, 1)
        
        if st.button("💾 Guardar Cambios", type="primary"):
            # Verificar si existe para actualizar, sino agregar
            if nuevo_id in df_activos['ID_Activo'].values:
                # Actualizar (Lógica simplificada: borramos y creamos de nuevo para la demo)
                idx = df_activos.index[df_activos['ID_Activo'] == nuevo_id].tolist()[0]
                st.session_state.df_activos.at[idx, 'Ubicación'] = nueva_ubicacion
                st.session_state.df_activos.at[idx, 'Estado'] = nuevo_estado
                st.session_state.df_activos.at[idx, 'RAM'] = nueva_ram
                st.session_state.df_activos.at[idx, 'Antigüedad_Años'] = nueva_antiguedad
                st.success(f"¡{nuevo_id} actualizado!")
            else:
                # Crear nuevo registro
                nuevo_dato = {
                    'ID_Activo': nuevo_id,
                    'Ubicación': nueva_ubicacion,
                    'Estado': nuevo_estado,
                    'RAM': nueva_ram,
                    'Antigüedad_Años': nueva_antiguedad
                }
                st.session_state.df_activos = pd.concat([df_activos, pd.DataFrame([nuevo_dato])], ignore_index=True)
                st.success(f"¡{nuevo_id} agregado al inventario!")
            
            # Recargar página para actualizar gráficos
            st.rerun()
    
    st.markdown("---")
    
    st.header("Filtros de Visualización")
    filtro_lab = st.multiselect(
        "Filtrar Dashboard por:",
        options=df_activos['Ubicación'].unique(),
        default=df_activos['Ubicación'].unique()
    )
    
    # Botón de descarga
    csv = df_activos.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar Reporte (CSV)", csv, "inventario.csv", "text/csv")

# Filtrar DataFrames para visualización
if filtro_lab:
    df_activos_filt = st.session_state.df_activos[st.session_state.df_activos['Ubicación'].isin(filtro_lab)]
    df_tickets_filt = df_tickets[df_tickets['Ubicación'].isin(filtro_lab)]
else:
    df_activos_filt = st.session_state.df_activos
    df_tickets_filt = df_tickets

# --- 3. Panel Principal ---

st.title("📊 Monitor de Infraestructura Tecnológica Escolar")
st.markdown("Plataforma integral para la gestión del ciclo de vida de activos TI y soporte técnico.")

# --- KPIs Dinámicos ---
col1, col2, col3, col4 = st.columns(4)

total_activos = len(df_activos_filt)
equipos_operativos = len(df_activos_filt[df_activos_filt['Estado'] == 'Operativo'])
tasa_operatividad = (equipos_operativos / total_activos) * 100 if total_activos > 0 else 0
tickets_totales = len(df_tickets_filt)
mttr = df_tickets_filt['Tiempo_Resolución_Hrs'].mean()

with col1:
    st.metric("Total Activos TI", total_activos, delta="En tiempo real")
with col2:
    st.metric("Operatividad", f"{tasa_operatividad:.1f}%", delta="Meta: 95%")
with col3:
    st.metric("Tickets Abiertos", tickets_totales)
with col4:
    st.metric("Tiempo Medio (MTTR)", f"{mttr:.1f} Hrs", delta_color="inverse")

st.divider()

# --- Gráficos Nativos (Actualizables) ---
col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("Estado del Parque Informático")
    estado_counts = df_activos_filt['Estado'].value_counts()
    st.bar_chart(estado_counts)
    st.caption("Si cambias el estado de un equipo en el menú lateral, este gráfico cambiará.")

with col_der:
    st.subheader("Incidencias por Categoría")
    cat_counts = df_tickets_filt['Categoría'].value_counts()
    st.bar_chart(cat_counts)

# --- Tabla Detallada (Verificación de Cambios) ---
st.subheader("📋 Detalle de Inventario")
st.dataframe(
    df_activos_filt[['ID_Activo', 'Ubicación', 'Estado', 'RAM', 'Antigüedad_Años']],
    use_container_width=True,
    hide_index=True
)

# --- Alerta de Obsolescencia ---
st.subheader("⚠️ Auditoría de Obsolescencia")
equipos_viejos = df_activos_filt[
    (df_activos_filt['Antigüedad_Años'] > 7) | (df_activos_filt['Estado'] == 'Obsoleto')
]

if not equipos_viejos.empty:
    st.warning(f"Se han detectado {len(equipos_viejos)} equipos que requieren renovación urgente.")
else:
    st.success("Todos los equipos se encuentran dentro del ciclo de vida útil.")

# --- Footer ---
st.markdown("---")
st.markdown("© 2025 **Alexander Galiano** | Proyecto Software Libre")
