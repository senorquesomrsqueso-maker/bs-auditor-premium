import streamlit as st
import yt_dlp
import pandas as pd
import re
import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILO PREMIUM ---
st.set_page_config(
    page_title="BS LATAM - Auditoría Pro", 
    page_icon="🚀", 
    layout="wide"
)

# Inyección de CSS para fondo oscuro y botones estilo Blood Strike
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    .stButton>button {
        background: linear-gradient(90deg, #8e0e00 0%, #1f1c18 100%) !important;
        color: white !important;
        border: 1px solid #ff4b2b !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        transition: 0.3s !important;
    }
    .stButton>button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0px 0px 15px rgba(255, 75, 43, 0.5) !important;
    }
    div[data-baseweb="tab-list"] { background-color: transparent !important; border-bottom: 2px solid #333 !important; }
    div[data-baseweb="tab"] { color: #888 !important; font-weight: bold !important; }
    div[data-baseweb="tab"][aria-selected="true"] { color: #ff4b2b !important; border-bottom-color: #ff4b2b !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LÓGICA DEL MOTOR DE EXTRACCIÓN ---
def extraer_datos_bs(texto):
    urls = re.findall(r"(https?://[^\s]+)", texto)
    # Limpieza de links para evitar errores de plataforma
    clean_urls = [u.split('?')[0].rstrip(',').rstrip(')').rstrip(']') for u in urls]
    
    if not clean_urls:
        return None
        
    resultados = []
    ydl_opts = {
        'quiet': True, 'extract_flat': True, 'skip_download': True, 'ignoreerrors': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    with st.spinner('🛰️ Extrayendo inteligencia de los enlaces...'):
        for url in clean_urls:
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    if info:
                        resultados.append({
                            "Creador": info.get('uploader', 'N/A'),
                            "Plataforma": "TikTok" if "tiktok" in url else "YouTube",
                            "Vistas": int(info.get('view_count') or 0),
                            "Likes": int(info.get('like_count') or 0),
                            "Link": url
                        })
            except: continue
    return pd.DataFrame(resultados)

# --- 3. INTERFAZ DE USUARIO ---
st.title("🚀 BS LATAM - SISTEMA DE AUDITORÍA DE ÉLITE")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["🔗 EXTRACTOR PRO", "🤖 PARTNER IA", "📂 SOPORTE DRIVE"])

with tab1:
    st.subheader("🔗 Procesador Masivo de Reportes")
    input_text = st.text_area("Pega los reportes o links directos aquí:", height=200, placeholder="Copia y pega desde Discord o Excel...")
    
    if st.button("EJECUTAR EXTRACCIÓN MAESTRA"):
        if input_text:
            df = extraer_datos_bs(input_text)
            if df is not None and not df.empty:
                st.success(f"✅ Se han auditado {len(df)} enlaces con éxito.")
                
                col_table, col_stats = st.columns([3, 1])
                with col_table:
                    st.dataframe(df, use_container_width=True)
                
                with col_stats:
                    total_v = df['Vistas'].sum()
                    st.metric("VISTAS TOTALES", f"{total_v:,}")
                    # Reporte formateado para copiar fácil
                    v_list = df['Vistas'].tolist()
                    reporte_mat = f"📊 REPORTE FINAL\nSuma: {' + '.join([f'{v:,}' for v in v_list])}\nTOTAL: {total_v:,}"
                    st.code(reporte_mat, language="text")
            else:
                st.error("❌ No se detectaron datos válidos. Revisa los links.")
        else:
            st.warning("⚠️ El campo de entrada está vacío.")

with tab2:
    st.subheader("🤖 Partner IA de Comando")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Mostrar historial de chat
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    if prompt := st.chat_input("¿Alguna duda con la auditoría, jefe?"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Respuesta del bot (Formato nativo de Streamlit)
        respuesta = "¡Recibido jefe! El sistema en Railway está operativo al 100%. ¿Qué más revisamos? 🫡"
        st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
        with st.chat_message("assistant"):
            st.markdown(respuesta)

with tab3:
    st.subheader("🛰️ Módulos en Sincronización")
    st.info("Este panel se activará automáticamente al detectar enlaces de Google Drive o escaneos de canal masivos.")
