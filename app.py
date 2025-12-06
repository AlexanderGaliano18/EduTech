import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- Configuración de la Página ---
st.set_page_config(
    page_title="EduTech ITSM | Gestión de Activos",
    page_icon="🛠️",
    layout="wide"
)

# --- 1. Inicialización de Datos (Memoria) ---
if 'df_activos' not in st.session_state:
    # Datos simulados iniciales
    laboratorios = ['Lab Cómputo 1', 'Lab Cómputo 2', 'Biblioteca', 'Admin']
    # Estados iniciales estándar
    estados = ['Operativo', 'Mantenimiento', 'Obsoleto', 'Baja']
    
    data = []
    for i in range(150): 
        data.append({
            'ID_Activo': f'PC-{1000+i}',
            'Ubicación': np.random.choice(laboratorios),
            'Estado': np.random.choice(estados, p=[0.7, 0.15, 0.1, 0.05]),
            'RAM': np.random.choice(['4GB', '8GB', '16GB']),
            'Antigüedad_Años': np.random.randint(1, 10)
        })
    st.session_state.df_activos = pd.DataFrame(data)

# Cargar dataframe de la sesión
df = st.session_state.df_activos

# --- 2. Barra Lateral: PANEL DE GESTIÓN (CRUD) ---
with st.sidebar:
    st.title("EduTech ITSM ⚙️")
    st.caption("Panel de Administración")
    
    tab1, tab2, tab3 = st.tabs(["➕ Registrar", "✏️ Editar", "🗑️ Borrar"])
    
    # Listas de opciones comunes
    opciones_ubicacion = ['Lab Cómputo 1', 'Lab Cómputo 2', 'Biblioteca', 'Admin', 'Almacén']
    opciones_estado = ['Operativo', 'Mantenimiento', 'Obsoleto', 'Baja', 'Repotenciada'] # ¡Nuevo Estado!
    opciones_ram = ['4GB', '8GB', '16GB', '32GB']

    # --- PESTAÑA 1: REGISTRAR (CREATE) ---
    with tab1:
        st.subheader("Nuevo Activo")
        next_id = int(df['ID_Activo'].str.split('-').str[1].max()) + 1 if not df.empty else 1000
        
        reg_id = st.text_input("ID", value=f"PC-{next_id}", key="reg_id")
        reg_ubic = st.selectbox("Ubicación", opciones_ubicacion, key="reg_ubi")
        reg_estado = st.selectbox("Estado", opciones_estado, key="reg_est")
        reg_ram = st.selectbox("RAM", opciones_ram, key="reg_ram")
        reg_ant = st.number_input("Años", min_value=0, value=0, key="reg_ant")
        
        if st.button("💾 Guardar Nuevo", type="primary"):
            if reg_id in df['ID_Activo'].values:
                st.error("¡Error! Ese ID ya existe.")
            else:
                nuevo_dato = {
                    'ID_Activo': reg_id, 'Ubicación': reg_ubic, 
                    'Estado': reg_estado, 'RAM': reg_ram, 
                    'Antigüedad_Años': reg_ant
                }
                st.session_state.df_activos = pd.concat([df, pd.DataFrame([nuevo_dato])], ignore_index=True)
                st.toast(f"Activo {reg_id} registrado exitosamente!", icon="✅")
                st.rerun()

    # --- PESTAÑA 2: EDITAR (UPDATE - MEJORADO) ---
    with tab2:
        st.subheader("Actualizar / Repotenciar")
        if not df.empty:
            edit_id = st.selectbox("Seleccionar ID", df['ID_Activo'].sort_values(), key="edit_select")
            
            # Obtener datos actuales para PRE-LLENAR los campos
            dato_actual = df[df['ID_Activo'] == edit_id].iloc[0]
            
            # Índices para los selectbox (para que muestren el valor actual por defecto)
            idx_ubic = opciones_ubicacion.index(dato_actual['Ubicación']) if dato_actual['Ubicación'] in opciones_ubicacion else 0
            idx_estado = opciones_estado.index(dato_actual['Estado']) if dato_actual['Estado'] in opciones_estado else 0
            idx_ram = opciones_ram.index(dato_actual['RAM']) if dato_actual['RAM'] in opciones_ram else 0
            
            # Formulario de edición con valores actuales
            new_ubic = st.selectbox("Ubicación", opciones_ubicacion, index=idx_ubic, key="edit_ubi")
            new_est = st.selectbox("Estado", opciones_estado, index=idx_estado, key="edit_est")
            
            col_edit1, col_edit2 = st.columns(2)
            with col_edit1:
                new_ram = st.selectbox("RAM (Actualizar)", opciones_ram, index=idx_ram, key="edit_ram")
            with col_edit2:
                new_ant = st.number_input("Antigüedad", min_value=0, value=int(dato_actual['Antigüedad_Años']), key="edit_ant")
            
            if st.button("🔄 Actualizar Datos", type="primary"):
                # Actualizamos en el DataFrame
                idx = df.index[df['ID_Activo'] == edit_id].tolist()[0]
                st.session_state.df_activos.at[idx, 'Ubicación'] = new_ubic
                st.session_state.df_activos.at[idx, 'Estado'] = new_est
                st.session_state.df_activos.at[idx, 'RAM'] = new_ram
                st.session_state.df_activos.at[idx, 'Antigüedad_Años'] = new_ant
                
                st.toast(f"{edit_id} actualizado correctamente.", icon="🚀")
                st.rerun()
        else:
            st.warning("No hay activos para editar.")

    # --- PESTAÑA 3: BORRAR (DELETE) ---
    with tab3:
        st.subheader("Dar de Baja")
        if not df.empty:
            del_id = st.selectbox("Seleccionar ID a eliminar", df['ID_Activo'].sort_values(), key="del_select")
            
            st.warning(f"¿Seguro que deseas eliminar {del_id}?")
            if st.button("❌ Eliminar Definitivamente"):
                st.session_state.df_activos = df[df['ID_Activo'] != del_id]
                st.toast(f"Activo {del_id} eliminado.", icon="🗑️")
                st.rerun()
        else:
            st.info("Inventario vacío.")

    st.markdown("---")
    filtro_lab = st.multiselect("Filtro de Visualización:", options=df['Ubicación'].unique(), default=df['Ubicación'].unique())

