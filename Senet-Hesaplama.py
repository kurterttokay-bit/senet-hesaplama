import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# Sayfa Ayarları
st.set_page_config(page_title="Kurter Finans | Pro", page_icon="🏦", layout="centered")

# Google Fonts'dan El Yazısı Fontu ve Kurumsal Stil
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600&display=swap" rel="stylesheet">
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 0rem; }
    h1 { text-align: center; color: #334155; font-size: 26px !important; font-weight: 700; margin-bottom: 0.5rem; }
    .signature { font-family: 'Dancing Script', cursive; font-size: 32px; color: #1e293b; margin-top: 10px; }
    .corporate-text { color: #64748b; font-size: 12px; letter-spacing: 1.5px; text-transform: uppercase; margin-top: -5px; }
    .stMetric { border: 1px solid #e2e8f0; padding: 10px; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("Kurter Finans Analiz")

# Girişler - Maksimum Kompaktlık
col1, col2 = st.columns(2)
with col1:
    ana_para = st.number_input("Senet Tutarı (₺)", min_value=0.0, value=100000.0, step=1000.0)
    secilen_faiz = st.slider("Faiz (%)", 1, 100, 53)
with col2:
    vade_tarihi = st.date_input("Vade Tarihi", value=datetime(2026, 6, 24))
    st.markdown("<br>", unsafe_allow_html=True)
    # Hızlı Bilgi Kartı
    bugun = datetime.now().date()
    kalan_gun = (vade_tarihi - bugun).days
    st.info(f"⏳ Kalan: {kalan_gun} Gün")

if ana_para > 0 and kalan_gun > 0:
    faiz_kazanci = ana_para * (secilen_faiz / 100) * (kalan_gun / 365)
    toplam_tutar = ana_para + faiz_kazanci
    
    # Metrikler
    m1, m2 = st.columns(2)
    m1.metric("Vade Sonu Toplam", f"{toplam_tutar:,.0f} ₺")
    m2.metric("Net Faiz Getirisi", f"{faiz_kazanci:,.0f} ₺")

    # Grafik - Minimalist Stil
    fig = go.Figure(data=[go.Pie(
        labels=['Anapara', 'Kazanç'], 
        values=[ana_para, faiz_kazanci], 
        hole=.75,
        marker=dict(colors=['#475569', '#cbd5e1']), # Slate ve Light Gray
        textinfo='none'
    )])
    
    fig.update_layout(
        height=200,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- ÖZEL EL YAZISI İMZA VE KURUMSAL ALT BİLGİ ---
st.markdown("---")
st.markdown(f"""
    <div style='text-align: center;'>
        <div class='signature'>Kurter</div>
        <div class='corporate-text'>Strategic Assets & Risk Management</div>
    </div>
    """, unsafe_allow_html=True)
