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

# --- 1. Inicialización del Estado (Memoria para Editar) ---
if 'df_activos' not in st.session_state:
    # Datos iniciales simulados
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
    # Tickets simulados
    laboratorios = ['Lab Cómputo 1', 'Lab Cómputo 2', 'Biblioteca', 'Admin']
    categorias = ['Hardware (Falla PC)', 'Software (Office/Windows)', 'Red/Internet', 'Periféricos']
    data_tickets = []
    for i in range(500):
        fecha_creacion = datetime.now() - timedelta(days=np.random.randint(0, 60))
        duracion = np.random.randint(1, 48)
        prioridad = np.random.choice(['Alta', 'Media', 'Baja'])
        cumple = not (prioridad == 'Alta' and duracion > 24)
        data_tickets.append({
            'Ticket_ID': f'TCK-{5000+i}',
            'Categoría': np.random.choice(categorias),
            'Tiempo_Resolución_Hrs': duracion,
            'Cumple_SLA': cumple,
            'Ubicación': np.random.choice(laboratorios)
        })
    st.session_state.df_tickets = pd.DataFrame(data_tickets)

# Cargar datos de la memoria
df_activos = st.session_state.df_activos
df_tickets = st.session_state.df_tickets

# --- 2. Barra Lateral: GESTIÓN DE ACTIVOS ---
with st.sidebar:
    st.title("EduTech ITSM ⚙️")
    st.markdown("---")
    
    # --- MÓDULO CRUD (Lo que pediste) ---
    with st.expander("🛠️ Gestión de Activos (Editar)", expanded=True):
        st.write("**Registrar / Actualizar Equipo**")
        
        nuevo_id = st.text_input("ID del Activo", value=f"PC-{len(df_activos)+1000}")
        nueva_ubicacion = st.selectbox("Ubicación", options=df_activos['Ubicación'].unique())
        nuevo_estado = st.selectbox("Estado", options=['Operativo', 'Mantenimiento', 'Obsoleto', 'Baja'])
        nueva_ram = st.selectbox("RAM", options=['4GB', '8GB', '16GB', '32GB'])
        nueva_antiguedad = st.slider("Años de uso", 0, 15, 1)
        
        if st.button("💾 Guardar Cambios", type="primary"):
            # Lógica de actualización
            if nuevo_id in df_activos['ID_Activo'].values:
                idx = df_activos.index[df_activos['ID_Activo'] == nuevo_id].tolist()[0]
                st.session_state.df_activos.at[idx, 'Ubicación'] = nueva_ubicacion
                st.session_state.df_activos.at[idx, 'Estado'] = nuevo_estado
                st.session_state.df_activos.at[idx, 'RAM'] = nueva_ram
                st.session_state.df_activos.at[idx, 'Antigüedad_Años'] = nueva_antiguedad
                st.success(f"¡{nuevo_id} actualizado!")
            else:
                nuevo_dato = {'ID_Activo': nuevo_id, 'Ubicación': nueva_ubicacion, 'Estado': nuevo_estado, 'RAM': nueva_ram, 'Antigüedad_Años': nueva_antiguedad}
                st.session_state.df_activos = pd.concat([df_activos, pd.DataFrame([nuevo_dato])], ignore_index=True)
                st.success(f"¡{nuevo_id} agregado!")
            st.rerun()

    st.markdown("---")
    st.header("Filtros")
    filtro_lab = st.multiselect("Filtrar Ubicación:", options=df_activos['Ubicación'].unique(), default=df_activos['Ubicación'].unique())
    
    # Botón de Descarga
    csv = df_activos.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar CSV", csv, "inventario.csv", "text/csv")

# Aplicar Filtros
if filtro_lab:
    df_activos_filt = df_activos[df_activos['Ubicación'].isin(filtro_lab)]
    df_tickets_filt = df_tickets[df_tickets['Ubicación'].isin(filtro_lab)]
else:
    df_activos_filt = df_activos
    df_tickets_filt = df_tickets

# --- 3. Panel Principal (Gráficos NATIVOS - Sin Plotly) ---
st.title("📊 Monitor de Infraestructura Tecnológica")

# KPIs
col1, col2, col3, col4 = st.columns(4)
total = len(df_activos_filt)
operativos = len(df_activos_filt[df_activos_filt['Estado'] == 'Operativo'])
tasa = (operativos / total * 100) if total > 0 else 0
tickets = len(df_tickets_filt)
mttr = df_tickets_filt['Tiempo_Resolución_Hrs'].mean()

col1.metric("Total Activos", total)
col2.metric("Operatividad", f"{tasa:.1f}%")
col3.metric("Tickets Totales", tickets)
col4.metric("Tiempo Medio (MTTR)", f"{mttr:.1f} Hrs")

st.divider()

# Gráficos de Barras Simples (No fallan nunca)
c1, c2 = st.columns(2)
with c1:
    st.subheader("Estado de Equipos")
    st.bar_chart(df_activos_filt['Estado'].value_counts()) # Gráfico nativo

with c2:
    st.subheader("Fallas por Categoría")
    st.bar_chart(df_tickets_filt['Categoría'].value_counts()) # Gráfico nativo

# Tabla de Obsolescencia
st.subheader("⚠️ Equipos Críticos (> 7 años u Obsoletos)")
viejos = df_activos_filt[(df_activos_filt['Antigüedad_Años'] > 7) | (df_activos_filt['Estado'] == 'Obsoleto')]
if not viejos.empty:
    st.warning(f"{len(viejos)} equipos requieren atención.")
    st.dataframe(viejos, use_container_width=True)
else:
    st.success("Todo en orden.")
