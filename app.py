import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- Configuración de la Página ---
st.set_page_config(
    page_title="EduTech ITSM | Gestión & Analítica",
    page_icon="🎓",
    layout="wide"
)

# --- 1. Inicialización de Datos (Persistencia) ---
if 'df_activos' not in st.session_state:
    laboratorios = ['Lab Cómputo 1', 'Lab Cómputo 2', 'Biblioteca', 'Admin']
    estados = ['Operativo', 'Mantenimiento', 'Obsoleto', 'Baja', 'Repotenciada']
    
    data = []
    for i in range(150): 
        data.append({
            'ID_Activo': f'PC-{1000+i}',
            'Ubicación': np.random.choice(laboratorios),
            'Estado': np.random.choice(estados, p=[0.6, 0.1, 0.1, 0.05, 0.15]),
            'RAM': np.random.choice(['4GB', '8GB', '16GB']),
            'Antigüedad_Años': np.random.randint(1, 12)
        })
    st.session_state.df_activos = pd.DataFrame(data)

if 'df_tickets' not in st.session_state:
    laboratorios = ['Lab Cómputo 1', 'Lab Cómputo 2', 'Biblioteca', 'Admin']
    categorias = ['Hardware', 'Software', 'Red', 'Periféricos']
    data_tickets = []
    for i in range(500):
        duracion = np.random.randint(1, 48)
        prioridad = np.random.choice(['Alta', 'Media', 'Baja'])
        # Algoritmo SLA: Si es Alta y dura > 24h, rompe el SLA
        cumple = not (prioridad == 'Alta' and duracion > 24)
        
        data_tickets.append({
            'Ticket_ID': f'TCK-{5000+i}',
            'Categoría': np.random.choice(categorias),
            'Tiempo_Resolución_Hrs': duracion,
            'Cumple_SLA': cumple,
            'Ubicación': np.random.choice(laboratorios)
        })
    st.session_state.df_tickets = pd.DataFrame(data_tickets)

# Cargar DataFrames
df_activos = st.session_state.df_activos
df_tickets = st.session_state.df_tickets

# --- 2. Barra Lateral: GESTIÓN CRUD COMPLETA ---
with st.sidebar:
    st.title("EduTech ITSM ⚙️")
    st.caption("Panel de Administración")
    
    # ¡Aquí recuperamos las 3 pestañas!
    tab1, tab2, tab3 = st.tabs(["➕ Alta", "✏️ Modificar", "🗑️ Baja"])
    
    opciones_ubic = ['Lab Cómputo 1', 'Lab Cómputo 2', 'Biblioteca', 'Admin']
    opciones_estado = ['Operativo', 'Mantenimiento', 'Obsoleto', 'Baja', 'Repotenciada']
    opciones_ram = ['4GB', '8GB', '16GB', '32GB']
    
    # --- PESTAÑA 1: REGISTRAR (Alta) ---
    with tab1: 
        next_id = int(df_activos['ID_Activo'].str.split('-').str[1].max()) + 1 if not df_activos.empty else 1000
        reg_id = st.text_input("Nuevo ID", value=f"PC-{next_id}", key="reg_id")
        reg_ubi = st.selectbox("Ubicación", opciones_ubic, key="r_u")
        reg_est = st.selectbox("Estado", opciones_estado, key="r_e")
        reg_ram = st.selectbox("RAM", opciones_ram, key="r_r")
        reg_ant = st.number_input("Años", 0, 20, 0, key="r_a")
        
        if st.button("💾 Registrar Activo", type="primary"):
            if reg_id in df_activos['ID_Activo'].values:
                st.error("ID duplicado.")
            else:
                nuevo = {'ID_Activo': reg_id, 'Ubicación': reg_ubi, 'Estado': reg_est, 'RAM': reg_ram, 'Antigüedad_Años': reg_ant}
                st.session_state.df_activos = pd.concat([df_activos, pd.DataFrame([nuevo])], ignore_index=True)
                st.toast("Registrado correctamente", icon="✅")
                st.rerun()

    # --- PESTAÑA 2: EDITAR (Modificar) ---
    with tab2: 
        if not df_activos.empty:
            edit_id = st.selectbox("Buscar ID", df_activos['ID_Activo'].sort_values(), key="e_id")
            # Pre-llenado de datos actuales
            dato = df_activos[df_activos['ID_Activo'] == edit_id].iloc[0]
            
            # Índices seguros
            idx_u = opciones_ubic.index(dato['Ubicación']) if dato['Ubicación'] in opciones_ubic else 0
            idx_e = opciones_estado.index(dato['Estado']) if dato['Estado'] in opciones_estado else 0
            idx_r = opciones_ram.index(dato['RAM']) if dato['RAM'] in opciones_ram else 0
            
            n_ubi = st.selectbox("Ubicación", opciones_ubic, index=idx_u, key="e_u")
            n_est = st.selectbox("Estado", opciones_estado, index=idx_e, key="e_e")
            n_ram = st.selectbox("RAM", opciones_ram, index=idx_r, key="e_r")
            n_ant = st.number_input("Años", 0, 20, int(dato['Antigüedad_Años']), key="e_a")
            
            if st.button("🔄 Actualizar"):
                idx = df_activos.index[df_activos['ID_Activo'] == edit_id][0]
                st.session_state.df_activos.at[idx, 'Ubicación'] = n_ubi
                st.session_state.df_activos.at[idx, 'Estado'] = n_est
                st.session_state.df_activos.at[idx, 'RAM'] = n_ram
                st.session_state.df_activos.at[idx, 'Antigüedad_Años'] = n_ant
                st.toast("Actualizado", icon="🔄")
                st.rerun()

    # --- PESTAÑA 3: BORRAR (Baja) - ¡RECUPERADA! ---
    with tab3:
        if not df_activos.empty:
            del_id = st.selectbox("ID a Eliminar", df_activos['ID_Activo'].sort_values(), key="d_id")
            st.warning(f"¿Eliminar {del_id}?")
            if st.button("❌ Confirmar Baja"):
                st.session_state.df_activos = df_activos[df_activos['ID_Activo'] != del_id]
                st.toast("Eliminado", icon="🗑️")
                st.rerun()

    st.markdown("---")
    st.header("Filtros")
    filtro = st.multiselect("Filtrar por Sala:", df_activos['Ubicación'].unique())
    
    # Botón Descarga
    csv = df_activos.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Bajar CSV", csv, "reporte.csv", "text/csv")

