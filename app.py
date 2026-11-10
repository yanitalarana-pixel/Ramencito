import streamlit as st
import pandas as pd
from datetime import datetime

# 🌸 Configuración de página
st.set_page_config(page_title="Ramen Boutique", page_icon="🌸", layout="centered")

# 🎀 Estilos CSS: Morado, lila, delicado y lindo
st.markdown("""
<style>
    /* Fondo general lila muy clarito */
    .stApp {
        background-color: #FCF9FF;
        color: #4A148C;
        font-family: 'Nunito', 'Segoe UI', sans-serif;
    }
    /* Títulos en morado suave */
    h1, h2, h3 {
        color: #9C27B0 !important;
        font-weight: 700 !important;
    }
    /* Tarjetas de pedidos lindas */
    div[data-testid="stExpander"] {
        background-color: #F3E5F5;
        border: 1.5px solid #E1BEE7;
        border-radius: 16px;
        box-shadow: 0 4px 6px rgba(225, 190, 231, 0.2);
    }
    /* Botones redondeados y lilas */
    .stButton > button {
        background-color: #E1BEE7;
        color: #4A148C;
        border-radius: 20px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #CE93D8;
        color: white;
    }
    /* Texto de métricas en morado fuerte */
    div[data-testid="stMetricValue"] {
        color: #7B1FA2 !important;
    }
</style>
""", unsafe_allow_html=True)

# 📦 Base de datos temporal
if "pedidos" not in st.session_state:
    st.session_state.pedidos = []
if "contador" not in st.session_state:
    st.session_state.contador = 1

MENU = {
    "Shin Ramyun Clásico": 85.0,
    "Buldak Carbonara": 110.0,
    "Buldak Rosa (Ligero)": 105.0,
    "Nissin Sésamo": 90.0,
    "Bebida Cielito": 35.0
}

vista = st.sidebar.radio("Navegación 🌷", ["🌸 Para Clientes", "💜 Para la Dueña"])

# -------------------------------------------------------------
# 1. PANTALLA CLIENTES: DELICADA Y CON PRECIOS
# -------------------------------------------------------------
if vista == "🌸 Para Clientes":
    st.markdown("<h1 style='text-align: center;'>✨ Pedidos Mágicos ✨</h1>", unsafe_allow_html=True)
    st.caption("Busca tu número mágico. Cuando esté en la lista de listos, ¡puedes pasar por él!")

    df_pedidos = pd.DataFrame(st.session_state.pedidos)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🥣 Preparando...")
        if not df_pedidos.empty:
            preparando = df_pedidos[df_pedidos["estatus"] == "Preparando"]
            if not preparando.empty:
                for _, row in preparando.iterrows():
                    # Solo mostramos el número al cliente
                    st.info(f"**Orden #{row['id']}**")
            else:
                st.write("Sin pedidos en espera 🌸")
        else:
            st.write("Sin pedidos en espera 🌸")

    with col2:
        st.markdown("### 🎀 ¡Listos para ti!")
        if not df_pedidos.empty:
            listos = df_pedidos[df_pedidos["estatus"] == "¡Listo!"]
            if not listos.empty:
                for _, row in listos.iterrows():
                    # Aquí el cliente ve que está listo y cuánto fue
                    st.success(f"### 🎉 Orden #{row['id']}\nTotal: **${row['precio']:.2f}**")
            else:
                st.write("Pronto saldrán más platillos ✨")
        else:
            st.write("Pronto saldrán más platillos ✨")

# -------------------------------------------------------------
# 2. PANTALLA DUEÑA: CONTROL DE INVENTARIO Y FLUJO
# -------------------------------------------------------------
elif vista == "💜 Para la Dueña":
    st.markdown("<h1>💜 Panel de Administración</h1>", unsafe_allow_html=True)

    df_pedidos = pd.DataFrame(st.session_state.pedidos)

    # 📊 Métrica rápida superior para la dueña
    total_pedidos = len(df_pedidos)
    pendientes = len(df_pedidos[df_pedidos["estatus"] == "Preparando"]) if not df_pedidos.empty else 0
    
    col_m1, col_m2 = st.columns(2)
    col_m1.metric("🍜 Total de rámenes pedidos hoy", total_pedidos)
    col_m2.metric("⏳ Faltan por preparar", pendientes)
    st.divider()

    tab_nuevo, tab_cocina = st.tabs(["📝 Tomar Pedido", "🍳 En Cocina"])

    # 📝 Nueva Orden
    with tab_nuevo:
        st.subheader("Nuevo Pedido Lindo 🌸")
        producto_sel = st.selectbox("¿Qué ramen desean?", list(MENU.keys()))
        precio_sugerido = MENU[producto_sel]
        
        if st.button("Agregar a la lista 🎀"):
            nuevo = {
                "id": st.session_state.contador,
                "producto": producto_sel,
                "precio": precio_sugerido,
                "estatus": "Preparando",
            }
            st.session_state.pedidos.append(nuevo)
            st.session_state.contador += 1
            st.success(f"¡Orden #{nuevo['id']} registrada con éxito!")
            st.rerun()

    # 🍳 Control de cola de cocina
    with tab_cocina:
        st.subheader("Pedidos Pendientes")
        if df_pedidos.empty:
            st.write("No hay pedidos activos por ahora. ¡Todo limpio! 🧼")
        else:
            activos = [p for p in st.session_state.pedidos if p["estatus"] != "Entregado"]
            if not activos:
                st.write("No hay rámenes pendientes de entregar. 🌸")
            else:
                for p in activos:
                    with st.expander(f"Orden #{p['id']} - {p['producto']} ({p['estatus']})", expanded=True):
                        st.write(f"**Precio:** ${p['precio']:.2f}")
                        
                        if p["estatus"] == "Preparando":
                            if st.button("Avisar que está ¡Listo! 💜", key=f"listo_{p['id']}"):
                                p["estatus"] = "¡Listo!"
                                st.rerun()
                        elif p["estatus"] == "¡Listo!":
                            if st.button("Marcar como Entregado ✅", key=f"entregado_{p['id']}"):
                                p["estatus"] = "Entregado"
                                st.rerun()
