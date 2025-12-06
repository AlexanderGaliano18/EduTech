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
    
    # Usamos Tabs para separar las acciones claramente
    tab1, tab2, tab3 = st.tabs(["➕ Registrar", "✏️ Editar", "🗑️ Borrar"])
    
    # --- PESTAÑA 1: REGISTRAR (CREATE) ---
    with tab1:
        st.subheader("Nuevo Activo")
        # Generar ID automático sugerido
        next_id = int(df['ID_Activo'].str.split('-').str[1].max()) + 1 if not df.empty else 1000
        
        reg_id = st.text_input("ID", value=f"PC-{next_id}", key="reg_id")
        reg_ubic = st.selectbox("Ubicación", ['Lab Cómputo 1', 'Lab Cómputo 2', 'Biblioteca', 'Admin', 'Almacén'], key="reg_ubi")
        reg_estado = st.selectbox("Estado", ['Operativo', 'Mantenimiento', 'Obsoleto', 'Baja'], key="reg_est")
        reg_ram = st.selectbox("RAM", ['4GB', '8GB', '16GB', '32GB'], key="reg_ram")
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
                # Agregar al DataFrame
                st.session_state.df_activos = pd.concat([df, pd.DataFrame([nuevo_dato])], ignore_index=True)
                st.toast(f"Activo {reg_id} registrado exitosamente!", icon="✅")
                st.rerun()

    # --- PESTAÑA 2: EDITAR (UPDATE) ---
    with tab2:
        st.subheader("Actualizar Equipo")
        if not df.empty:
            edit_id = st.selectbox("Seleccionar ID", df['ID_Activo'].sort_values(), key="edit_select")
            
            # Obtener datos actuales para pre-llenar
            dato_actual = df[df['ID_Activo'] == edit_id].iloc[0]
            
            # Formulario de edición
            new_ubic = st.selectbox("Nueva Ubicación", ['Lab Cómputo 1', 'Lab Cómputo 2', 'Biblioteca', 'Admin', 'Almacén'], index=['Lab Cómputo 1', 'Lab Cómputo 2', 'Biblioteca', 'Admin', 'Almacén'].index(dato_actual['Ubicación']), key="edit_ubi")
            new_est = st.selectbox("Nuevo Estado", ['Operativo', 'Mantenimiento', 'Obsoleto', 'Baja'], index=['Operativo', 'Mantenimiento', 'Obsoleto', 'Baja'].index(dato_actual['Estado']), key="edit_est")
            
            if st.button("🔄 Actualizar Datos"):
                idx = df.index[df['ID_Activo'] == edit_id].tolist()[0]
                st.session_state.df_activos.at[idx, 'Ubicación'] = new_ubic
                st.session_state.df_activos.at[idx, 'Estado'] = new_est
                st.toast(f"{edit_id} actualizado correctamente.", icon="🔄")
                st.rerun()
        else:
            st.warning("No hay activos para editar.")

    # --- PESTAÑA 3: BORRAR (DELETE) ---
    with tab3:
        st.subheader("Dar de Baja")
        if not df.empty:
            del_id = st.selectbox("Seleccionar ID a eliminar", df['ID_Activo'].sort_values(), key="del_select")
            
            st.warning(f"¿Seguro que deseas eliminar {del_id}?")
            if st.button("❌ Eliminar Definitivamente", type="primary"):
                # Filtrar y guardar todo MENOS el eliminado
                st.session_state.df_activos = df[df['ID_Activo'] != del_id]
                st.toast(f"Activo {del_id} eliminado.", icon="🗑️")
                st.rerun()
        else:
            st.info("Inventario vacío.")

    st.markdown("---")
    # Filtros para el Dashboard
    filtro_lab = st.multiselect("Filtro de Visualización:", options=df['Ubicación'].unique(), default=df['Ubicación'].unique())

# --- 3. Panel Principal (DASHBOARD) ---

# Aplicar filtros
if filtro_lab:
    df_filtered = st.session_state.df_activos[st.session_state.df_activos['Ubicación'].isin(filtro_lab)]
else:
    df_filtered = st.session_state.df_activos

st.title("📊 Dashboard de Control de Activos")
st.markdown(f"Vista general del inventario ({len(df_filtered)} equipos visibles).")

# KPIs
c1, c2, c3 = st.columns(3)
total = len(df_filtered)
operativos = len(df_filtered[df_filtered['Estado'] == 'Operativo'])
obsoletos = len(df_filtered[df_filtered['Estado'] == 'Obsoleto'])

c1.metric("Total Activos", total)
c2.metric("Operativos", operativos, delta=f"{operativos/total*100:.1f}% del total")
c3.metric("Obsoletos / Baja", obsoletos, delta_color="inverse")

st.divider()

# Gráficos (Nativos)
col_graph1, col_graph2 = st.columns(2)

with col_graph1:
    st.subheader("Estado de Conservación")
    if not df_filtered.empty:
        st.bar_chart(df_filtered['Estado'].value_counts())
    else:
        st.info("No hay datos para mostrar.")

with col_graph2:
    st.subheader("Equipos Críticos (> 7 Años)")
    viejos = df_filtered[df_filtered['Antigüedad_Años'] > 7]
    if not viejos.empty:
        st.dataframe(viejos[['ID_Activo', 'Ubicación', 'Estado', 'Antigüedad_Años']], use_container_width=True, hide_index=True)
    else:
        st.success("No hay equipos con antigüedad crítica en esta selección.")

# Tabla General
st.markdown("### 📋 Inventario Completo")
st.dataframe(df_filtered, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.caption("Sistema EduTech ITSM v1.0 | Desarrollado por Alexander Galiano")