# --- 3. Panel Principal (DASHBOARD) ---

# Aplicar filtros
if filtro_lab:
    df_filtered = st.session_state.df_activos[st.session_state.df_activos['Ubicación'].isin(filtro_lab)]
else:
    df_filtered = st.session_state.df_activos

st.title("📊 Dashboard de Control de Activos")
st.markdown(f"Vista general del inventario ({len(df_filtered)} equipos visibles).")

# KPIs Actualizados
c1, c2, c3, c4 = st.columns(4)
total = len(df_filtered)
operativos = len(df_filtered[df_filtered['Estado'] == 'Operativo'])
# Contamos también las repotenciadas como algo positivo
repotenciadas = len(df_filtered[df_filtered['Estado'] == 'Repotenciada'])
bajas = len(df_filtered[df_filtered['Estado'] == 'Baja'])

c1.metric("Total Activos", total)
c2.metric("Operativos", operativos)
c3.metric("✨ Repotenciadas", repotenciadas, delta="Upgrade reciente")
c4.metric("Baja / Descarte", bajas, delta_color="inverse")

st.divider()

# Gráficos
col_graph1, col_graph2 = st.columns(2)

with col_graph1:
    st.subheader("Estado de Conservación")
    if not df_filtered.empty:
        # Usamos gráfico de barras horizontal para que se lean bien las etiquetas
        st.bar_chart(df_filtered['Estado'].value_counts())
    else:
        st.info("No hay datos.")

with col_graph2:
    st.subheader("Distribución de Memoria RAM")
    if not df_filtered.empty:
        st.bar_chart(df_filtered['RAM'].value_counts())

# Tabla General
st.markdown("### 📋 Inventario Detallado")
st.dataframe(
    df_filtered[['ID_Activo', 'Ubicación', 'Estado', 'RAM', 'Antigüedad_Años']], 
    use_container_width=True, 
    hide_index=True
)

# --- Footer ---
st.markdown("---")
st.caption("Sistema EduTech ITSM v4.0 | Desarrollado por Alexander Galiano")