# --- 3. DASHBOARD DE ANALÍTICA (Documento) ---

# Aplicar filtros
df_a = st.session_state.df_activos
df_t = df_tickets
if filtro:
    df_a = df_a[df_a['Ubicación'].isin(filtro)]
    df_t = df_t[df_t['Ubicación'].isin(filtro)]

st.title("📊 Analítica de Gestión de Activos TI")

# --- ALGORITMOS DE CÁLCULO (Documento) ---
# 1. Tasa de Obsolescencia
total_activos = len(df_a)
obsoletos = len(df_a[(df_a['Antigüedad_Años'] > 7) | (df_a['Estado'] == 'Obsoleto')])
tasa_obs = (obsoletos / total_activos * 100) if total_activos > 0 else 0

# 2. Cumplimiento SLA
total_tickets = len(df_t)
cumplen = len(df_t[df_t['Cumple_SLA']])
tasa_sla = (cumplen / total_tickets * 100) if total_tickets > 0 else 0

# 3. Frecuencia de Fallas (MTTR)
mttr = df_t['Tiempo_Resolución_Hrs'].mean()

# Mostrar KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Cumplimiento SLA", f"{tasa_sla:.1f}%", delta="Meta: >90%")
c2.metric("Tasa Obsolescencia", f"{tasa_obs:.1f}%", delta_color="inverse")
c3.metric("Tiempo Medio (MTTR)", f"{mttr:.1f} Hrs", delta_color="inverse")
c4.metric("Total Activos", total_activos)

st.divider()

# --- GRÁFICOS SOLICITADOS ---
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("📍 Frecuencia de Fallas por Laboratorio")
    # Conteo de tickets por ubicación
    fallas_lab = df_t['Ubicación'].value_counts()
    st.bar_chart(fallas_lab)
    st.caption("Ubicaciones con mayor incidencia de soporte.")

with col_g2:
    st.subheader("💾 Ciclo de Vida del Hardware")
    # Estado de los equipos
    st.bar_chart(df_a['Estado'].value_counts())
    st.caption("Distribución operativa de los equipos.")

# --- LISTADO CRÍTICO (Para toma de decisiones) ---
st.subheader("⚠️ Equipos Críticos (Obsolescencia Detectada)")
if not df_a.empty and obsoletos > 0:
    criticos = df_a[(df_a['Antigüedad_Años'] > 7) | (df_a['Estado'] == 'Obsoleto')]
    st.dataframe(criticos, use_container_width=True)
else:
    st.success("Excelente: No hay equipos críticos en la selección actual.")

# Footer
st.markdown("---")
st.caption("EduTech ITSM v6.0 | Módulo de Gestión Integral y Analítica")
