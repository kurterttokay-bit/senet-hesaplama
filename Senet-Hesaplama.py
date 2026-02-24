import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# Sayfa Ayarları
st.set_page_config(page_title="Kurter Finans | Pro", page_icon="🏦", layout="centered")

# Gelişmiş Tasarım ve Başlık Süsleme
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 0rem; }
    
    /* Başlık Süsleme */
    .main-title { 
        text-align: center; 
        color: #0f172a; 
        font-family: 'Inter', sans-serif;
        font-size: 28px; 
        font-weight: 800; 
        margin-bottom: 0px;
        letter-spacing: -0.5px;
    }
    .sub-title {
        text-align: center;
        color: #64748b;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 15px;
    }
    .title-underline {
        width: 50px;
        height: 3px;
        background: #1e293b;
        margin: 0 auto 20px auto;
        border-radius: 2px;
    }

    /* İmza ve Metrik Stilleri */
    .signature { font-family: 'Dancing Script', cursive; font-size: 40px; color: #0f172a; margin-top: 10px; }
    .corporate-text { color: #94a3b8; font-size: 11px; letter-spacing: 2px; text-transform: uppercase; margin-top: -10px; }
    .stMetric { border: 1px solid #f1f5f9; padding: 8px; border-radius: 12px; background: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# Süslü Başlık Alanı
st.markdown('<div class="main-title">KURTER FINANS</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Strategic Asset Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="title-underline"></div>', unsafe_allow_html=True)

# Girişler
c1, c2, c3 = st.columns([1.5, 1, 1.2])
with c1:
    ana_para = st.number_input("Ana Para (₺)", min_value=0.0, value=100000.0, step=1000.0)
with c2:
    secilen_faiz = st.number_input("Faiz (%)", min_value=1.0, value=53.0, step=0.5)
with c3:
    vade_tarihi = st.date_input("Vade", value=datetime(2026, 6, 24))

bugun = datetime.now().date()
kalan_gun = (vade_tarihi - bugun).days

if ana_para > 0 and kalan_gun > 0:
    faiz_kazanci = ana_para * (secilen_faiz / 100) * (kalan_gun / 365)
    toplam_tutar = ana_para + faiz_kazanci
    vergi_avantaji = faiz_kazanci * 0.075

    # Metrikler
    m1, m2, m3 = st.columns(3)
    m1.metric("Vade Sonu", f"{toplam_tutar:,.0f}")
    m2.metric("Gün", f"{kalan_gun}")
    m3.metric("Net Kâr", f"{faiz_kazanci:,.0f}")

    # Grafik - Yazıların kesilmemesi için 'pull' ve 'margin' ayarı eklendi
    fig = go.Figure(data=[go.Pie(
        labels=['Ana Para', 'Kâr'], 
        values=[ana_para, faiz_kazanci], 
        hole=.7,
        marker=dict(colors=['#1e293b', '#94a3b8']), 
        textinfo='label+percent',
        textposition='outside', # Yazıları dışarı aldık ama alanı genişlettik
        pull=[0, 0.05], # Kâr dilimini hafifçe öne çıkararak yer açtık
        textfont=dict(size=13, color='#0f172a')
    )])
    
    fig.update_layout(
        height=280, # Okunaklılık için yüksekliği biraz artırdık
        margin=dict(l=60, r=60, t=20, b=20), # Kenar boşluklarını artırarak yazıların kesilmesini önledik
        showlegend=False,
        annotations=[dict(text=f"₺{toplam_tutar:,.0f}", x=0.5, y=0.5, font_size=15, showarrow=False, font_color="#0f172a")]
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"<p style='text-align: center; color: #64748b; font-size: 11px; margin-top:-10px;'>Vergi Avantajı: {vergi_avantaji:,.0f} ₺</p>", unsafe_allow_html=True)

# --- İMZA BÖLÜMÜ ---
st.markdown(f"""
    <div style='text-align: center; border-top: 1px solid #f1f5f9; margin-top: 10px; padding-top: 10px;'>
        <div class='signature'>Kurter</div>
        <div class='corporate-text'>Strategic Assets & Risk Management</div>
    </div>
    """, unsafe_allow_html=True)
